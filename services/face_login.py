"""
Face login module for FaceSecure application.
Handles face capture, encoding comparison, and user verification.
"""

import cv2
import face_recognition
import numpy as np
from datetime import datetime
from database.mongodb import users
from services.camera import open_camera, read_frame, close_camera, convert_to_rgb, display_frame
from services.blink_detection import BlinkDetector
from config import FACE_DETECTION_MODEL, UPSAMPLE_TIMES, FACE_MATCH_THRESHOLD, REQUIRED_BLINKS


def verify_face():
    """
    Verify live face against stored encodings in database.
    
    Returns:
        User document if match found, None otherwise
    """
    # Open camera
    camera = open_camera()
    
    # Liveness check
    blink_detector = BlinkDetector()
    if not blink_detector.check_liveness(camera):
        close_camera(camera)
        return None
    
    # Capture live face encoding
    live_encoding = capture_face_encoding(camera)
    
    if live_encoding is None:
        close_camera(camera)
        return None
    
    # Close camera
    close_camera(camera)
    
    # Get all users from database
    all_users = list(users.find())
    
    # Compare against all users
    for user in all_users:
        stored_encoding = np.array(user["face_encoding"])
        
        # Compare faces
        result = face_recognition.compare_faces(
            [stored_encoding],
            live_encoding,
            tolerance=FACE_MATCH_THRESHOLD
        )
        
        if result[0]:
            # Update last login
            users.update_one(
                {"_id": user["_id"]},
                {"$set": {"last_login": datetime.now()}}
            )
            return user
    
    return None


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
        
        display_frame(frame, "Face Login")
        
        # Wait for exactly one face
        if len(face_locations) == 1:
            encoding = face_recognition.face_encodings(rgb_frame, face_locations)[0]
            break
        
        # Exit on 'q' press
        if cv2.waitKey(1) == ord('q'):
            break
    
    return encoding
