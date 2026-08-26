@echo off
REM Deployment Script for Deepfake Detection System (Windows)
REM This script helps deploy the system to free cloud hosting services

echo 🚀 Starting Deployment Process for Deepfake Detection System
echo ==================================================

REM Check if git is initialized
if not exist ".git" (
    echo 📦 Initializing Git repository...
    git init
    git add .
    git commit -m "Initial commit - Deepfake detection with blockchain"
    echo ✅ Git repository initialized
) else (
    echo ✅ Git repository already exists
)

REM Check if remote is set
git remote get-url origin >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  Git remote not set. Please run:
    echo    git remote add origin https://github.com/YOUR_USERNAME/deepfake-detection.git
    echo    git push -u origin main
    echo.
    pause
)

REM Check environment variables
echo 🔧 Checking environment configuration...
if not exist "backend\.env" (
    echo ⚠️  backend\.env not found. Copying from .env.example...
    copy backend\.env.example backend\.env
    echo ⚠️  Please update backend\.env with your actual configuration:
    echo    - MongoDB connection string
    echo    - Blockchain contract address
    echo    - Private keys
    echo.
    pause
)

REM Verify project structure
echo 📁 Verifying project structure...
if not exist "backend" (
    echo ❌ Required directory backend not found!
    exit /b 1
)
if not exist "frontend" (
    echo ❌ Required directory frontend not found!
    exit /b 1
)
if not exist "contracts" (
    echo ❌ Required directory contracts not found!
    exit /b 1
)
echo ✅ Project structure verified

REM Check required files
echo 📄 Checking required files...
if not exist "backend\app.py" (
    echo ❌ Required file backend\app.py not found!
    exit /b 1
)
if not exist "backend\requirements.txt" (
    echo ❌ Required file backend\requirements.txt not found!
    exit /b 1
)
if not exist "frontend\index.html" (
    echo ❌ Required file frontend\index.html not found!
    exit /b 1
)
if not exist "contracts\AccessRecord.sol" (
    echo ❌ Required file contracts\AccessRecord.sol not found!
    exit /b 1
)
echo ✅ Required files verified

REM Frontend API URL check
echo 🌐 Checking frontend API configuration...
findstr /C:"https://deepfake-backend.onrender.com" frontend\index.html >nul
if %errorlevel% equ 0 (
    echo ⚠️  Frontend still has placeholder backend URL
    echo    Please update frontend\index.html with your actual Render backend URL
    echo.
    pause
)

echo.
echo ✅ Local deployment checks completed!
echo.
echo 📋 Next Steps:
echo 1. Push code to GitHub:
echo    git push -u origin main
echo.
echo 2. Deploy Backend to Render:
echo    - Go to https://render.com
echo    - Connect your GitHub repository
echo    - Create Web Service with:
echo      * Root Directory: backend
echo      * Runtime: Python 3
echo      * Build Command: pip install -r requirements.txt
echo      * Start Command: gunicorn app:app --host 0.0.0.0 --port %%PORT%%
echo.
echo 3. Deploy Frontend to Netlify:
echo    - Go to https://netlify.com
echo    - Connect your GitHub repository
echo    - Publish directory: frontend
echo.
echo 4. Update environment variables in Render dashboard
echo.
echo 5. Update frontend API URL in Netlify
echo.
echo 📚 For detailed instructions, see DEPLOYMENT_GUIDE.md
echo.
echo 🎉 Deployment script completed!
pause