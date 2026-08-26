# Free Cloud Deployment Guide

Complete guide to host your Deepfake Detection System with Blockchain Integration online for FREE.

## 🏗️ Architecture Overview

```
Frontend (Netlify/Vercel) → Backend (Render/Railway) → MongoDB Atlas (Free) → Polygon Testnet (Free)
```

## 🚀 Recommended Free Hosting Services

| Component | Service | Free Tier Limits |
|-----------|---------|------------------|
| Frontend | Netlify | Unlimited bandwidth, 100GB build |
| Backend | Render | 750 hours/month, 0.1 CPU, 512MB RAM |
| Database | MongoDB Atlas | 512MB storage |
| Blockchain | Polygon Mumbai Testnet | Free test tokens |

## 📋 Prerequisites

1. **GitHub Account** - For code hosting and deployment
2. **Email Accounts** - For signing up to services
3. **Basic Git Knowledge** - For pushing code

## 🎯 Step-by-Step Deployment

### Step 1: Prepare Your Code for Deployment

#### 1.1 Update Project Structure

Create a proper production structure:

```bash
deepfake-main/
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   ├── blockchain_service.py
│   ├── utils.py
│   ├── file_monitor.py
│   └── .env.example
├── frontend/
│   ├── index.html
│   └── (other frontend files)
├── contracts/
│   └── AccessRecord.sol
└── README.md
```

#### 1.2 Move Backend Files

```bash
# Create backend directory if it doesn't exist
mkdir backend

# Move backend files
mv app.py blockchain_service.py utils.py file_monitor.py requirements.txt backend/
mv .env .env.example backend/
```

#### 1.3 Move Frontend Files

```bash
# Create frontend directory if it doesn't exist
mkdir frontend

# Move frontend files
mv templates/index.html frontend/
mv static frontend/
```

#### 1.4 Update Backend Import Paths

In `backend/app.py`, update imports:

```python
# Remove these lines (no longer needed)
# from flask import Flask, request, jsonify, render_template
# from flask_cors import CORS

# Add these imports
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
```

#### 1.5 Create Root Level Files

Create `requirements.txt` in root (empty for now) and update `README.md`.

### Step 2: Setup GitHub Repository

#### 2.1 Initialize Git

```bash
cd E:\deepfake-main
git init
git add .
git commit -m "Initial commit - Deepfake detection with blockchain"
```

#### 2.2 Create GitHub Repository

1. Go to [GitHub](https://github.com)
2. Click "New Repository"
3. Name it `deepfake-detection`
4. Make it Public
5. Don't initialize with README
6. Click "Create Repository"

#### 2.3 Push to GitHub

```bash
git remote add origin https://github.com/YOUR_USERNAME/deepfake-detection.git
git branch -M main
git push -u origin main
```

### Step 3: Setup MongoDB Atlas (Free Database)

#### 3.1 Create MongoDB Account

1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Sign up for free account
3. Verify email address

#### 3.2 Create Free Cluster

1. Click "Build a Database"
2. Choose "Free" tier (M0 Sandbox)
3. Select cloud provider (AWS) and region (closest to you)
4. Name cluster: `deepfake-cluster`
5. Click "Create"

#### 3.3 Setup Database User

1. Go to "Database Access" → "Add New Database User"
2. Username: `deepfake_user`
3. Password: Generate strong password (save it!)
4. Privileges: "Read and write to any database"
5. Click "Add User"

#### 3.4 Whitelist IP Address

1. Go to "Network Access" → "Add IP Address"
2. Choose "Allow Access from Anywhere" (0.0.0.0/0)
3. Click "Confirm"

#### 3.5 Get Connection String

1. Go to "Database" → Click "Connect"
2. Choose "Connect your application"
3. Select driver: Python, version: 3.6 or later
4. Copy the connection string

It should look like:
```
mongodb+srv://deepfake_user:PASSWORD@deepfake-cluster.xxxxx.mongodb.net/?retryWrites=true&w=majority
```

### Step 4: Setup Polygon Testnet (Free Blockchain)

#### 4.1 Get Testnet MATIC

1. Go to [Polygon Mumbai Faucet](https://faucet.polygon.technology/)
2. Connect your MetaMask wallet
3. Request test MATIC tokens

#### 4.2 Deploy Smart Contract to Mumbai

Use Remix IDE or Hardhat to deploy to Mumbai testnet.

**Using Remix:**

1. Go to [Remix IDE](https://remix.ethereum.org/)
2. Create new file `AccessRecord.sol`
3. Copy contract code from `contracts/AccessRecord.sol`
4. Compile the contract
5. Go to "Deploy" tab
6. Select "Injected Provider - MetaMask"
7. Switch MetaMask to Mumbai Testnet
8. Deploy contract
9. Save the contract address

#### 4.3 Get Contract ABI

1. In Remix, go to "Compile" tab
2. Click "Compilation Details"
3. Copy the ABI section
4. Save as JSON file

### Step 5: Deploy Backend to Render (Free)

#### 5.1 Create Render Account

1. Go to [Render](https://render.com)
2. Sign up with GitHub
3. Authorize Render to access your repositories

#### 5.2 Create Web Service

1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Select `deepfake-detection` repository
4. Configure service:
   - **Name**: `deepfake-backend`
   - **Root Directory**: `backend`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --host 0.0.0.0 --port $PORT`

#### 5.3 Add Environment Variables

In Render dashboard, add these environment variables:

```bash
# Flask Configuration
FLASK_ENV=production
SECRET_KEY=your_random_secret_key_here

# MongoDB Configuration
MONGODB_URI=mongodb+srv://deepfake_user:PASSWORD@deepfake-cluster.xxxxx.mongodb.net/?retryWrites=true&w=majority
MONGODB_DATABASE=deepfake_auth

# Blockchain Configuration
BLOCKCHAIN_ENABLED=true
BLOCKCHAIN_PROVIDER_URL=https://rpc-mumbai.maticvigil.com
BLOCKCHAIN_CONTRACT_ADDRESS=your_deployed_contract_address
BLOCKCHAIN_PRIVATE_KEY=your_testnet_private_key
BLOCKCHAIN_CHAIN_ID=80001
BLOCKCHAIN_CONTRACT_ABI_PATH=./contracts/AccessRecord.json

# Application Configuration
KNOWN_FACE=just.jpg
PRIVATE_FOLDER=/tmp/private_files
MATCH_THRESHOLD=0.60
AUTO_CLOSE_SECONDS=10
FILE_MONITORING_ENABLED=false

# User Configuration
USER_ID=your_email@example.com
```

#### 5.4 Deploy

Click "Create Web Service" and wait for deployment.

#### 5.5 Get Backend URL

After deployment, Render will provide a URL like:
```
https://deepfake-backend.onrender.com
```

### Step 6: Deploy Frontend to Netlify (Free)

#### 6.1 Create Netlify Account

1. Go to [Netlify](https://netlify.com)
2. Sign up with GitHub
3. Authorize Netlify to access your repositories

#### 6.2 Update Frontend API URL

In `frontend/index.html`, update the API endpoint:

```javascript
// Find this line in your JavaScript
const response = await fetch('/check_face', {

// Change to your Render backend URL
const response = await fetch('https://deepfake-backend.onrender.com/check_face', {
```

#### 6.3 Deploy to Netlify

1. In Netlify, click "Add new site" → "Import an existing project"
2. Select your GitHub repository
3. Configure build settings:
   - **Build command**: (leave empty)
   - **Publish directory**: `frontend`
4. Click "Deploy site"

#### 6.4 Get Frontend URL

Netlify will provide a URL like:
```
https://your-site-name.netlify.app
```

### Step 7: Configure CORS and Security

#### 7.1 Update Backend CORS

In `backend/app.py`, update CORS configuration:

```python
# Replace this line
CORS(app)

# With this (more specific)
CORS(app, resources={
    r"/*": {
        "origins": ["https://your-site-name.netlify.app"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})
```

#### 7.2 Update Blockchain Contract ABI

For Render deployment, you need to embed the ABI directly since you can't easily upload files:

1. Create `backend/contract_abi.py`:
```python
CONTRACT_ABI = [
    // Paste your contract ABI here as a Python list
]
```

2. Update `backend/blockchain_service.py` to import from this file instead of loading from JSON.

### Step 8: Handle File Storage

Since cloud platforms don't provide persistent local storage like your `E:\Justin` folder:

#### Option A: Use Cloud Storage (Recommended)

1. **Setup Cloudinary (Free Tier):**
   - Sign up at [Cloudinary](https://cloudinary.com)
   - Get API credentials
   - Store face images and files there

2. **Update your code to use Cloudinary SDK** for file operations.

#### Option B: Use Temporary Storage

For demo purposes, use `/tmp` directory and accept that files won't persist between deployments.

#### Option C: Use Supabase Storage (Free)

1. Sign up at [Supabase](https://supabase.com)
2. Create storage bucket
3. Use their SDK for file operations

### Step 9: Testing the Deployment

#### 9.1 Test Backend

```bash
# Test health endpoint
curl https://deepfake-backend.onrender.com/api/blockchain/status

# Test face recognition endpoint
curl -X POST https://deepfake-backend.onrender.com/check_face \
  -H "Content-Type: application/json" \
  -d '{"image": "base64_image_data"}'
```

#### 9.2 Test Frontend

1. Open your Netlify URL in browser
2. Allow camera access
3. Test face recognition
4. Check browser console for any errors

### Step 10: Monitor and Maintain

#### 10.1 Render Dashboard

- Monitor your service status
- Check logs for errors
- View deployment history

#### 10.2 MongoDB Atlas Dashboard

- Monitor database performance
- Check storage usage
- View query statistics

#### 10.3 Polygon Scan

- View your contract transactions
- Monitor gas usage
- Check contract status

## 🔧 Troubleshooting

### Common Issues and Solutions

**1. Backend Fails to Start**
- Check Render logs for specific errors
- Ensure all environment variables are set
- Verify requirements.txt has all dependencies

**2. CORS Errors**
- Update CORS origins in backend
- Ensure frontend URL is whitelisted
- Check browser console for specific CORS errors

**3. Blockchain Connection Issues**
- Verify RPC URL is correct
- Check testnet has gas tokens
- Ensure contract address is correct

**4. Database Connection Issues**
- Verify MongoDB connection string
- Check IP whitelist in Atlas
- Ensure database user has correct permissions

**5. Face Recognition Not Working**
- Ensure known face image is accessible
- Check file permissions
- Verify OpenCV and dlib are installed correctly

## 📊 Free Tier Limitations

### Render (Backend)
- 750 hours/month (sufficient for development)
- 0.1 CPU, 512MB RAM
- Spins down after 15 minutes inactivity
- Cold start takes ~30 seconds

### Netlify (Frontend)
- Unlimited bandwidth
- 100GB build minutes/month
- 300GB bandwidth/month

### MongoDB Atlas
- 512MB storage
- Shared RAM
- Good for development and small apps

### Polygon Mumbai
- Free test tokens
- Not real money
- Need to refill periodically

## 🚀 Production Upgrades

When you're ready for production:

1. **Upgrade Render Plans** - Better performance, no spin-down
2. **Use Polygon Mainnet** - Real blockchain transactions
3. **Upgrade MongoDB** - More storage and performance
4. **Add CDN** - Better frontend performance
5. **Implement Monitoring** - Error tracking, analytics
6. **Add Authentication** - User login system
7. **Use Proper File Storage** - AWS S3, Cloudinary, etc.

## 📝 Additional Resources

- [Render Documentation](https://render.com/docs)
- [Netlify Documentation](https://docs.netlify.com)
- [MongoDB Atlas Documentation](https://docs.atlas.mongodb.com)
- [Polygon Documentation](https://docs.polygon.technology)
- [Flask Deployment Guide](https://flask.palletsprojects.com/en/latest/deploying/)

## 🎉 You're Live!

Your deepfake detection system with blockchain integration is now hosted online for free!

**Access URLs:**
- Frontend: `https://your-site-name.netlify.app`
- Backend: `https://deepfake-backend.onrender.com`
- Database: MongoDB Atlas Dashboard
- Blockchain: Polygon Mumbai Testnet

Users can now access your face recognition system from anywhere in the world with immutable blockchain audit logs!