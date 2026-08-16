# 🔐 FaceSecure – AI-Powered Continuous Face Authentication System

FaceSecure is a production-quality full-stack web application that provides **continuous AI-based face authentication and liveness detection**.

The system uses a local webcam for real-time facial verification and stores user authentication data securely in a **MongoDB database**. It is designed to operate **100% offline**, without requiring cloud-based AI services or paid APIs.

---

## ✨ Features

### 👤 Face Recognition

* AI-powered facial recognition
* Real-time face detection using a webcam
* Face encoding comparison for authentication
* Unknown-face detection
* Configurable face matching threshold
* Supports HOG and CNN face detection models

### 🛡️ Liveness Detection

FaceSecure uses multiple liveness verification techniques:

* 👁️ Blink detection
* ↔️ Head-pose analysis
* 🧑 Face-presence verification
* 🚫 Photo-attack detection
* Anti-spoofing checks

The login process requires the user to blink naturally and move their head in different directions before authentication is completed.

### 🔄 Continuous Authentication

After successful login, FaceSecure can continuously verify that the authenticated user remains in front of the camera.

* Real-time authentication
* Verification every 2 seconds
* Detects when the user leaves
* Detects when another person appears
* Detects failed liveness verification
* Automatically locks the session when verification fails

### 🔒 Secure Storage

User information is stored in MongoDB.

Stored information includes:

* Username
* Email
* Password hash
* Face image
* Face encoding
* Login history
* Authentication events
* Account status

### 📴 100% Offline

FaceSecure is designed to operate locally.

* No cloud AI services
* No paid APIs
* Local webcam processing
* Local MongoDB database
* Local Flask backend

### 🎨 Modern UI

The application provides a responsive interface using:

* HTML5
* CSS3
* JavaScript
* Bootstrap 5
* Dark cybersecurity-style interface
* Responsive authentication screens
* Animated face-scanning interface

### 📊 Comprehensive Logging

Authentication events are recorded for auditing and monitoring.

Supported events include:

* `LOGIN_SUCCESS`
* `LOGIN_FAILED`
* `FACE_NOT_FOUND`
* `UNKNOWN_FACE`
* `PHOTO_ATTACK`
* `LIVENESS_FAILED`
* `SESSION_LOCKED`
* `SESSION_EXPIRED`
* `LOGOUT`

---

# 🎬 Authentication Animation Flow

FaceSecure can use animated UI feedback during the authentication process.

## 1. Face Scan Animation

When the webcam detects a face:

```text
┌──────────────────────────────┐
│                              │
│        ╭──────────╮          │
│        │   FACE   │          │
│        │   ◀──    │          │
│        ╰──────────╯          │
│          ────────             │
│       Scanning Face...        │
│                              │
└──────────────────────────────┘
```

Recommended animation:

* Moving scan line
* Face-frame glow
* Circular scanning indicator
* `Scanning Face...` status

---

## 2. Blink Detection Animation

During liveness verification:

```text
👁️  Please Blink

Detecting blink...
```

After successful detection:

```text
✓ Blink Detected
```

The UI should visually indicate that the blink has been successfully detected.

---

## 3. Head Pose Animation

The application can display directional instructions:

```text
          ↑
          │
     ←   FACE   →
          │
          ↓
```

Instructions:

```text
Move your head LEFT
Move your head RIGHT
Move your head UP
Move your head DOWN
```

The project uses head movement as part of its liveness verification process.

---

## 4. Authentication Success Animation

After successful verification:

```text
        ✓
   Face Verified

 Authentication
    Successful
```

Recommended animation:

* Circular checkmark
* Smooth scale-in effect
* Green success indicator
* Automatic transition to dashboard

---

## 5. Authentication Failure Animation

If verification fails:

```text
        ✕
 Face Not Recognized

 Please try again
```

Recommended animation:

* Red face frame
* Short shake animation
* Error icon
* Clear retry message

Possible failure states:

```text
Face Not Found
Unknown Face
Liveness Failed
Photo Attack Detected
```

---

## 6. Continuous Authentication Animation

When continuous authentication is enabled:

```text
       ╭─────────╮
       │  FACE   │
       ╰─────────╯
          ◉
   Authentication Active
```

Recommended animation:

* Pulsing circular indicator
* Continuous scanning effect
* Authentication status indicator
* Real-time verification status

The system verifies the user's presence every **2 seconds**.

---

## 7. Session Lock Animation

If the authenticated user leaves or verification fails:

```text
        🔒

   SESSION LOCKED

 Face verification failed
```

Recommended animation:

* Screen blur/fade
* Lock icon animation
* Red warning indicator
* Return-to-login button

---

# 🧠 Technology Stack

## Backend

* Python 3.12+
* Flask
* MongoDB
* MongoEngine

## AI & Computer Vision

* OpenCV
* face_recognition
* dlib
* MediaPipe Face Mesh
* NumPy

## Frontend

* HTML5
* CSS3
* JavaScript
* Bootstrap 5

## Security

* Cryptography
* Werkzeug Password Hashing
* Flask Session

---

# 🏗️ System Architecture

```text
                    ┌─────────────────────┐
                    │       USER          │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Web Interface    │
                    │ HTML / CSS / JS      │
                    │ Bootstrap 5          │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Flask Backend    │
                    └──────────┬──────────┘
                               │
             ┌─────────────────┼─────────────────┐
             │                 │                 │
             ▼                 ▼                 ▼
       ┌───────────┐    ┌────────────┐    ┌────────────┐
       │   Face    │    │  Liveness  │    │   Session  │
       │Recognition│    │ Detection  │    │ Management │
       └─────┬─────┘    └──────┬─────┘    └──────┬─────┘
             │                 │                 │
             └─────────────────┼─────────────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      MongoDB        │
                    │ Users & Auth Logs   │
                    └─────────────────────┘
```

---

# 📁 Project Structure

```text
FaceSecure/
│
├── app.py
├── config.py
├── requirements.txt
├── README.md
│
├── database/
│   ├── database.py
│   └── models.py
│
├── authentication/
│   ├── register.py
│   ├── login.py
│   ├── verify.py
│   ├── continuous_auth.py
│   ├── session_manager.py
│   └── lock_screen.py
│
├── camera/
│   └── webcam.py
│
├── services/
│   ├── face_service.py
│   ├── liveness_service.py
│   ├── auth_service.py
│   └── logger_service.py
│
├── utils/
│   ├── helper.py
│   ├── constants.py
│   └── logger.py
│
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   ├── camera.js
│   │   └── auth.js
│   ├── images/
│   └── uploads/
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── register.html
│   ├── login.html
│   ├── dashboard.html
│   ├── profile.html
│   └── lockscreen.html
│
└── logs/
    └── facesecure.log
```

---

# ⚙️ Prerequisites

Before installing FaceSecure, make sure the following are installed.

### Required Software

1. Python 3.12+
2. MongoDB
3. CMake
4. Visual Studio Build Tools on Windows
5. Webcam

### Windows

Visual Studio Build Tools must include:

```text
Desktop development with C++
```

CMake is required for building dlib.

---

# 🗄️ MongoDB Setup

FaceSecure uses MongoDB as its local database.

Default configuration:

```text
Host: localhost
Port: 27017
Database: facesecure
```

MongoDB connection:

```text
mongodb://localhost:27017/facesecure
```

---

# 📦 Installation

## 1. Clone the Repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd FaceSecure
```

## 2. Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python -m venv venv
source venv/bin/activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Running the Application

## Simplified Version

Recommended for initial testing:

```bash
python app_simple.py
```

## Full Version

For the complete UI:

```bash
python app.py
```

The application will be available at:

```text
http://localhost:5000
```

---

# 📝 Registration Process

Open:

```text
http://localhost:5000
```

Then:

1. Click **Register**
2. Enter username
3. Enter email
4. Enter password
5. Allow webcam access
6. Position your face inside the camera frame
7. Capture the required face images
8. Complete registration

The face information is stored in MongoDB.

---

# 🔑 Login Process

The login process consists of multiple verification stages.

```text
Username
   ↓
Password
   ↓
Camera Access
   ↓
Face Detection
   ↓
Face Recognition
   ↓
Blink Detection
   ↓
Head Pose Verification
   ↓
Authentication Success
   ↓
Dashboard
```

The user must:

1. Enter username
2. Enter password
3. Allow camera access
4. Position their face in the camera
5. Blink naturally
6. Move their head left/right/up/down
7. Complete face verification

After successful verification, the user is redirected to the dashboard.

---

# 🔄 Continuous Authentication

After login:

```text
Dashboard
    ↓
Start Continuous Auth
    ↓
Webcam Monitoring
    ↓
Face Verification
    ↓
Liveness Verification
    ↓
User Present?
   ┌───────┴───────┐
  YES              NO
   │                │
   ▼                ▼
Continue        Lock Session
```

The system performs verification every:

```text
2 seconds
```

If:

* The user leaves
* Another person appears
* The face cannot be recognized
* Liveness verification fails

the session can be locked.

---

# 🗃️ Database Schema

## Users Collection

```text
_id
username
email
password_hash
face_image
face_encoding
created_at
last_login
status
login_logs
authentication_logs
```

### User Fields

| Field                 | Description                      |
| --------------------- | -------------------------------- |
| `_id`                 | MongoDB ObjectId                 |
| `username`            | Unique username                  |
| `email`               | Unique email                     |
| `password_hash`       | Hashed password                  |
| `face_image`          | Face image stored as binary data |
| `face_encoding`       | Face encoding                    |
| `created_at`          | Registration timestamp           |
| `last_login`          | Last login timestamp             |
| `status`              | Account status                   |
| `login_logs`          | Login history                    |
| `authentication_logs` | Authentication events            |

---

# 📋 Login Logs

Each login session can contain:

```text
login_time
logout_time
status
reason
ip_address
device_name
```

---

# 📊 Authentication Logs

Authentication events contain:

```text
timestamp
event
details
```

---

# 🚨 Authentication Events

FaceSecure supports the following authentication events:

| Event             | Meaning                      |
| ----------------- | ---------------------------- |
| `LOGIN_SUCCESS`   | Successful login             |
| `LOGIN_FAILED`    | Failed login                 |
| `FACE_NOT_FOUND`  | No face detected             |
| `UNKNOWN_FACE`    | Unknown face detected        |
| `PHOTO_ATTACK`    | Possible photo attack        |
| `LIVENESS_FAILED` | Liveness verification failed |
| `SESSION_LOCKED`  | Session locked               |
| `SESSION_EXPIRED` | Session expired              |
| `LOGOUT`          | User logged out              |

---

# 🔐 Security Features

## Password Hashing

Passwords are stored using secure password hashing rather than plain text.

## NoSQL Injection Prevention

MongoEngine is used for database interaction and parameterized queries.

## Session Security

Flask sessions are used with session expiration.

Default session lifetime:

```text
1800 seconds
```

or:

```text
30 minutes
```

## Face Encoding Storage

Face encodings are stored as binary data.

## Liveness Detection

Multiple liveness mechanisms are used to reduce spoofing attempts.

## Authentication Logging

Security events are recorded for auditing.

---

# ⚙️ Configuration

Edit:

```text
config.py
```

Example configuration:

```python
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
MONGODB_DATABASE = 'facesecure'

MONGODB_URI = (
    f"mongodb://{MONGODB_HOST}:"
    f"{MONGODB_PORT}/{MONGODB_DATABASE}"
)

SECRET_KEY = 'your-secret-key-here'

PERMANENT_SESSION_LIFETIME = 1800

FACE_MATCH_THRESHOLD = 0.6

FACE_DETECTION_MODEL = 'hog'

BLINK_THRESHOLD = 0.25

BLINK_CONSECUTIVE_FRAMES = 3

HEAD_POSE_THRESHOLD = 0.5

CONTINUOUS_AUTH_INTERVAL = 2

MAX_FAILED_ATTEMPTS = 3
```

---

# 🌐 Environment Variables

Instead of placing configuration directly inside the application, environment variables can be used.

### Windows

```bash
set MONGODB_HOST=localhost
set MONGODB_PORT=27017
set MONGODB_DATABASE=facesecure
set SECRET_KEY=your-secret-key
```

### Linux / macOS

```bash
export MONGODB_HOST=localhost
export MONGODB_PORT=27017
export MONGODB_DATABASE=facesecure
export SECRET_KEY=your-secret-key
```

---

# 🧠 Face Recognition Models

FaceSecure supports:

### HOG

```text
FACE_DETECTION_MODEL = 'hog'
```

Advantages:

* Faster
* Lower computational requirements
* Suitable for normal real-time usage

### CNN

```text
FACE_DETECTION_MODEL = 'cnn'
```

Advantages:

* Better detection accuracy
* More computationally expensive
* Slower than HOG

For better performance, use good lighting and position the face clearly inside the camera frame.

---

# 🎨 UI/UX Design

The FaceSecure interface should follow a modern cybersecurity theme.

### Recommended Design

```text
Dark Background
      +
Glowing Face Scanner
      +
Animated Authentication Status
      +
Blue/White Security Elements
      +
Green Success
      +
Red Failure
```

### Main Screens

```text
Home
 │
 ├── Register
 │
 ├── Login
 │
 ├── Dashboard
 │
 ├── Profile
 │
 └── Lock Screen
```

---

# 🎞️ Recommended UI Animations

| Screen          | Animation                |
| --------------- | ------------------------ |
| Login           | Face scanning animation  |
| Registration    | Camera capture animation |
| Face Detection  | Scanning line            |
| Blink Detection | Eye animation            |
| Head Pose       | Directional arrows       |
| Face Verified   | Animated checkmark       |
| Failed Login    | Shake/error animation    |
| Continuous Auth | Pulsing scanner          |
| Session Locked  | Lock/fade animation      |

---

# 🛠️ Troubleshooting

## MongoDB Connection Error

Make sure MongoDB is running.

### Windows

```bash
net start MongoDB
```

### Linux

```bash
sudo systemctl start mongodb
```

### macOS

```bash
brew services start mongodb-community
```

---

# 📷 Camera Access Problems

If the webcam does not work:

* Make sure no other application is using the camera
* Check browser camera permissions
* Try Chrome or Firefox
* Check Windows camera permissions
* Verify that webcam drivers are installed

---

# 🧩 dlib Installation Problems

### Windows

Install:

```text
Visual Studio Build Tools
CMake
```

Make sure C++ development support is enabled.

Then:

```bash
pip install cmake
pip install dlib
```

### Linux

```bash
sudo apt-get install build-essential cmake
sudo apt-get install libopenblas-dev liblapack-dev
pip install dlib
```

---

# ⚡ Face Recognition Performance

For faster face detection:

```text
HOG
```

For better accuracy:

```text
CNN
```

Additional recommendations:

* Use good lighting
* Keep your face clearly visible
* Avoid excessive movement
* Position the face in the center of the camera
* Ensure the webcam has sufficient resolution

---

# 🐞 Debug Mode

Run:

```bash
python app.py
```

For production, disable Flask debug mode:

```python
app.run(
    debug=False,
    host='0.0.0.0',
    port=5000
)
```

---

# 🗑️ Database Reset

The database can be reset using:

```python
from database.database import reset_database

reset_database()
```

⚠️ This operation should be used carefully because it can remove stored application data.

---

# 🔒 Security Considerations

FaceSecure is designed as an educational and demonstration project.

For a real production deployment, consider adding:

* Stronger anti-spoofing models
* Secure HTTPS deployment
* Hardware-backed key storage
* Rate limiting
* Multi-factor authentication
* Secure secret management
* Database encryption
* Advanced audit logging
* Privacy controls
* Data retention policies
* User consent management
* Regulatory compliance

---

# 🔏 Privacy

FaceSecure processes biometric information such as facial images and face encodings.

Any real-world deployment should:

* Obtain appropriate user consent
* Protect stored biometric information
* Limit access to biometric data
* Define data retention policies
* Provide appropriate deletion mechanisms
* Follow applicable privacy and data-protection regulations

---

# 📈 Future Enhancements

Possible future improvements include:

* AI-based advanced anti-spoofing
* Emotion detection
* Multi-face monitoring
* Mobile application
* Admin dashboard
* Real-time security alerts
* Email notifications
* Advanced authentication analytics
* Role-based access control
* Hardware security integration
* Improved deepfake detection
* WebSocket-based real-time authentication
* More advanced continuous authentication models

---

# 🧪 Development Workflow

```text
User
 │
 ▼
Webcam
 │
 ▼
Face Detection
 │
 ▼
Face Recognition
 │
 ▼
Liveness Detection
 │
 ▼
Authentication
 │
 ├───────────────┐
 ▼               ▼
Success         Failure
 │               │
 ▼               ▼
Dashboard     Lock Screen
 │
 ▼
Continuous Authentication
 │
 ▼
Authentication Logs
```

---

# 📦 Main Dependencies

The project uses technologies including:

```text
Flask
MongoDB
MongoEngine
OpenCV
face_recognition
dlib
MediaPipe
NumPy
Bootstrap
Werkzeug
Cryptography
```

Install dependencies with:

```bash
pip install -r requirements.txt
```

---

# 📚 Acknowledgments

This project uses and builds upon:

* `face_recognition` library by Adam Geitgey
* dlib by Davis King
* OpenCV
* Flask by Pallets Projects
* Bootstrap by The Bootstrap Authors

---

# 📄 License

This project is intended for **educational and demonstration purposes**.

Use responsibly and in compliance with applicable privacy and data-protection requirements.

---

# ⚠️ Disclaimer

FaceSecure is an educational and demonstration system.

It should **not be considered a complete production-grade biometric security solution without additional security testing, privacy controls, anti-spoofing validation, and regulatory compliance work**.

---

# 👨‍💻 Project

## FaceSecure

**AI-Powered Continuous Face Authentication System**

```text
Face Recognition
       +
Liveness Detection
       +
Continuous Authentication
       +
Secure Session Management
       +
Authentication Logging
```

### Core Goal

> Provide continuous identity verification using local AI-based facial recognition and liveness detection while maintaining a secure, offline-first architecture.
