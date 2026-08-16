"""
MongoDB connection module for FaceSecure application.
"""

from pymongo import MongoClient
from config import MONGO_URI, MONGO_DATABASE

# MongoDB connection
client = MongoClient(MONGO_URI)

# Database and collections
db = client[MONGO_DATABASE]
users = db["users"]

print("MongoDB Connected")

