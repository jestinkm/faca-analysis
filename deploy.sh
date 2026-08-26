#!/bin/bash

# Deployment Script for Deepfake Detection System
# This script helps deploy the system to free cloud hosting services

set -e

echo "🚀 Starting Deployment Process for Deepfake Detection System"
echo "=================================================="

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📦 Initializing Git repository..."
    git init
    git add .
    git commit -m "Initial commit - Deepfake detection with blockchain"
    echo "✅ Git repository initialized"
else
    echo "✅ Git repository already exists"
fi

# Check if remote is set
if ! git remote get-url origin > /dev/null 2>&1; then
    echo "⚠️  Git remote not set. Please run:"
    echo "   git remote add origin https://github.com/YOUR_USERNAME/deepfake-detection.git"
    echo "   git push -u origin main"
    echo ""
    read -p "Press Enter after setting up GitHub repository..."
fi

# Check environment variables
echo "🔧 Checking environment configuration..."
if [ ! -f "backend/.env" ]; then
    echo "⚠️  backend/.env not found. Copying from .env.example..."
    cp backend/.env.example backend/.env
    echo "⚠️  Please update backend/.env with your actual configuration:"
    echo "   - MongoDB connection string"
    echo "   - Blockchain contract address"
    echo "   - Private keys"
    echo ""
    read -p "Press Enter after updating .env file..."
fi

# Verify project structure
echo "📁 Verifying project structure..."
required_dirs=("backend" "frontend" "contracts")
for dir in "${required_dirs[@]}"; do
    if [ ! -d "$dir" ]; then
        echo "❌ Required directory $dir not found!"
        exit 1
    fi
done
echo "✅ Project structure verified"

# Check required files
echo "📄 Checking required files..."
required_files=("backend/app.py" "backend/requirements.txt" "frontend/index.html" "contracts/AccessRecord.sol")
for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ Required file $file not found!"
        exit 1
    fi
done
echo "✅ Required files verified"

# Frontend API URL check
echo "🌐 Checking frontend API configuration..."
if grep -q "https://deepfake-backend.onrender.com" frontend/index.html; then
    echo "⚠️  Frontend still has placeholder backend URL"
    echo "   Please update frontend/index.html with your actual Render backend URL"
    echo ""
    read -p "Press Enter after updating frontend API URL..."
fi

echo ""
echo "✅ Local deployment checks completed!"
echo ""
echo "📋 Next Steps:"
echo "1. Push code to GitHub:"
echo "   git push -u origin main"
echo ""
echo "2. Deploy Backend to Render:"
echo "   - Go to https://render.com"
echo "   - Connect your GitHub repository"
echo "   - Create Web Service with:"
echo "     * Root Directory: backend"
echo "     * Runtime: Python 3"
echo "     * Build Command: pip install -r requirements.txt"
echo "     * Start Command: gunicorn app:app --host 0.0.0.0 --port \$PORT"
echo ""
echo "3. Deploy Frontend to Netlify:"
echo "   - Go to https://netlify.com"
echo "   - Connect your GitHub repository"
echo "   - Publish directory: frontend"
echo ""
echo "4. Update environment variables in Render dashboard"
echo ""
echo "5. Update frontend API URL in Netlify"
echo ""
echo "📚 For detailed instructions, see DEPLOYMENT_GUIDE.md"
echo ""
echo "🎉 Deployment script completed!"