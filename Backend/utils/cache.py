"""
Caching utilities
"""

from extensions import redis_client
from flask import current_app
import json
from functools import wraps

def cache_get(key):
    """Get value from cache"""
    try:
        if redis_client:
            value = redis_client.get(key)
            if value:
                return json.loads(value)
    except Exception:
        pass
    return None

def cache_set(key, value, ttl=None):
    """Set value in cache"""
    try:
        if redis_client:
            if ttl:
                redis_client.setex(key, ttl, json.dumps(value))
            else:
                redis_client.set(key, json.dumps(value))
            return True
    except Exception:
        pass
    return False

def cache_delete(key):
    """Delete key from cache"""
    try:
        if redis_client:
            redis_client.delete(key)
            return True
    except Exception:
        pass
    return False

def cached(ttl=None):
    """Decorator to cache function results"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            cache_key = f"{f.__name__}:{str(args)}:{str(kwargs)}"
            cached_value = cache_get(cache_key)
            if cached_value is not None:
                return cached_value
            result = f(*args, **kwargs)
            cache_set(cache_key, result, ttl)
            return result
        return decorated_function
    return decorator

