"""
Face registration module for FaceSecure application.
Handles face capture, detection, encoding, and storage.
"""

import cv2
import face_recognition
import numpy as np
from datetime import datetime
from database.mongodb import users
from services.camera import open_camera, read_frame, close_camera, convert_to_rgb, display_frame
from services.blink_detection import BlinkDetector
from config import FACE_DETECTION_MODEL, UPSAMPLE_TIMES, REQUIRED_BLINKS


def register_user(name, email):
    """
    Register a new user with face capture and encoding.
    
    Args:
        name: User name
        email: User email
        
    Returns:
        Tuple of (success, message)
    """
    # Check if user already exists
    if users.find_one({"email": email}):
        return False, "Email already registered"
    
    # Open camera
    camera = open_camera()
    
    # Liveness check
    blink_detector = BlinkDetector()
    if not blink_detector.check_liveness(camera):
        close_camera(camera)
        return False, "Liveness check failed"
    
    # Capture face encoding
    encoding = capture_face_encoding(camera)
    
    if encoding is None:
        close_camera(camera)
        return False, "Face not detected"
    
    # Close camera
    close_camera(camera)
    
    # Store in database
    user_doc = {
        "name": name,
        "email": email,
        "face_encoding": encoding.tolist(),
        "created_at": datetime.now(),
        "last_login": None
    }
    
    result = users.insert_one(user_doc)
    
    if result.inserted_id:
        return True, "Registration successful"
    else:
        return False, "Registration failed"


def capture_face_encoding(camera):
    """
    Capture face encoding from camera.
    Waits until exactly one face is detected.
    
    Args:
        camera: OpenCV camera object
        
    Returns:
        Face encoding as numpy array or None if failed
    """
    encoding = None
    
    while True:
        frame = read_frame(camera)
        if frame is None:
            continue
        
        # Convert to RGB
        rgb_frame = convert_to_rgb(frame)
        
        # Detect faces
        face_locations = face_recognition.face_locations(
            rgb_frame,
            model=FACE_DETECTION_MODEL,
            number_of_times_to_upsample=UPSAMPLE_TIMES
        )
        
        # Display face count
        cv2.putText(
            frame,
            f"Faces: {len(face_locations)}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0) if len(face_locations) == 1 else (0, 0, 255),
            2
        )
        
        display_frame(frame, "Face Registration")
        
        # Wait for exactly one face
        if len(face_locations) == 1:
            encoding = face_recognition.face_encodings(rgb_frame, face_locations)[0]
            break
        
        # Exit on 'q' press
        if cv2.waitKey(1) == ord('q'):
            break
    
    return encoding
