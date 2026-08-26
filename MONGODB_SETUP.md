# MongoDB Atlas Setup Guide

This guide will help you set up a free MongoDB Atlas database for your deepfake detection system.

## 🚀 Quick Setup Steps

### 1. Create MongoDB Atlas Account

1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Click "Try Free" 
3. Sign up with email or Google/GitHub account
4. Verify your email address

### 2. Create Free Cluster

1. After login, click "Build a Database"
2. Select "Free" tier (M0 Sandbox - 512MB storage)
3. **Cloud Provider**: AWS (recommended)
4. **Region**: Choose region closest to your users
   - For Europe: Frankfurt (eu-central-1)
   - For Asia: Singapore (ap-southeast-1)
   - For US: North Virginia (us-east-1)
5. **Cluster Name**: `deepfake-cluster` (or your preferred name)
6. Click "Create Cluster"
7. Wait for cluster creation (2-5 minutes)

### 3. Create Database User

1. Go to "Database Access" in left sidebar
2. Click "Add New Database User"
3. **Authentication Method**: Choose "Password"
4. **Username**: `deepfake_user` (or your preferred username)
5. **Password**: Click "Autogenerate Secure Password" and SAVE IT
6. **Database User Privileges**: Select "Read and write to any database"
7. Click "Add User"

### 4. Configure Network Access

1. Go to "Network Access" in left sidebar
2. Click "Add IP Address"
3. Choose "Allow Access from Anywhere" (0.0.0.0/0)
   - This allows your Render backend to connect from any IP
4. Click "Confirm"

### 5. Get Connection String

1. Go to "Database" in left sidebar
2. Click "Connect" on your cluster
3. Choose "Connect your application"
4. **Driver**: Select "Python"
5. **Version**: Select "3.6 or later"
6. Copy the connection string

It will look like:
```
mongodb+srv://deepfake_user:<password>@deepfake-cluster.xxxxx.mongodb.net/?retryWrites=true&w=majority
```

### 6. Update Environment Variables

Replace `<password>` with your actual password and add to your `.env` file:

```bash
MONGODB_URI=mongodb+srv://deepfake_user:YOUR_ACTUAL_PASSWORD@deepfake-cluster.xxxxx.mongodb.net/?retryWrites=true&w=majority
MONGODB_DATABASE=deepfake_auth
```

### 7. Test Connection (Optional)

Create a test script to verify your connection:

```python
# test_mongodb.py
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv("MONGODB_URI"))
try:
    # Test connection
    client.admin.command('ping')
    print("✅ MongoDB connection successful!")
    
    # Test database access
    db = client[os.getenv("MONGODB_DATABASE")]
    print(f"✅ Database '{db.name}' accessible")
    
    # Create a test collection
    test_collection = db.test_collection
    test_collection.insert_one({"test": "connection"})
    print("✅ Write operation successful")
    
    # Clean up
    test_collection.delete_many({})
    print("✅ Cleanup successful")
    
except Exception as e:
    print(f"❌ Connection failed: {e}")
finally:
    client.close()
```

Run: `python test_mongodb.py`

## 🔧 Database Structure for Future User Authentication

When you implement user authentication, create these collections:

### Users Collection
```javascript
{
  "_id": ObjectId("..."),
  "email": "user@example.com",
  "password_hash": "hashed_password",
  "face_encoding": [encoding_array],
  "face_image_path": "encrypted_path_or_cloudinary_url",
  "created_at": ISODate("2026-08-24T10:00:00Z"),
  "last_login": ISODate("2026-08-24T12:00:00Z"),
  "is_active": true
}
```

### Access Logs Collection (Local Backup)
```javascript
{
  "_id": ObjectId("..."),
  "user_id": ObjectId("..."),
  "file_hash": "abc123...",
  "access_granted": true,
  "access_type": "LOGIN",
  "timestamp": ISODate("2026-08-24T12:00:00Z"),
  "blockchain_tx_hash": "0x123..."
}
```

### Files Collection
```javascript
{
  "_id": ObjectId("..."),
  "user_id": ObjectId("..."),
  "file_name": "document.pdf",
  "file_hash": "abc123...",
  "file_path": "encrypted_path",
  "blockchain_recorded": true,
  "created_at": ISODate("2026-08-24T10:00:00Z")
}
```

## 📊 Monitoring Your Database

### MongoDB Atlas Dashboard

1. **Metrics Tab**: Monitor performance, connections, storage
2. **Data Explorer**: View and edit your data
3. **Logs**: Check for connection issues and errors

### Free Tier Limits

- **Storage**: 512MB
- **RAM**: Shared
- **Connections**: Sufficient for development
- **Price**: Free forever

## 🔒 Security Best Practices

1. **Never commit passwords** to version control
2. **Use environment variables** for sensitive data
3. **Regular backups** are automatic on Atlas
4. **Monitor usage** to stay within free tier
5. **Update passwords** periodically

## 🚨 Troubleshooting

### Connection Issues

**Problem**: "Authentication failed"
- **Solution**: Verify username and password in connection string

**Problem**: "IP whitelist error"  
- **Solution**: Ensure 0.0.0.0/0 is whitelisted in Network Access

**Problem**: "Connection timeout"
- **Solution**: Check your internet connection and Atlas status

### Performance Issues

**Problem**: Slow queries
- **Solution**: Create indexes on frequently queried fields
- **Solution**: Optimize query structure

**Problem**: Storage full
- **Solution**: Clean up old test data
- **Solution**: Consider upgrading to paid tier

## 📈 Scaling Beyond Free Tier

When you need more resources:

1. **M20 Tier**: $9/month - 2GB storage, dedicated RAM
2. **M30 Tier**: $59/month - 8GB storage, better performance
3. **M40+ Tier**: For production workloads

Upgrade path: Clusters → Modify → Change Capacity

## 🔄 Backup and Restore

### Automatic Backups

MongoDB Atlas provides automatic backups for paid tiers. For free tier:

1. **Manual Export**:
```bash
mongodump --uri="mongodb+srv://user:pass@cluster.mongodb.net/dbname" --out=./backup
```

2. **Manual Import**:
```bash
mongorestore --uri="mongodb+srv://user:pass@cluster.mongodb.net/dbname" ./backup
```

## 🎯 Next Steps

1. ✅ MongoDB Atlas account created
2. ✅ Free cluster deployed  
3. ✅ Database user configured
4. ✅ Network access configured
5. ✅ Connection string obtained
6. ✅ Environment variables updated
7. ✅ Connection tested

Your MongoDB database is now ready for integration with your deepfake detection system!