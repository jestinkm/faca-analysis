"""
Face recognition service for FaceSecure application.
Handles face detection, encoding, and matching.
"""

import cv2
import face_recognition
import numpy as np
import pickle
from typing import List, Tuple, Optional
from config import FACE_MATCH_THRESHOLD, FACE_DETECTION_MODEL, NUM_JITTERS, UPSAMPLE_TIMES
from utils.logger import get_logger


class FaceService:
    """Service for face recognition operations."""
    
    def __init__(self):
        """Initialize face service."""
        self.logger = get_logger('face_service')
    
    def detect_faces(self, image: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """
        Detect faces in an image.
        
        Args:
            image: Input image as numpy array
            
        Returns:
            List of face locations (top, right, bottom, left)
        """
        try:
            # DEBUG: Print image shape and type
            print(f"DEBUG: Image shape: {image.shape}, dtype: {image.dtype}")
            
            # Convert BGR to RGB if needed
            if len(image.shape) == 3 and image.shape[2] == 3:
                image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                print(f"DEBUG: Converted BGR to RGB")
            else:
                image_rgb = image
                print(f"DEBUG: Using image as-is (not 3 channels)")
            
            # Detect faces with upsampling for better detection
            face_locations = face_recognition.face_locations(
                image_rgb,
                model=FACE_DETECTION_MODEL,
                number_of_times_to_upsample=UPSAMPLE_TIMES
            )
            
            if not face_locations and FACE_DETECTION_MODEL.lower() != 'cnn':
                self.logger.debug(f"No faces detected with model={FACE_DETECTION_MODEL}, trying cnn fallback")
                face_locations = face_recognition.face_locations(
                    image_rgb,
                    model='cnn'
                )
            
            print(f"DEBUG: Faces detected: {len(face_locations)}; locations={face_locations}")
            self.logger.debug(f"Detected {len(face_locations)} face(s)")
            return face_locations
            
        except Exception as e:
            self.logger.error(f"Error detecting faces: {str(e)}")
            return []
    
    def encode_face(self, image: np.ndarray, face_location: Optional[Tuple[int, int, int, int]] = None) -> Optional[np.ndarray]:
        """
        Encode a face from an image.
        
        Args:
            image: Input image as numpy array
            face_location: Specific face location to encode (optional)
            
        Returns:
            Face encoding as numpy array or None if failed
        """
        try:
            # Convert BGR to RGB if needed
            if len(image.shape) == 3 and image.shape[2] == 3:
                image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            else:
                image_rgb = image
            
            # Get face locations if not provided
            if face_location is None:
                face_locations = self.detect_faces(image)
                if not face_locations:
                    self.logger.warning("No face detected for encoding")
                    return None
                face_location = face_locations[0]
            
            # Encode face
            face_encodings = face_recognition.face_encodings(
                image_rgb,
                known_face_locations=[face_location],
                num_jitters=NUM_JITTERS
            )
            
            if not face_encodings:
                self.logger.warning("Failed to encode face")
                return None
            
            return face_encodings[0]
            
        except Exception as e:
            self.logger.error(f"Error encoding face: {str(e)}")
            return None
    
    def compare_faces(self, face_encoding1: np.ndarray, face_encoding2: np.ndarray) -> Tuple[bool, float]:
        """
        Compare two face encodings.
        
        Args:
            face_encoding1: First face encoding
            face_encoding2: Second face encoding
            
        Returns:
            Tuple of (is_match, distance)
        """
        try:
            # Calculate distance
            distance = face_recognition.face_distance([face_encoding1], face_encoding2)[0]
            
            # Check if match
            is_match = distance <= FACE_MATCH_THRESHOLD
            
            self.logger.debug(f"Face comparison - Distance: {distance:.4f}, Match: {is_match}")
            return is_match, distance
            
        except Exception as e:
            self.logger.error(f"Error comparing faces: {str(e)}")
            return False, 1.0
    
    def match_face_against_encoding(self, image: np.ndarray, stored_encoding: np.ndarray) -> Tuple[bool, float]:
        """
        Match a face from image against stored encoding.
        
        Args:
            image: Input image
            stored_encoding: Stored face encoding
            
        Returns:
            Tuple of (is_match, distance)
        """
        try:
            # Detect faces
            face_locations = self.detect_faces(image)
            
            if not face_locations:
                self.logger.warning("No face detected in image")
                return False, 1.0
            
            if len(face_locations) > 1:
                self.logger.warning("Multiple faces detected in image")
                return False, 1.0
            
            # Encode face
            face_encoding = self.encode_face(image, face_locations[0])
            
            if face_encoding is None:
                self.logger.warning("Failed to encode face from image")
                return False, 1.0
            
            # Compare with stored encoding
            return self.compare_faces(face_encoding, stored_encoding)
            
        except Exception as e:
            self.logger.error(f"Error matching face: {str(e)}")
            return False, 1.0
    
    def encoding_to_blob(self, encoding: np.ndarray) -> bytes:
        """
        Convert face encoding to blob for storage.
        
        Args:
            encoding: Face encoding as numpy array
            
        Returns:
            Encoding as bytes
        """
        return pickle.dumps(encoding)
    
    def blob_to_encoding(self, blob: bytes) -> Optional[np.ndarray]:
        """
        Convert blob to face encoding.
        
        Args:
            blob: Encoding as bytes
            
        Returns:
            Face encoding as numpy array or None if failed
        """
        try:
            return pickle.loads(blob)
        except Exception as e:
            self.logger.error(f"Error converting blob to encoding: {str(e)}")
            return None
    
    def get_face_landmarks(self, image: np.ndarray, face_location: Optional[Tuple[int, int, int, int]] = None) -> Optional[dict]:
        """
        Get facial landmarks for a face.
        
        Args:
            image: Input image
            face_location: Specific face location (optional)
            
        Returns:
            Dictionary of facial landmarks or None if failed
        """
        try:
            # Convert BGR to RGB if needed
            if len(image.shape) == 3 and image.shape[2] == 3:
                image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            else:
                image_rgb = image
            
            # Get face locations if not provided
            if face_location is None:
                face_locations = self.detect_faces(image)
                if not face_locations:
                    return None
                face_location = face_locations[0]
            
            # Get landmarks
            landmarks = face_recognition.face_landmarks(image_rgb, [face_location])
            
            if not landmarks:
                return None
            
            return landmarks[0]
            
        except Exception as e:
            self.logger.error(f"Error getting face landmarks: {str(e)}")
            return None
