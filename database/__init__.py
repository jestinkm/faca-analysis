from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

db = client["FaceSecureDB"]

users = db["users"]

print("Database initialized successfully!")
