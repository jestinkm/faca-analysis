"""
Blink detection module for FaceSecure application.
Uses MediaPipe for blink detection (anti-spoofing).
"""

import cv2
import mediapipe as mp
import numpy as np
from config import BLINK_THRESHOLD, BLINK_CONSECUTIVE_FRAMES, REQUIRED_BLINKS


class BlinkDetector:
    """Blink detector using MediaPipe Face Mesh."""
    
    def __init__(self):
        """Initialize MediaPipe face mesh."""
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        # Eye landmark indices
        self.LEFT_EYE = [33, 160, 158, 133, 153, 144]
        self.RIGHT_EYE = [362, 385, 387, 263, 373, 380]
        
        # Reset counters
        self.reset()
    
    def reset(self):
        """Reset blink counters."""
        self.blink_counter = 0
        self.total_blinks = 0
    
    def calculate_ear(self, eye_landmarks):
        """
        Calculate Eye Aspect Ratio (EAR) for blink detection.
        
        Args:
            eye_landmarks: List of 6 eye landmark points
            
        Returns:
            EAR value
        """
        # Vertical eye landmarks
        A = np.linalg.norm(np.array(eye_landmarks[1]) - np.array(eye_landmarks[5]))
        B = np.linalg.norm(np.array(eye_landmarks[2]) - np.array(eye_landmarks[4]))
        
        # Horizontal eye landmark
        C = np.linalg.norm(np.array(eye_landmarks[0]) - np.array(eye_landmarks[3]))
        
        # EAR formula
        ear = (A + B) / (2.0 * C)
        return ear
    
    def detect_blink(self, frame):
        """
        Detect blink in frame.
        
        Args:
            frame: Input frame (BGR)
            
        Returns:
            Tuple of (is_blinking, total_blinks)
        """
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process with MediaPipe
        results = self.face_mesh.process(rgb_frame)
        
        if not results.multi_face_landmarks:
            return False, self.total_blinks
        
        # Get first face landmarks
        landmarks = results.multi_face_landmarks[0]
        
        # Get eye landmarks
        h, w = frame.shape[:2]
        left_eye = [(landmarks.landmark[i].x * w, landmarks.landmark[i].y * h) 
                    for i in self.LEFT_EYE]
        right_eye = [(landmarks.landmark[i].x * w, landmarks.landmark[i].y * h) 
                     for i in self.RIGHT_EYE]
        
        # Calculate EAR for both eyes
        left_ear = self.calculate_ear(left_eye)
        right_ear = self.calculate_ear(right_eye)
        
        # Average EAR
        ear = (left_ear + right_ear) / 2.0
        
        # Check for blink
        if ear < BLINK_THRESHOLD:
            self.blink_counter += 1
        else:
            if self.blink_counter >= BLINK_CONSECUTIVE_FRAMES:
                self.total_blinks += 1
                self.blink_counter = 0
            else:
                self.blink_counter = 0
        
        return self.blink_counter >= BLINK_CONSECUTIVE_FRAMES, self.total_blinks
    
    def check_liveness(self, camera, max_seconds=10):
        """
        Check liveness by requiring blinks.
        
        Args:
            camera: OpenCV camera object
            max_seconds: Maximum time to wait for liveness check
            
        Returns:
            True if liveness confirmed, False otherwise
        """
        import time
        start_time = time.time()
        
        while time.time() - start_time < max_seconds:
            ret, frame = camera.read()
            if not ret:
                continue
            
            is_blinking, total_blinks = self.detect_blink(frame)
            
            # Display status
            status = f"Blinks: {total_blinks}/{REQUIRED_BLINKS}"
            cv2.putText(
                frame,
                status,
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0) if total_blinks >= REQUIRED_BLINKS else (0, 0, 255),
                2
            )
            
            cv2.imshow("Liveness Check", frame)
            
            if total_blinks >= REQUIRED_BLINKS:
                cv2.destroyAllWindows()
                return True
            
            if cv2.waitKey(1) == ord('q'):
                cv2.destroyAllWindows()
                return False
        
        cv2.destroyAllWindows()
        return False
