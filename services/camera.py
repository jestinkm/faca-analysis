"""
Camera module for FaceSecure application.
Handles camera operations and helper functions.
"""

import cv2
import numpy as np
from config import CAMERA_INDEX, FRAME_WIDTH, FRAME_HEIGHT, FPS


def open_camera():
    """
    Open camera with configured settings.
    
    Returns:
        cv2.VideoCapture object
    """
    camera = cv2.VideoCapture(CAMERA_INDEX)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
    camera.set(cv2.CAP_PROP_FPS, FPS)
    return camera


def read_frame(camera):
    """
    Read a single frame from camera.
    
    Args:
        camera: cv2.VideoCapture object
        
    Returns:
        Frame as numpy array or None if failed
    """
    ret, frame = camera.read()
    if ret:
        return frame
    return None


def close_camera(camera):
    """
    Close camera and release resources.
    
    Args:
        camera: cv2.VideoCapture object
    """
    camera.release()
    cv2.destroyAllWindows()


def convert_to_rgb(frame):
    """
    Convert BGR frame to RGB.
    
    Args:
        frame: BGR frame as numpy array
        
    Returns:
        RGB frame as numpy array
    """
    return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)


def display_frame(frame, window_name="Camera"):
    """
    Display frame in window.
    
    Args:
        frame: Frame as numpy array
        window_name: Name of the window
    """
    cv2.imshow(window_name, frame)
    cv2.waitKey(1)
