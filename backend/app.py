from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import cv2
import numpy as np
import face_recognition
import subprocess
import base64
import os
import threading
import logging
import time
from dotenv import load_dotenv
from blockchain_service import create_blockchain_service_from_env
from utils import generate_file_hash, generate_user_hash, verify_file_integrity
from file_monitor import create_file_monitor

app = Flask(__name__, template_folder='../templates')
# Configure CORS for cloud deployment
CORS(app, resources={
    r"/*": {
        "origins": "*",  # Update with your specific Netlify domain in production
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

logging.basicConfig(level=logging.INFO)

# Load environment variables
load_dotenv()

# --- CONFIG ---
KNOWN_FACE = os.getenv("KNOWN_FACE", "just.jpg")  # Path to known reference image
# Use temp directory for cloud deployment compatibility
PRIVATE_FOLDER = os.getenv("PRIVATE_FOLDER", os.path.join(os.getcwd(), "private_files"))
MATCH_THRESHOLD = float(os.getenv("MATCH_THRESHOLD", "0.60"))       # Open folder if accuracy >= 60%
RESIZE_SCALE = 0.25
AUTO_CLOSE_SECONDS = int(os.getenv("AUTO_CLOSE_SECONDS", "10"))      # Close after 10 sec no match/no face

# Create private folder if it doesn't exist
os.makedirs(PRIVATE_FOLDER, exist_ok=True)

# Blockchain Configuration
BLOCKCHAIN_ENABLED = os.getenv("BLOCKCHAIN_ENABLED", "false").lower() == "true"
USER_ID = os.getenv("USER_ID", os.getlogin())  # User identifier for blockchain records
# ----------------

# Load known encoding
if not os.path.exists(KNOWN_FACE):
    logging.warning(f"Known face image not found: {KNOWN_FACE}. Face recognition will be disabled.")
    known_encoding = None
else:
    try:
        known_image = face_recognition.load_image_file(KNOWN_FACE)
        known_encodings = face_recognition.face_encodings(known_image)
        if not known_encodings:
            logging.warning("No faces found in known face image. Face recognition will be disabled.")
            known_encoding = None
        else:
            known_encoding = known_encodings[0]
            logging.info("Known face encoding loaded successfully")
    except Exception as e:
        logging.error(f"Error loading known face: {e}. Face recognition will be disabled.")
        known_encoding = None

# State variables
folder_open = False
last_match_time = 0
folder_open_lock = threading.Lock()

# Blockchain Service (initialized if enabled)
blockchain_service = None
if BLOCKCHAIN_ENABLED:
    try:
        blockchain_service = create_blockchain_service_from_env()
        if blockchain_service and blockchain_service.is_connected():
            logging.info("Blockchain service connected successfully")
        else:
            logging.warning("Blockchain service failed to connect, running without blockchain")
            blockchain_service = None
    except Exception as e:
        logging.error(f"Failed to initialize blockchain service: {e}")
        blockchain_service = None

# File Monitor (for tampering detection)
file_monitor = None
FILE_MONITORING_ENABLED = os.getenv("FILE_MONITORING_ENABLED", "false").lower() == "true"
if FILE_MONITORING_ENABLED and os.path.exists(PRIVATE_FOLDER):
    try:
        file_monitor = create_file_monitor(PRIVATE_FOLDER, check_interval=60)
        logging.info(f"File monitor initialized for {PRIVATE_FOLDER}")
    except Exception as e:
        logging.error(f"Failed to initialize file monitor: {e}")
        file_monitor = None


# ---------------- Permission Handling ----------------

def get_current_user():
    return os.getlogin()


def grant_access():
    user = get_current_user()
    cmd = f'icacls "{PRIVATE_FOLDER}" /grant:r "{user}:F"'
    os.system(cmd)
    logging.info(f"Access granted to {user}")
    
    # Record successful access to blockchain
    record_blockchain_access(
        user_id=USER_ID,
        file_path=PRIVATE_FOLDER,
        granted=True,
        access_type="LOGIN"
    )


def revoke_access():
    user = get_current_user()
    cmd = f'icacls "{PRIVATE_FOLDER}" /deny "{user}:F"'
    os.system(cmd)
    logging.info(f"Access revoked for {user}")


# ---------------- Folder Open/Close ----------------

def open_folder():
    """Grant access and open folder in Explorer."""
    try:
        grant_access()
        logging.info("Opening folder: %s", PRIVATE_FOLDER)
        subprocess.Popen(["explorer", "/e,", PRIVATE_FOLDER], shell=True)
    except Exception as e:
        logging.exception("Failed to open folder: %s", e)


def close_folder_win32():
    """Close the folder window using Win32 API."""
    try:
        import win32gui
        import win32con
    except ImportError:
        logging.info("pywin32 not available - skipping win32 close.")
        return False

    basename = os.path.basename(PRIVATE_FOLDER)
    closed_any = False

    def enum_handler(hwnd, _):
        nonlocal closed_any
        if not win32gui.IsWindowVisible(hwnd):
            return
        title = win32gui.GetWindowText(hwnd) or ""
        if basename.lower() in title.lower():
            logging.info("Closing window HWND=%s Title=%s", hwnd, title)
            try:
                win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
                closed_any = True
            except Exception as e:
                logging.exception("Failed to send WM_CLOSE: %s", e)

    win32gui.EnumWindows(enum_handler, None)
    return closed_any


def close_folder_taskkill_fallback():
    """Fallback method using taskkill."""
    basename = os.path.basename(PRIVATE_FOLDER)
    cmd = f'taskkill /FI "WINDOWTITLE contains {basename}" /F'
    try:
        logging.info("Running fallback taskkill: %s", cmd)
        os.system(cmd)
        return True
    except Exception as e:
        logging.exception("taskkill fallback failed: %s", e)
        return False


def close_folder():
    """Close folder window and revoke access."""
    try:
        closed = close_folder_win32()
        if not closed:
            close_folder_taskkill_fallback()
        revoke_access()
        return True
    except Exception as e:
        logging.exception("Failed to close folder: %s", e)
        return False


# ---------------- Blockchain Recording ----------------

def record_blockchain_access(user_id, file_path=None, granted=True, access_type="LOGIN"):
    """
    Record access attempt to blockchain if service is available.
    
    Args:
        user_id: User identifier
        file_path: Path to accessed file (optional)
        granted: Whether access was granted
        access_type: Type of access ("LOGIN", "FILE_ACCESS", "FILE_TAMPER")
        
    Returns:
        Transaction hash if successful, None otherwise
    """
    if blockchain_service:
        try:
            tx_hash = blockchain_service.record_access(
                user_id=user_id,
                file_path=file_path,
                granted=granted,
                access_type=access_type
            )
            if tx_hash:
                logging.info(f"Blockchain record created: {tx_hash}")
                return tx_hash
            else:
                logging.warning("Blockchain transaction failed")
                return None
        except Exception as e:
            logging.error(f"Error recording to blockchain: {e}")
            return None
    return None

# ---------------- Image Handling ----------------

def decode_base64_image(image_data_uri):
    """Convert base64 string to OpenCV image."""
    if not image_data_uri:
        return None
    if image_data_uri.startswith("data:"):
        parts = image_data_uri.split(",", 1)
        if len(parts) == 2:
            image_data_uri = parts[1]
    try:
        img_bytes = base64.b64decode(image_data_uri)
        np_arr = np.frombuffer(img_bytes, dtype=np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        return frame
    except Exception as e:
        logging.exception("Failed decoding base64 image: %s", e)
        return None


# ---------------- Flask Routes ----------------

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api")
def api_info():
    return jsonify({
        "message": "Deepfake Detection Backend API",
        "version": "1.0.0",
        "endpoints": {
            "check_face": "/check_face",
            "blockchain_status": "/api/blockchain/status",
            "user_history": "/api/blockchain/user_history",
            "verify_file": "/api/blockchain/verify_file",
            "file_monitor_status": "/api/file_monitor/status"
        }
    })


@app.route("/check_face", methods=["POST"])
def check_face():
    global folder_open, last_match_time
    data = request.get_json(force=True, silent=True) or {}
    image_data = data.get("image")

    frame = decode_base64_image(image_data)
    if frame is None:
        return jsonify({"status": "error", "message": "Image decoding failed"}), 400

    small_frame = cv2.resize(frame, (0, 0), fx=RESIZE_SCALE, fy=RESIZE_SCALE)
    rgb_small = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb_small, model="hog")
    matched = False
    best_accuracy = 0.0

    # Check if face recognition is available
    if known_encoding is None:
        return jsonify({
            "status": "error",
            "message": "Face recognition not available - known face image not loaded",
            "matched": False,
            "accuracy": 0.0
        }), 503

    if face_locations:
        face_encodings = face_recognition.face_encodings(rgb_small, face_locations)
        for enc in face_encodings:
            distance = face_recognition.face_distance([known_encoding], enc)[0]
            confidence = max(0.0, min(1.0, 1.0 - distance))
            accuracy_pct = confidence * 100.0
            if accuracy_pct > best_accuracy:
                best_accuracy = accuracy_pct
            if confidence >= MATCH_THRESHOLD:
                matched = True
                break
    else:
        best_accuracy = 0.0

    with folder_open_lock:
        if matched:
            last_match_time = time.time()
            if not folder_open:
                open_folder()
                folder_open = True
            return jsonify({
                "status": "opened" if not folder_open else "unchanged",
                "matched": True,
                "accuracy": round(best_accuracy, 2)
            })
        else:
            if folder_open and (time.time() - last_match_time > AUTO_CLOSE_SECONDS):
                close_folder()
                folder_open = False
                # Record failed access/closure to blockchain
                record_blockchain_access(
                    user_id=USER_ID,
                    file_path=PRIVATE_FOLDER,
                    granted=False,
                    access_type="LOGIN"
                )
                return jsonify({
                    "status": "closed",
                    "matched": False,
                    "accuracy": round(best_accuracy, 2)
                })

    return jsonify({
        "status": "unchanged",
        "matched": matched,
        "accuracy": round(best_accuracy, 2)
    })


# ---------------- Blockchain API Routes ----------------

@app.route("/api/blockchain/status", methods=["GET"])
def blockchain_status():
    """Get blockchain connection status."""
    if not blockchain_service:
        return jsonify({
            "enabled": False,
            "connected": False,
            "message": "Blockchain service not initialized"
        })
    
    return jsonify({
        "enabled": True,
        "connected": blockchain_service.is_connected(),
        "total_records": blockchain_service.get_total_records(),
        "account_balance": blockchain_service.get_account_balance()
    })


@app.route("/api/blockchain/user_history", methods=["GET"])
def get_user_history():
    """Get blockchain access history for current user."""
    if not blockchain_service:
        return jsonify({
            "error": "Blockchain service not available"
        }), 503
    
    try:
        history = blockchain_service.get_user_history(USER_ID)
        records = []
        
        for record_id in history:
            record = blockchain_service.get_access_record(record_id)
            if record:
                records.append({
                    "record_id": record_id,
                    **record
                })
        
        return jsonify({
            "user_id": USER_ID,
            "total_records": len(records),
            "history": records
        })
    except Exception as e:
        logging.error(f"Error getting user history: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/blockchain/verify_file", methods=["POST"])
def verify_file_integrity_api():
    """Verify file integrity against blockchain records."""
    if not blockchain_service:
        return jsonify({
            "error": "Blockchain service not available"
        }), 503
    
    data = request.get_json(force=True, silent=True) or {}
    file_path = data.get("file_path")
    
    if not file_path:
        return jsonify({"error": "file_path is required"}), 400
    
    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404
    
    try:
        is_valid = blockchain_service.verify_file_integrity(USER_ID, file_path)
        current_hash = generate_file_hash(file_path)
        
        # Record this verification attempt
        record_blockchain_access(
            user_id=USER_ID,
            file_path=file_path,
            granted=is_valid,
            access_type="FILE_TAMPER" if not is_valid else "FILE_ACCESS"
        )
        
        return jsonify({
            "file_path": file_path,
            "is_valid": is_valid,
            "current_hash": current_hash.hex() if current_hash else None,
            "message": "File integrity verified" if is_valid else "File has been tampered with"
        })
    except Exception as e:
        logging.error(f"Error verifying file integrity: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/blockchain/record_manual", methods=["POST"])
def record_manual_access():
    """Manually record an access event to blockchain."""
    if not blockchain_service:
        return jsonify({
            "error": "Blockchain service not available"
        }), 503
    
    data = request.get_json(force=True, silent=True) or {}
    file_path = data.get("file_path")
    granted = data.get("granted", True)
    access_type = data.get("access_type", "MANUAL")
    
    try:
        tx_hash = record_blockchain_access(
            user_id=USER_ID,
            file_path=file_path,
            granted=granted,
            access_type=access_type
        )
        
        if tx_hash:
            return jsonify({
                "success": True,
                "transaction_hash": tx_hash,
                "message": "Access recorded to blockchain"
            })
        else:
            return jsonify({
                "success": False,
                "message": "Failed to record access"
            }), 500
    except Exception as e:
        logging.error(f"Error recording manual access: {e}")
        return jsonify({"error": str(e)}), 500


# ---------------- File Monitoring API Routes ----------------

@app.route("/api/file_monitor/status", methods=["GET"])
def file_monitor_status():
    """Get file monitoring status."""
    if not file_monitor:
        return jsonify({
            "enabled": False,
            "message": "File monitoring not initialized"
        })
    
    return jsonify({
        "enabled": True,
        "monitoring": file_monitor.monitoring,
        "directory": file_monitor.directory_path,
        "monitored_files": len(file_monitor.file_hashes),
        "check_interval": file_monitor.check_interval
    })


@app.route("/api/file_monitor/start", methods=["POST"])
def start_file_monitoring():
    """Start file monitoring."""
    if not file_monitor:
        return jsonify({
            "error": "File monitor not available"
        }), 503
    
    try:
        file_monitor.start_monitoring()
        return jsonify({
            "success": True,
            "message": "File monitoring started"
        })
    except Exception as e:
        logging.error(f"Error starting file monitoring: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/file_monitor/stop", methods=["POST"])
def stop_file_monitoring():
    """Stop file monitoring."""
    if not file_monitor:
        return jsonify({
            "error": "File monitor not available"
        }), 503
    
    try:
        file_monitor.stop_monitoring()
        return jsonify({
            "success": True,
            "message": "File monitoring stopped"
        })
    except Exception as e:
        logging.error(f"Error stopping file monitoring: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/file_monitor/check", methods=["POST"])
def check_file_integrity_manual():
    """Manually trigger file integrity check."""
    if not file_monitor:
        return jsonify({
            "error": "File monitor not available"
        }), 503
    
    try:
        results = file_monitor.check_directory_integrity()
        
        tampered_files = [file_path for file_path, is_valid in results.items() if not is_valid]
        
        return jsonify({
            "total_files": len(results),
            "intact_files": len(results) - len(tampered_files),
            "tampered_files": tampered_files,
            "results": {k: v for k, v in results.items()}
        })
    except Exception as e:
        logging.error(f"Error checking file integrity: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/file_monitor/files", methods=["GET"])
def get_monitored_files():
    """Get list of monitored files."""
    if not file_monitor:
        return jsonify({
            "error": "File monitor not available"
        }), 503
    
    try:
        files = file_monitor.get_monitored_files()
        return jsonify({
            "total_files": len(files),
            "files": files
        })
    except Exception as e:
        logging.error(f"Error getting monitored files: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/file_monitor/add", methods=["POST"])
def add_file_to_monitor():
    """Add a file to monitoring."""
    if not file_monitor:
        return jsonify({
            "error": "File monitor not available"
        }), 503
    
    data = request.get_json(force=True, silent=True) or {}
    file_path = data.get("file_path")
    
    if not file_path:
        return jsonify({"error": "file_path is required"}), 400
    
    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404
    
    try:
        file_monitor.add_file_to_monitor(file_path)
        return jsonify({
            "success": True,
            "message": f"File added to monitoring: {file_path}"
        })
    except Exception as e:
        logging.error(f"Error adding file to monitor: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_ENV") == "development"
    app.run(debug=debug, host="0.0.0.0", port=port)
