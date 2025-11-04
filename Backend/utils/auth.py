"""
Authentication utilities
"""

from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from models.user import User
from extensions import db

def token_required(f):
    """Decorator to require JWT token"""
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            verify_jwt_in_request()
        except Exception as e:
            return jsonify({'error': 'Token is missing or invalid'}), 401
        return f(*args, **kwargs)
    return decorated

def get_current_user():
    """Get current user from JWT token"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return None
        return user
    except Exception:
        return None

