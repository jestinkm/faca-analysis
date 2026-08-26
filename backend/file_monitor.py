import os
import time
import threading
import logging
from typing import Dict, Callable, Optional
from utils import generate_file_hash, monitor_directory_changes
from blockchain_service import create_blockchain_service_from_env

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FileMonitor:
    def __init__(self, directory_path: str, blockchain_service=None, check_interval: int = 60):
        """
        Initialize file monitor for detecting tampering.
        
        Args:
            directory_path: Directory to monitor
            blockchain_service: Blockchain service for recording tampering events
            check_interval: Time in seconds between checks
        """
        self.directory_path = directory_path
        self.blockchain_service = blockchain_service
        self.check_interval = check_interval
        self.file_hashes: Dict[str, bytes] = {}
        self.monitoring = False
        self.monitor_thread = None
        self.callbacks = []
        
        # Initialize file hashes
        self._initialize_file_hashes()

    def _initialize_file_hashes(self):
        """Initialize hashes for all files in the directory."""
        logger.info(f"Initializing file hashes for {self.directory_path}")
        
        if not os.path.exists(self.directory_path):
            logger.warning(f"Directory does not exist: {self.directory_path}")
            return
        
        for root, dirs, files in os.walk(self.directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                # Skip encrypted files and system files
                if not file.endswith('.encrypted') and not file.startswith('.'):
                    file_hash = generate_file_hash(file_path)
                    if file_hash:
                        self.file_hashes[file_path] = file_hash
                        logger.info(f"Initialized hash for {file_path}")

    def check_file_integrity(self, file_path: str) -> bool:
        """
        Check if a specific file has been tampered with.
        
        Args:
            file_path: Path to file to check
            
        Returns:
            True if file is intact, False if tampered
        """
        if file_path not in self.file_hashes:
            logger.warning(f"File not in monitoring list: {file_path}")
            return True  # Not monitoring, assume intact
        
        current_hash = generate_file_hash(file_path)
        if current_hash is None:
            logger.error(f"Failed to generate hash for {file_path}")
            return False
        
        stored_hash = self.file_hashes[file_path]
        
        if current_hash != stored_hash:
            logger.warning(f"FILE TAMPERED: {file_path}")
            self._handle_tampering(file_path, stored_hash, current_hash)
            return False
        
        return True

    def _handle_tampering(self, file_path: str, original_hash: bytes, new_hash: bytes):
        """
        Handle detected file tampering.
        
        Args:
            file_path: Path to tampered file
            original_hash: Original file hash
            new_hash: New file hash
        """
        # Record to blockchain if service available
        if self.blockchain_service:
            try:
                from blockchain_service import hash_to_hex_string
                user_id = os.getenv("USER_ID", os.getlogin())
                
                self.blockchain_service.record_access(
                    user_id=user_id,
                    file_path=file_path,
                    granted=False,
                    access_type="FILE_TAMPER"
                )
                logger.info(f"Tampering event recorded to blockchain for {file_path}")
            except Exception as e:
                logger.error(f"Failed to record tampering to blockchain: {e}")
        
        # Call registered callbacks
        for callback in self.callbacks:
            try:
                callback(file_path, original_hash, new_hash)
            except Exception as e:
                logger.error(f"Callback error: {e}")

    def check_directory_integrity(self) -> Dict[str, bool]:
        """
        Check integrity of all monitored files.
        
        Returns:
            Dictionary mapping file paths to integrity status
        """
        results = {}
        
        for file_path in list(self.file_hashes.keys()):
            if os.path.exists(file_path):
                results[file_path] = self.check_file_integrity(file_path)
            else:
                logger.warning(f"File no longer exists: {file_path}")
                results[file_path] = False
                self._handle_tampering(file_path, self.file_hashes[file_path], None)
        
        return results

    def update_file_hash(self, file_path: str):
        """
        Update the stored hash for a file (call after legitimate modifications).
        
        Args:
            file_path: Path to file to update
        """
        new_hash = generate_file_hash(file_path)
        if new_hash:
            self.file_hashes[file_path] = new_hash
            logger.info(f"Updated hash for {file_path}")

    def add_callback(self, callback: Callable):
        """
        Add a callback function to be called on tampering detection.
        
        Args:
            callback: Function that takes (file_path, original_hash, new_hash)
        """
        self.callbacks.append(callback)

    def start_monitoring(self):
        """Start continuous monitoring in a background thread."""
        if self.monitoring:
            logger.warning("Monitoring already active")
            return
        
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        logger.info("File monitoring started")

    def stop_monitoring(self):
        """Stop continuous monitoring."""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        logger.info("File monitoring stopped")

    def _monitor_loop(self):
        """Main monitoring loop."""
        while self.monitoring:
            try:
                self.check_directory_integrity()
                time.sleep(self.check_interval)
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                time.sleep(self.check_interval)

    def add_file_to_monitor(self, file_path: str):
        """
        Add a new file to monitoring.
        
        Args:
            file_path: Path to file to add
        """
        if os.path.exists(file_path):
            file_hash = generate_file_hash(file_path)
            if file_hash:
                self.file_hashes[file_path] = file_hash
                logger.info(f"Added file to monitoring: {file_path}")

    def remove_file_from_monitor(self, file_path: str):
        """
        Remove a file from monitoring.
        
        Args:
            file_path: Path to file to remove
        """
        if file_path in self.file_hashes:
            del self.file_hashes[file_path]
            logger.info(f"Removed file from monitoring: {file_path}")

    def get_monitored_files(self) -> list:
        """Get list of currently monitored files."""
        return list(self.file_hashes.keys())


def create_file_monitor(directory_path: str, check_interval: int = 60) -> FileMonitor:
    """
    Create a file monitor with blockchain integration if available.
    
    Args:
        directory_path: Directory to monitor
        check_interval: Time in seconds between checks
        
    Returns:
        FileMonitor instance
    """
    blockchain_service = None
    try:
        blockchain_service = create_blockchain_service_from_env()
        if blockchain_service and blockchain_service.is_connected():
            logger.info("Blockchain service connected for file monitoring")
        else:
            blockchain_service = None
    except Exception as e:
        logger.error(f"Failed to initialize blockchain for file monitoring: {e}")
    
    return FileMonitor(directory_path, blockchain_service, check_interval)