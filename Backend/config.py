"""
Configuration settings for ZeTheta FinArcade API
"""

import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://postgres:postgres@localhost:5432/zetheta_finarcade'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    
    # JWT Configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key-change-in-production'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    
    # Redis Configuration
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://localhost:6379/0'
    
    # CORS Configuration
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*').split(',')
    
    # Rate Limiting
    RATELIMIT_ENABLED = True
    RATELIMIT_STORAGE_URL = os.environ.get('REDIS_URL') or 'redis://localhost:6379/0'
    
    # API Settings
    API_PREFIX = '/api'
    
    # Cache TTLs (in seconds)
    CACHE_TTL_PORTFOLIO = 300  # 5 minutes
    CACHE_TTL_MARKET = 60  # 1 minute
    CACHE_TTL_RISK_PROFILE = 3600  # 1 hour
    
    # AI Model Paths (update these with actual model paths)
    MODELS_DIR = os.path.join(os.path.dirname(__file__), 'models')
    FINBERT_MODEL_PATH = os.path.join(MODELS_DIR, 'finbert')
    LSTM_MODEL_PATH = os.path.join(MODELS_DIR, 'lstm_model')
    CATBOOST_MODEL_PATH = os.path.join(MODELS_DIR, 'catboost_model')
    ROBERTA_MODEL_PATH = os.path.join(MODELS_DIR, 'roberta_model')
    
    # External APIs
    MARKET_DATA_API_KEY = os.environ.get('MARKET_DATA_API_KEY', '')
    NEWS_SCRAPER_ENABLED = True
    
    # Logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    
    # Pagination
    ITEMS_PER_PAGE = 20
    
class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    SQLALCHEMY_ECHO = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    SQLALCHEMY_ECHO = False

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost:5432/zetheta_finarcade_test'
    WTF_CSRF_ENABLED = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

