
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# MongoDB Configuration
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017')
MONGO_DATABASE = os.getenv('MONGO_DATABASE', 'FaceSecureDB')

# Flask Configuration
SECRET_KEY = os.getenv('SECRET_KEY', 'face-secure-secret-key-change-in-production')
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'

# Camera Configuration
CAMERA_INDEX = 0
FRAME_WIDTH = 1280
FRAME_HEIGHT = 720
FPS = 30

# Face Recognition Configuration
FACE_MATCH_THRESHOLD = 0.6
FACE_DETECTION_MODEL = 'cnn'
NUM_JITTERS = 1
UPSAMPLE_TIMES = 1

# Liveness Detection Configuration
BLINK_THRESHOLD = 0.21
BLINK_CONSECUTIVE_FRAMES = 3
REQUIRED_BLINKS = 2
