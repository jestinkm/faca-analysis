# Quick Start Guide

Get your Deepfake Detection System with Blockchain Integration running online in minutes!

## 🚀 Fast Track Deployment (15 minutes)

### Prerequisites
- GitHub account
- Basic web browser
- 15 minutes of time

### Step 1: Prepare Your Code (2 minutes)

**Windows:**
```bash
deploy.bat
```

**Mac/Linux:**
```bash
chmod +x deploy.sh
./deploy.sh
```

### Step 2: Setup Free Services (8 minutes)

#### 2.1 MongoDB Atlas (2 minutes)
1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) → Sign up free
2. Create free cluster (M0 Sandbox)
3. Create database user with password
4. Allow access from anywhere (0.0.0.0/0)
5. Copy connection string

#### 2.2 Polygon Testnet (3 minutes)
1. Install [MetaMask](https://metamask.io/)
2. Add Polygon Mumbai testnet
3. Get free MATIC from [faucet](https://faucet.polygon.technology/)
4. Deploy contract using [Remix](https://remix.ethereum.org/)
5. Copy contract address

#### 2.3 Update Configuration (3 minutes)
Edit `backend/.env`:
```bash
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/?retryWrites=true&w=majority
BLOCKCHAIN_CONTRACT_ADDRESS=0xYourContractAddress
BLOCKCHAIN_PRIVATE_KEY=your_private_key
```

### Step 3: Deploy to Cloud (5 minutes)

#### 3.1 GitHub (1 minute)
```bash
git remote add origin https://github.com/YOUR_USERNAME/deepfake-detection.git
git push -u origin main
```

#### 3.2 Render Backend (2 minutes)
1. Go to [Render](https://render.com) → Sign up with GitHub
2. "New+" → "Web Service" → Connect your repo
3. Settings:
   - Root Directory: `backend`
   - Runtime: Python 3
   - Build: `pip install -r requirements.txt`
   - Start: `gunicorn app:app --host 0.0.0.0 --port $PORT`
4. Add environment variables from your `.env`
5. Deploy → Wait for green checkmark

#### 3.3 Netlify Frontend (2 minutes)
1. Go to [Netlify](https://netlify.com) → Sign up with GitHub
2. "Add new site" → "Import existing project"
3. Settings:
   - Publish directory: `frontend`
   - Build command: (leave empty)
4. Deploy → Get your URL
5. Update `frontend/index.html` with your Render backend URL

### Step 4: Test It! (1 minute)

1. Open your Netlify URL
2. Allow camera access
3. Test face recognition
4. Check blockchain logs on PolygonScan

## 🎉 You're Live!

**Your URLs:**
- Frontend: `https://your-site.netlify.app`
- Backend: `https://your-backend.onrender.com`
- Database: MongoDB Atlas Dashboard
- Blockchain: Polygon Mumbai Testnet

## 📚 Detailed Guides

Need more help? Check these comprehensive guides:

- **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** - Complete deployment instructions
- **[MONGODB_SETUP.md](MONGODB_SETUP.md)** - Database setup guide
- **[BLOCKCHAIN_TESTNET_SETUP.md](BLOCKCHAIN_TESTNET_SETUP.md)** - Blockchain configuration
- **[BLOCKCHAIN_SETUP.md](BLOCKCHAIN_SETUP.md)** - Smart contract deployment

## 🔧 Common Issues

**Problem**: Backend won't start
- **Solution**: Check Render logs, verify environment variables

**Problem**: CORS errors
- **Solution**: Update CORS origins in `backend/app.py`

**Problem**: Blockchain connection fails
- **Solution**: Verify contract address and private key

**Problem**: Frontend can't connect to backend
- **Solution**: Update API URL in `frontend/index.html`

## 💡 Tips

1. **Start with blockchain disabled** to test basic functionality
2. **Use testnet first** before considering mainnet
3. **Monitor free tier limits** to avoid surprises
4. **Keep secrets secure** - never commit `.env` files
5. **Test locally** before deploying to cloud

## 🆘 Support

If you encounter issues:

1. Check the detailed guides above
2. Review service logs (Render, Netlify, MongoDB Atlas)
3. Verify environment variables are set correctly
4. Ensure all dependencies are installed

## 🚀 Going Further

Once your basic deployment works:

1. **Add user authentication** with MongoDB
2. **Implement deepfake detection** models
3. **Add file encryption** for sensitive data
4. **Upgrade to production** tiers when needed
5. **Monitor performance** and optimize

Happy deploying! 🎊