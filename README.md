# FaceSecure - AI-Powered Continuous Face Authentication System

A production-quality full-stack web application that provides continuous AI-based face authentication. The system works entirely offline, uses a local webcam, and stores all user data in a MongoDB database.

## Features

- **Face Recognition**: Advanced AI-powered face recognition using deep learning algorithms
- **Liveness Detection**: Blink detection, head pose analysis, and anti-spoofing measures
- **Continuous Authentication**: Real-time continuous verification ensures the authenticated user remains present
- **100% Offline**: No cloud services or paid APIs required
- **Secure Storage**: All data stored in MongoDB database with face images as Binary data
- **Modern UI**: Beautiful dark theme with Bootstrap 5 and responsive design
- **Comprehensive Logging**: All authentication events logged for auditing

## Technology Stack

### Backend
- Python 3.12+
- Flask
- MongoDB
- MongoEngine (ODM)

### AI & Computer Vision
- OpenCV
- face_recognition (dlib)
- MediaPipe Face Mesh
- NumPy

### Frontend
- HTML5
- CSS3
- JavaScript
- Bootstrap 5

### Security
- Cryptography
- Werkzeug Password Hashing
- Flask Session

## Installation

### Prerequisites

1. **Python 3.12+**: Ensure Python 3.12 or higher is installed
2. **MongoDB**: Install and run MongoDB locally (default: localhost:27017)
3. **CMake**: Required for dlib installation
4. **Visual Studio Build Tools**: Required on Windows for dlib compilation

### MongoDB Setup

**Windows:**
```bash
# Download MongoDB Community Server from https://www.mongodb.com/try/download/community
# Install and start MongoDB service
# Default connection: mongodb://localhost:27017
```

**Linux:**
```bash
sudo apt-get install mongodb
sudo systemctl start mongodb
sudo systemctl enable mongodb
```

**macOS:**
```bash
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb-community
```

### Windows Setup

```bash
# Install CMake
# Download from https://cmake.org/download/

# Install Visual Studio Build Tools
# Download from https://visualstudio.microsoft.com/downloads/
# Select "Desktop development with C++" during installation
```

### Linux Setup

```bash
# Install build dependencies
sudo apt-get update
sudo apt-get install build-essential cmake
sudo apt-get install libopenblas-dev liblapack-dev
sudo apt-get install libx11-dev libgtk-3-dev
sudo apt-get install python3-dev python3-pip
```

### Install Python Dependencies

```bash
# Clone the repository
cd FaceSecure

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Running the Application

**Simplified Version (Recommended for Testing):**
```bash
# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Run the simplified application
python app_simple.py
```

**Full Version (With UI):**
```bash
# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Run the full application
python app.py
```

The application will start on `http://localhost:5000`

### First Time Setup

1. Open `http://localhost:5000` in your browser
2. Click "Register" to create a new account
3. Fill in username, email, and password
4. Allow camera access when prompted
5. Position your face in the frame and capture multiple images
6. Complete registration

### Login Process

1. Navigate to the login page
2. Enter your username and password
3. Allow camera access
4. Complete face verification with liveness check:
   - Blink naturally
   - Move your head left, right, up, and down
5. Access the dashboard upon successful authentication

### Continuous Authentication

1. After login, click "Start Continuous Auth" on the dashboard
2. The system will verify your presence every 2 seconds
3. If you leave, another person appears, or liveness fails, the session locks
4. View authentication status and logs in real-time

## Project Structure

```
FaceSecure/
│
├── app.py                      # Main Flask application
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
├── README.md                   # This file
│
├── database/
│   ├── database.py             # MongoDB initialization
│   └── models.py               # MongoEngine models
│
├── authentication/
│   ├── register.py             # Registration handler
│   ├── login.py                # Login handler
│   ├── verify.py               # Face verification handler
│   ├── continuous_auth.py      # Continuous authentication
│   ├── session_manager.py      # Session management
│   └── lock_screen.py          # Lock screen handler
│
├── camera/
│   └── webcam.py               # Webcam operations
│
├── services/
│   ├── face_service.py         # Face recognition service
│   ├── liveness_service.py     # Liveness detection service
│   ├── auth_service.py         # Authentication service
│   └── logger_service.py       # Logging service
│
├── utils/
│   ├── helper.py               # Helper functions
│   ├── constants.py            # Constants and enums
│   └── logger.py               # Logger configuration
│
├── static/
│   ├── css/
│   │   └── style.css           # Custom styles
│   ├── js/
│   │   ├── camera.js           # Camera utilities
│   │   └── auth.js             # Authentication utilities
│   ├── images/                 # Static images
│   └── uploads/                # User uploads
│
├── templates/
│   ├── base.html               # Base template
│   ├── index.html              # Home page
│   ├── register.html           # Registration page
│   ├── login.html              # Login page
│   ├── dashboard.html          # Dashboard
│   ├── profile.html            # Profile page
│   └── lockscreen.html         # Lock screen
│
└── logs/
    └── facesecure.log          # Application logs
```

## Database Schema

### Users Collection (MongoDB)
- `_id` - MongoDB ObjectId (primary key)
- `username` - Unique username (indexed)
- `email` - Unique email (indexed)
- `password_hash` - Hashed password
- `face_image` - Face image as Binary data
- `face_encoding` - Face encoding as Binary data
- `created_at` - Registration timestamp
- `last_login` - Last login timestamp
- `status` - User status (active/inactive/locked)
- `login_logs` - Embedded array of login log documents
- `authentication_logs` - Embedded array of authentication log documents

### Login Logs (Embedded in Users)
- `login_time` - Login timestamp
- `logout_time` - Logout timestamp
- `status` - Session status
- `reason` - Lock/completion reason
- `ip_address` - Client IP address
- `device_name` - Client device name

### Authentication Logs (Embedded in Users)
- `timestamp` - Event timestamp
- `event` - Event type (LOGIN_SUCCESS, LOGIN_FAILED, etc.)
- `details` - Additional event details

## Authentication Events

- `LOGIN_SUCCESS` - Successful login
- `LOGIN_FAILED` - Failed login attempt
- `FACE_NOT_FOUND` - No face detected
- `UNKNOWN_FACE` - Unknown face detected
- `PHOTO_ATTACK` - Photo attack detected
- `LIVENESS_FAILED` - Liveness check failed
- `SESSION_LOCKED` - Session locked
- `SESSION_EXPIRED` - Session expired
- `LOGOUT` - User logout

## Security Features

- **Password Hashing**: Uses Werkzeug's secure password hashing
- **NoSQL Injection Prevention**: MongoEngine ODM with parameterized queries
- **Session Security**: Secure Flask sessions with expiration
- **Face Encoding Storage**: Face encodings stored as binary data
- **Liveness Detection**: Multiple anti-spoofing measures
- **Comprehensive Logging**: All security events logged

## Configuration

Edit `config.py` to customize:

```python
# MongoDB configuration
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
MONGODB_DATABASE = 'facesecure'
MONGODB_URI = f"mongodb://{MONGODB_HOST}:{MONGODB_PORT}/{MONGODB_DATABASE}"

# Security
SECRET_KEY = 'your-secret-key-here'
PERMANENT_SESSION_LIFETIME = 1800  # 30 minutes

# Face recognition
FACE_MATCH_THRESHOLD = 0.6  # Lower is more strict
FACE_DETECTION_MODEL = 'hog'  # 'hog' or 'cnn'

# Liveness detection
BLINK_THRESHOLD = 0.25
BLINK_CONSECUTIVE_FRAMES = 3
HEAD_POSE_THRESHOLD = 0.5

# Continuous authentication
CONTINUOUS_AUTH_INTERVAL = 2  # seconds
MAX_FAILED_ATTEMPTS = 3
```

### Environment Variables

You can also use environment variables:

```bash
# Windows
set MONGODB_HOST=localhost
set MONGODB_PORT=27017
set MONGODB_DATABASE=facesecure
set SECRET_KEY=your-secret-key

# Linux/Mac
export MONGODB_HOST=localhost
export MONGODB_PORT=27017
export MONGODB_DATABASE=facesecure
export SECRET_KEY=your-secret-key
```

## Troubleshooting

### MongoDB Connection Issues

**MongoDB not running:**
```bash
# Windows
# Start MongoDB service
net start MongoDB

# Linux
sudo systemctl start mongodb

# macOS
brew services start mongodb-community
```

**Connection refused:**
- Ensure MongoDB is running on the configured host and port
- Check firewall settings
- Verify MongoDB configuration allows local connections

### dlib Installation Issues

**Windows:**
```bash
# Install Visual Studio Build Tools with C++ support
# Install CMake
pip install cmake
pip install dlib
```

**Linux:**
```bash
sudo apt-get install build-essential cmake
sudo apt-get install libopenblas-dev liblapack-dev
pip install dlib
```

### Camera Access Issues

- Ensure no other application is using the camera
- Check browser permissions for camera access
- Try using a different browser (Chrome/Firefox recommended)
- On Windows, ensure camera drivers are installed

### Face Recognition Performance

- Use `hog` model for faster detection (default)
- Use `cnn` model for better accuracy (slower)
- Ensure good lighting conditions
- Position face clearly in the frame

## Development

### Running in Debug Mode

```bash
python app.py
```

Debug mode is enabled by default. Disable in production:

```python
# In app.py
app.run(debug=False, host='0.0.0.0', port=5000)
```

### Database Reset

```python
# In Python shell
from database.database import reset_database
reset_database()
```

## License

This project is for educational purposes. Use responsibly and in compliance with privacy laws and regulations.

## Contributing

This is a demonstration project for educational purposes. Feel free to fork and modify for your needs.

## Acknowledgments

- face_recognition library by Adam Geitgey
- dlib by Davis King
- OpenCV by Intel
- Flask by Pallets Projects
- Bootstrap by The Bootstrap Authors

## Disclaimer

This system is for educational and demonstration purposes. For production use, additional security measures, testing, and compliance with privacy regulations (GDPR, CCPA, etc.) are required.
#   f a c e - a n a l y s i s  
 