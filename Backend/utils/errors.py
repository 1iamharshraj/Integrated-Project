"""
Custom error classes
"""

class ValidationError(Exception):
    """Validation error"""
    pass

class NotFoundError(Exception):
    """Resource not found error"""
    pass

class UnauthorizedError(Exception):
    """Unauthorized access error"""
    pass

