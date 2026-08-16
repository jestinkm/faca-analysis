"""
Logger service for FaceSecure application.
Provides logging functionality for various modules.
"""

from utils.logger import FaceSecureLogger


class LoggerService:
    """Service for application logging."""
    
    def __init__(self):
        """Initialize logger service."""
        self.logger = FaceSecureLogger()
    
    def log_authentication(self, user_id: int, event: str, details: str = None):
        """
        Log authentication event.
        
        Args:
            user_id: User ID
            event: Event type
            details: Additional details
        """
        self.logger.log_authentication_event(user_id, event, details)
    
    def log_error(self, module: str, error: str):
        """
        Log error.
        
        Args:
            module: Module name
            error: Error message
        """
        self.logger.log_error(module, error)
    
    def log_security(self, event: str, details: str):
        """
        Log security event.
        
        Args:
            event: Event type
            details: Event details
        """
        self.logger.log_security_event(event, details)
