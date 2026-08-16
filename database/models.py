"""
Database models for FaceSecure application.
Defines all MongoDB models using MongoEngine.
"""

from datetime import datetime
from mongoengine import Document, EmbeddedDocument, fields
from bson.binary import Binary


class LoginLog(EmbeddedDocument):
    """Login log embedded document for tracking user login/logout sessions."""
    
    login_time = fields.DateTimeField(default=datetime.utcnow, required=True)
    logout_time = fields.DateTimeField()
    status = fields.StringField(max_length=50, required=True)
    reason = fields.StringField(max_length=255)
    ip_address = fields.StringField(max_length=45)
    device_name = fields.StringField(max_length=100)
    
    def to_dict(self):
        """Convert login log to dictionary."""
        return {
            'login_time': self.login_time.isoformat() if self.login_time else None,
            'logout_time': self.logout_time.isoformat() if self.logout_time else None,
            'status': self.status,
            'reason': self.reason,
            'ip_address': self.ip_address,
            'device_name': self.device_name
        }


class AuthenticationLog(EmbeddedDocument):
    """Authentication log embedded document for tracking authentication events."""
    
    timestamp = fields.DateTimeField(default=datetime.utcnow, required=True)
    event = fields.StringField(max_length=50, required=True)
    details = fields.StringField()
    
    def to_dict(self):
        """Convert authentication log to dictionary."""
        return {
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'event': self.event,
            'details': self.details
        }


class User(Document):
    """User document for storing user information."""
    
    username = fields.StringField(max_length=80, required=True, unique=True)
    email = fields.StringField(max_length=120, required=True, unique=True)
    password_hash = fields.StringField(max_length=255, required=True)
    face_image = fields.BinaryField()
    face_encoding = fields.BinaryField()
    created_at = fields.DateTimeField(default=datetime.utcnow, required=True)
    last_login = fields.DateTimeField()
    status = fields.StringField(max_length=20, default='active', required=True)
    
    # Embedded documents
    login_logs = fields.ListField(fields.EmbeddedDocumentField(LoginLog))
    authentication_logs = fields.ListField(fields.EmbeddedDocumentField(AuthenticationLog))
    
    meta = {
        'collection': 'users',
        'indexes': [
            'username',
            'email',
            'created_at',
            'last_login',
            'status'
        ]
    }
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def to_dict(self):
        """Convert user to dictionary."""
        return {
            'id': str(self.id),
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'status': self.status
        }
