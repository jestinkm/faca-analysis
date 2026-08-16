"""
Database initialization and management for FaceSecure application.
"""

from flask import Flask
from mongoengine import connect, disconnect
from config import MONGODB_URI, MONGODB_DATABASE


def init_database(app: Flask):
    """
    Initialize MongoDB connection with Flask app.
    
    Args:
        app: Flask application instance
    """
    # Connect to MongoDB
    connect(host=MONGODB_URI, db=MONGODB_DATABASE, alias='default')
    
    # Ensure indexes are created
    from database.models import User
    User.ensure_indexes()


def create_tables():
    """Create all database indexes (MongoDB creates collections automatically)."""
    from database.models import User
    User.ensure_indexes()


def drop_tables():
    """Drop all database collections."""
    from database.models import User
    User.drop_collection()


def reset_database():
    """Reset database by dropping and recreating collections."""
    from database.models import User
    User.drop_collection()
    User.ensure_indexes()


def get_database():
    """Get MongoDB database instance."""
    from mongoengine.connection import get_db
    return get_db()
