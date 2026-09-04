# Deepfake Detection System with Blockchain Integration

[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)
[![Blockchain](https://img.shields.io/badge/blockchain-Polygon_Mumbai-blue)](https://polygon.technology/)
[![Database](https://img.shields.io/badge/database-MongoDB_Atlas-green)](https://www.mongodb.com/cloud/atlas)

A comprehensive facial recognition system with blockchain-based immutable audit logs and file integrity verification.

---

## **Table of Contents**

1. [Project Overview](#project-overview)  
2. [Features](#features)  
3. [Architecture](#architecture)  
4. [Folder Structure](#folder-structure)  
5. [Quick Start](#quick-start)  
6. [Installation](#installation)  
7. [Deployment](#deployment)  
8. [Technologies Used](#technologies-used)  
9. [API Documentation](#api-documentation)  
10. [Future Enhancements](#future-enhancements)  
11. [License](#license)  

---

## **Project Overview**

This project is a **Deepfake/Facial Recognition secured file system** with blockchain integration that:  

- Detects faces in real-time using webcam input  
- Records all access attempts on blockchain for immutable audit logs  
- Provides file integrity verification against blockchain records  
- Detects file tampering with automatic blockchain alerts  
- Supports MongoDB for user authentication and data storage  

The system is split into:  

- **Frontend:** Static HTML/CSS/JS with real-time webcam capture  
- **Backend:** Flask API with face recognition and blockchain integration  
- **Blockchain:** Smart contract on Polygon testnet for access logging  
- **Database:** MongoDB Atlas for user data and local backup  

---

## **Features**

### Core Features
- Real-time face recognition using OpenCV & face_recognition  
- **Blockchain Integration**: Immutable access records on Polygon testnet  
- **File Integrity Verification**: SHA-256 hashing with blockchain verification  
- **Tampering Detection**: Automatic file monitoring with blockchain alerts  
- Smart contract for access record management  

### Security Features
- **Immutable Audit Logs**: All access attempts recorded on blockchain  
- **File Hash Verification**: Detect unauthorized file modifications  
- **User Authentication Ready**: MongoDB integration for user management  
- **Environment-based Configuration**: Secure credential management  

### Deployment Features
- **Free Cloud Hosting**: Netlify (frontend) + Render (backend)  
- **Free Database**: MongoDB Atlas (512MB tier)  
- **Free Blockchain**: Polygon Mumbai testnet  
- **Container-ready**: Procfile and runtime configuration included  

---

## **Architecture**

```
┌─────────────────┐
│   React/Web UI  │
│   (Netlify)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Flask / FastAPI │
│   (Render)      │
└────────┬────────┘
         │
    ┌────┼────┬──────────┐
    ▼    ▼    ▼          ▼
Face  Deepfake  MongoDB  Blockchain
Recog  Detection Atlas   Service
    │           │          │
    ▼           ▼          ▼
SHA-256 Hash  User Data  Smart Contract
    │                      │
    └──────────┬───────────┘
               ▼
       Polygon Mumbai Testnet
               │
               ▼
       Immutable Audit Log
```

---

## **Folder Structure**
deepfake-main/
│-- backend/               # Flask backend
│   |-- app.py            # Main Flask application
│   |-- blockchain_service.py  # Web3 integration
│   |-- utils.py          # File hashing and encryption
│   |-- file_monitor.py   # File integrity monitoring
│   |-- contract_abi.py   # Smart contract ABI
│   |-- requirements.txt  # Python dependencies
│   |-- Procfile          # Render deployment config
│   |-- runtime.txt       # Python version specification
│   |-- .env              # Environment variables (not in git)
│   └── .env.example      # Environment template
│-- frontend/             # Frontend UI
│   |-- index.html        # Main interface
│   └── static/           # CSS, JS, images
│-- contracts/            # Smart contracts
│   └── AccessRecord.sol  # Solidity contract
│-- DEPLOYMENT_GUIDE.md   # Complete deployment instructions
│-- MONGODB_SETUP.md      # Database setup guide
│-- BLOCKCHAIN_SETUP.md   # Blockchain setup guide
│-- BLOCKCHAIN_TESTNET_SETUP.md  # Testnet configuration
│-- QUICK_START.md        # Fast deployment guide
│-- deploy.sh / deploy.bat # Deployment scripts
│-- README.md             # This file
│-- .gitignore            # Git ignore rules


---

## **Quick Start**

Get the system running online in 15 minutes! See [QUICK_START.md](QUICK_START.md) for detailed instructions.

### Prerequisites
- GitHub account
- Basic web browser
- 15 minutes

### Fast Track
1. **Windows**: Run `deploy.bat`
2. **Mac/Linux**: Run `./deploy.sh`
3. Follow the prompts to set up free services
4. Deploy to Render (backend) and Netlify (frontend)

---

## **Installation (Local Setup)**

### 1. Clone the repository
```bash
git clone https://github.com/jestinkm/deepfake.git
cd deepfake-main
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```

### 3. Install dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 4. Configure environment variables
```bash
cp .env.example .env
# Edit .env with your configuration
```

### 5. Add known face image
Place your reference face image as `just.jpg` in the backend directory.

### 6. Run the Flask server
```bash
cd backend
python app.py
```

### 7. Test the application
Open your browser at: `http://127.0.0.1:5000/`

---

## **Deployment**

### Free Cloud Deployment

Complete deployment guide available in [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

#### Backend (Render)
- **Platform**: Render
- **Runtime**: Python 3
- **Build**: `pip install -r requirements.txt`
- **Start**: `gunicorn app:app --host 0.0.0.0 --port $PORT`

#### Frontend (Netlify)
- **Platform**: Netlify
- **Publish directory**: `frontend`
- **Build command**: (leave empty)

#### Database (MongoDB Atlas)
- **Platform**: MongoDB Atlas Free Tier
- **Setup**: See [MONGODB_SETUP.md](MONGODB_SETUP.md)

#### Blockchain (Polygon Mumbai)
- **Platform**: Polygon Mumbai Testnet
- **Setup**: See [BLOCKCHAIN_TESTNET_SETUP.md](BLOCKCHAIN_TESTNET_SETUP.md)

---

## **Technologies Used**

### Frontend
- HTML5, CSS3, JavaScript
- Real-time webcam capture
- AJAX for API communication

### Backend
- Python 3.9+
- Flask (Web Framework)
- Flask-CORS (Cross-origin support)
- Gunicorn (WSGI server)

### Face Recognition
- OpenCV (Computer Vision)
- face_recognition (Face detection)
- dlib (Machine learning)

### Blockchain
- Web3.py (Ethereum/Polygon interaction)
- Solidity (Smart contracts)
- Polygon Mumbai Testnet

### Security
- SHA-256 (File hashing)
- AES (File encryption)
- python-dotenv (Secret management)

### Database
- MongoDB Atlas (Free tier)
- PyMongo (MongoDB driver)

### Deployment
- Render (Backend hosting)
- Netlify (Frontend hosting)
- GitHub (Version control)

---

## **API Documentation**

### Face Recognition
- `POST /check_face` - Process face recognition frame
- `GET /` - API status and endpoints

### Blockchain Operations
- `GET /api/blockchain/status` - Check blockchain connection
- `GET /api/blockchain/user_history` - Get user access history
- `POST /api/blockchain/verify_file` - Verify file integrity
- `POST /api/blockchain/record_manual` - Manual access recording

### File Monitoring
- `GET /api/file_monitor/status` - Check monitoring status
- `POST /api/file_monitor/start` - Start file monitoring
- `POST /api/file_monitor/stop` - Stop file monitoring
- `POST /api/file_monitor/check` - Manual integrity check
- `GET /api/file_monitor/files` - List monitored files
- `POST /api/file_monitor/add` - Add file to monitoring

---

## **Future Enhancements**

- [ ] **User Authentication**: Complete MongoDB integration for user login
- [ ] **Deepfake Detection**: CNN/LSTM models for deepfake detection
- [ ] **File Encryption**: AES encryption for sensitive files
- [ ] **IPFS Integration**: Decentralized file storage
- [ ] **Multi-face Support**: Handle multiple users simultaneously
- [ ] **Liveness Detection**: Anti-spoofing measures
- [ ] **Admin Dashboard**: Web interface for system management
- [ ] **Mobile App**: React Native mobile application
- [ ] **Production Blockchain**: Polygon mainnet deployment
- [ ] **Real-time Alerts**: Email/SMS notifications for security events

---

## **License**

MIT License — see LICENSE

---

## **Contributing**

Contributions are welcome! Please feel free to submit a Pull Request.

---

## **Support**

For detailed setup and deployment instructions, see:
- [QUICK_START.md](QUICK_START.md) - Fast deployment
- [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - Complete deployment
- [MONGODB_SETUP.md](MONGODB_SETUP.md) - Database setup
- [BLOCKCHAIN_SETUP.md](BLOCKCHAIN_SETUP.md) - Smart contract deployment
- [BLOCKCHAIN_TESTNET_SETUP.md](BLOCKCHAIN_TESTNET_SETUP.md) - Testnet configuration



#   R e a l - T i m e - D e e p f a k e - D e t e c t i o n - U s i n g - D e e p - L e a r n i n g - f o r - S e c u r e - a n d - T r u s t w o r t h y - D i g i t a l - M e d i a  
 