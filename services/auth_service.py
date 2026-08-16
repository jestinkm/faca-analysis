"""
Authentication service for FaceSecure application.
Handles user authentication operations.
"""

from datetime import datetime
from typing import Tuple
from werkzeug.security import generate_password_hash, check_password_hash
from database.models import User, LoginLog, AuthenticationLog
from utils.constants import AUTH_EVENTS, USER_STATUS
from utils.logger import FaceSecureLogger


class AuthService:
    """Service for authentication operations."""
    
    def __init__(self):
        """Initialize auth service."""
        self.logger = FaceSecureLogger()
    
    def hash_password(self, password: str) -> str:
        """
        Hash a password.
        
        Args:
            password: Plain text password
            
        Returns:
            Hashed password
        """
        return generate_password_hash(password)
    
    def verify_password(self, password: str, password_hash: str) -> bool:
        """
        Verify a password against hash.
        
        Args:
            password: Plain text password
            password_hash: Hashed password
            
        Returns:
            True if password matches, False otherwise
        """
        return check_password_hash(password_hash, password)
    
    def create_user(self, username: str, email: str, password: str) -> User:
        """
        Create a new user.
        
        Args:
            username: Username
            email: Email address
            password: Plain text password
            
        Returns:
            Created user object
        """
        user = User(
            username=username,
            email=email,
            password_hash=self.hash_password(password),
            status=USER_STATUS['ACTIVE']
        )
        
        user.save()
        
        self.logger.log_authentication_event(
            str(user.id),
            AUTH_EVENTS['LOGIN_SUCCESS'],
            "User registered"
        )
        
        return user
    
    def get_user_by_username(self, username: str) -> User:
        """
        Get user by username.
        
        Args:
            username: Username
            
        Returns:
            User object or None
        """
        try:
            return User.objects(username=username).first()
        except:
            return None
    
    def get_user_by_id(self, user_id: str) -> User:
        """
        Get user by ID.
        
        Args:
            user_id: User ID (MongoDB ObjectId as string)
            
        Returns:
            User object or None
        """
        try:
            return User.objects(id=user_id).first()
        except:
            return None
    
    def update_user_face(self, user: User, face_image: bytes, face_encoding: bytes):
        """
        Update user face data.
        
        Args:
            user: User object
            face_image: Face image as blob
            face_encoding: Face encoding as blob
        """
        user.face_image = face_image
        user.face_encoding = face_encoding
        user.save()
        
        self.logger.log_authentication_event(
            str(user.id),
            AUTH_EVENTS['LOGIN_SUCCESS'],
            "Face registered"
        )
    
    def verify_credentials(self, username: str, password: str) -> Tuple[bool, User]:
        """
        Verify user credentials.
        
        Args:
            username: Username
            password: Plain text password
            
        Returns:
            Tuple of (is_valid, user)
        """
        user = self.get_user_by_username(username)
        
        if user is None:
            return False, None
        
        if not self.verify_password(password, user.password_hash):
            self.logger.log_authentication_event(
                str(user.id),
                AUTH_EVENTS['LOGIN_FAILED'],
                "Invalid password"
            )
            return False, None
        
        if user.status != 'active':
            self.logger.log_authentication_event(
                str(user.id),
                AUTH_EVENTS['LOGIN_FAILED'],
                f"User status: {user.status}"
            )
            return False, None
        
        return True, user
    
    def create_login_log(self, user_id: str, ip_address: str = None, device_name: str = None) -> LoginLog:
        """
        Create a login log entry.
        
        Args:
            user_id: User ID
            ip_address: IP address
            device_name: Device name
            
        Returns:
            LoginLog object
        """
        user = self.get_user_by_id(user_id)
        if not user:
            return None
        
        login_log = LoginLog(
            login_time=datetime.utcnow(),
            status='active',
            ip_address=ip_address,
            device_name=device_name
        )
        
        user.login_logs.append(login_log)
        user.save()
        
        return login_log
    
    def update_login_log(self, user_id: str, status: str, reason: str = None):
        """
        Update login log on logout/lock.
        
        Args:
            user_id: User ID
            status: New status
            reason: Reason for status change
        """
        user = self.get_user_by_id(user_id)
        if not user or not user.login_logs:
            return
        
        # Update the most recent active login log
        for log in reversed(user.login_logs):
            if log.status == 'active':
                log.logout_time = datetime.utcnow()
                log.status = status
                log.reason = reason
                break
        
        user.save()
    
    def create_authentication_log(self, user_id: str, event: str, details: str = None) -> AuthenticationLog:
        """
        Create an authentication log entry.
        
        Args:
            user_id: User ID
            event: Event type
            details: Additional details
            
        Returns:
            AuthenticationLog object
        """
        user = self.get_user_by_id(user_id)
        if not user:
            return None
        
        auth_log = AuthenticationLog(
            timestamp=datetime.utcnow(),
            event=event,
            details=details
        )
        
        user.authentication_logs.append(auth_log)
        user.save()
        
        self.logger.log_authentication_event(user_id, event, details)
        
        return auth_log
    
    def update_last_login(self, user: User):
        """
        Update user's last login time.
        
        Args:
            user: User object
        """
        user.last_login = datetime.utcnow()
        user.save()
    
    def get_recent_login_logs(self, user_id: str, limit: int = 10) -> list:
        """
        Get recent login logs for a user.
        
        Args:
            user_id: User ID
            limit: Number of logs to retrieve
            
        Returns:
            List of LoginLog objects
        """
        user = self.get_user_by_id(user_id)
        if not user or not user.login_logs:
            return []
        
        # Return most recent logs (already in order by append)
        return user.login_logs[-limit:] if len(user.login_logs) > limit else user.login_logs
    
    def get_recent_authentication_logs(self, user_id: str, limit: int = 20) -> list:
        """
        Get recent authentication logs for a user.
        
        Args:
            user_id: User ID
            limit: Number of logs to retrieve
            
        Returns:
            List of AuthenticationLog objects
        """
        user = self.get_user_by_id(user_id)
        if not user or not user.authentication_logs:
            return []
        
        # Return most recent logs (already in order by append)
        return user.authentication_logs[-limit:] if len(user.authentication_logs) > limit else user.authentication_logs
