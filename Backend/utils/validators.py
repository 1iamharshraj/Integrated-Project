"""
Validation utilities
"""

import re
from decimal import Decimal

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    """Validate Indian phone number"""
    if not phone:
        return False
    # Remove spaces and special characters
    phone = re.sub(r'[^\d]', '', phone)
    # Indian phone numbers: 10 digits starting with 6-9
    pattern = r'^[6-9]\d{9}$'
    return re.match(pattern, phone) is not None

def validate_risk_data(data):
    """Validate risk profiling data"""
    required_fields = ['user_id']
    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}"
    return True, None

def validate_decimal(value, min_val=None, max_val=None):
    """Validate decimal value"""
    try:
        decimal_value = Decimal(str(value))
        if min_val is not None and decimal_value < min_val:
            return False, f"Value must be >= {min_val}"
        if max_val is not None and decimal_value > max_val:
            return False, f"Value must be <= {max_val}"
        return True, decimal_value
    except (ValueError, TypeError):
        return False, "Invalid decimal value"

