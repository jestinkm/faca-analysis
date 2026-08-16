"""
Liveness detection service for FaceSecure application.
Handles blink detection, head pose estimation, and anti-spoofing.
"""

import cv2
import numpy as np
from typing import Tuple, Optional, List
from config import BLINK_THRESHOLD, BLINK_CONSECUTIVE_FRAMES, HEAD_POSE_THRESHOLD
from utils.logger import get_logger


class LivenessService:
    """Service for liveness detection operations."""
    
    def __init__(self):
        """Initialize liveness service."""
        self.logger = get_logger('liveness_service')
        self.blink_frame_count = 0
        self.head_pose_history = []
    
    def calculate_ear(self, eye_landmarks: List[Tuple[int, int]]) -> float:
        """
        Calculate Eye Aspect Ratio (EAR) for blink detection.
        
        Args:
            eye_landmarks: List of 6 eye landmark points
            
        Returns:
            Eye Aspect Ratio value
        """
        # Vertical eye landmarks
        p2 = np.array(eye_landmarks[1])
        p6 = np.array(eye_landmarks[5])
        p3 = np.array(eye_landmarks[2])
        p5 = np.array(eye_landmarks[4])
        
        # Horizontal eye landmarks
        p1 = np.array(eye_landmarks[0])
        p4 = np.array(eye_landmarks[3])
        
        # Calculate vertical distances
        vertical_1 = np.linalg.norm(p2 - p6)
        vertical_2 = np.linalg.norm(p3 - p5)
        
        # Calculate horizontal distance
        horizontal = np.linalg.norm(p1 - p4)
        
        # Calculate EAR
        ear = (vertical_1 + vertical_2) / (2.0 * horizontal)
        
        return ear
    
    def detect_blink(self, landmarks: dict) -> bool:
        """
        Detect blink using Eye Aspect Ratio.
        
        Args:
            landmarks: Facial landmarks dictionary
            
        Returns:
            True if blink detected, False otherwise
        """
        try:
            # Get left eye landmarks
            left_eye = landmarks.get('left_eye', [])
            # Get right eye landmarks
            right_eye = landmarks.get('right_eye', [])
            
            if not left_eye or not right_eye:
                return False
            
            # Calculate EAR for both eyes
            left_ear = self.calculate_ear(left_eye)
            right_ear = self.calculate_ear(right_eye)
            
            # Average EAR
            ear = (left_ear + right_ear) / 2.0
            
            # Check if blink
            if ear < BLINK_THRESHOLD:
                self.blink_frame_count += 1
            else:
                self.blink_frame_count = 0
            
            # Blink detected if consecutive frames below threshold
            blink_detected = self.blink_frame_count >= BLINK_CONSECUTIVE_FRAMES
            
            if blink_detected:
                self.logger.info("Blink detected")
                self.blink_frame_count = 0  # Reset after detection
            
            return blink_detected
            
        except Exception as e:
            self.logger.error(f"Error detecting blink: {str(e)}")
            return False
    
    def detect_head_pose(self, landmarks: dict) -> Tuple[str, bool]:
        """
        Detect head pose direction.
        
        Args:
            landmarks: Facial landmarks dictionary
            
        Returns:
            Tuple of (direction, is_movement_detected)
        """
        try:
            # Get nose tip and other reference points
            nose_tip = landmarks.get('nose_tip', [])
            chin = landmarks.get('chin', [])
            left_eyebrow = landmarks.get('left_eyebrow', [])
            right_eyebrow = landmarks.get('right_eyebrow', [])
            
            if not nose_tip or not chin or not left_eyebrow or not right_eyebrow:
                return "unknown", False
            
            nose_tip = np.array(nose_tip[0])
            chin_center = np.array(chin[len(chin) // 2])
            left_eyebrow_center = np.array(left_eyebrow[len(left_eyebrow) // 2])
            right_eyebrow_center = np.array(right_eyebrow[len(right_eyebrow) // 2])
            
            # Calculate horizontal offset
            face_center_x = (left_eyebrow_center[0] + right_eyebrow_center[0]) / 2
            horizontal_offset = nose_tip[0] - face_center_x
            face_width = right_eyebrow_center[0] - left_eyebrow_center[0]
            
            # Calculate vertical offset
            face_center_y = (left_eyebrow_center[1] + right_eyebrow_center[1]) / 2
            vertical_offset = nose_tip[1] - face_center_y
            face_height = chin_center[1] - face_center_y
            
            # Determine direction
            direction = "center"
            is_movement = False
            
            # Horizontal movement
            if abs(horizontal_offset) > face_width * HEAD_POSE_THRESHOLD:
                if horizontal_offset > 0:
                    direction = "right"
                else:
                    direction = "left"
                is_movement = True
            
            # Vertical movement
            if abs(vertical_offset) > face_height * HEAD_POSE_THRESHOLD:
                if vertical_offset > 0:
                    direction = "down"
                else:
                    direction = "up"
                is_movement = True
            
            # Track head pose history
            self.head_pose_history.append(direction)
            if len(self.head_pose_history) > 10:
                self.head_pose_history.pop(0)
            
            # Check for movement in history
            if len(set(self.head_pose_history)) > 1:
                is_movement = True
            
            return direction, is_movement
            
        except Exception as e:
            self.logger.error(f"Error detecting head pose: {str(e)}")
            return "unknown", False
    
    def check_liveness(self, image: np.ndarray, landmarks: dict, require_blink: bool = True, require_head_movement: bool = True) -> Tuple[bool, str]:
        """
        Perform comprehensive liveness check.
        
        Args:
            image: Input image
            landmarks: Facial landmarks
            require_blink: Whether to require blink detection
            require_head_movement: Whether to require head movement
            
        Returns:
            Tuple of (is_live, reason)
        """
        try:
            # Check blink if required
            if require_blink:
                blink_detected = self.detect_blink(landmarks)
                if not blink_detected:
                    return False, "No blink detected"
            
            # Check head movement if required
            if require_head_movement:
                direction, movement_detected = self.detect_head_pose(landmarks)
                if not movement_detected:
                    return False, "No head movement detected"
            
            self.logger.info("Liveness check passed")
            return True, "Liveness verified"
            
        except Exception as e:
            self.logger.error(f"Error in liveness check: {str(e)}")
            return False, f"Liveness check error: {str(e)}"
    
    def reset_state(self):
        """Reset liveness detection state."""
        self.blink_frame_count = 0
        self.head_pose_history = []
        self.logger.debug("Liveness state reset")
