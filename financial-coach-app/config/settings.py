import os
from pathlib import Path

class Config:
    """Base configuration class"""
    
    # Basic Flask configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///financial_coach.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = DEBUG
    
    # API configuration
    API_VERSION = os.getenv('API_VERSION', 'v1')
    
    # CORS configuration
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*').split(',')
    
    # File paths
    BASE_DIR = Path(__file__).parent.parent
    MODEL_PATH = os.getenv('MODEL_PATH', str(BASE_DIR / 'models'))
    LOG_FILE = os.getenv('LOG_FILE', str(BASE_DIR / 'logs' / 'financial_coach.log'))
    
    # Feature flags
    ENABLE_FRAUD_DETECTION = os.getenv('ENABLE_FRAUD_DETECTION', 'True').lower() == 'true'
    ENABLE_INVESTMENT_RECOMMENDATIONS = os.getenv('ENABLE_INVESTMENT_RECOMMENDATIONS', 'True').lower() == 'true'
    ENABLE_LOAN_ANALYSIS = os.getenv('ENABLE_LOAN_ANALYSIS', 'True').lower() == 'true'
    ENABLE_FINANCIAL_PLANNING = os.getenv('ENABLE_FINANCIAL_PLANNING', 'True').lower() == 'true'
    
    # ML/AI configuration
    ENABLE_MODEL_TRAINING = os.getenv('ENABLE_MODEL_TRAINING', 'False').lower() == 'true'
    
    # Cache configuration
    CACHE_TYPE = os.getenv('CACHE_TYPE', 'simple')
    CACHE_DEFAULT_TIMEOUT = int(os.getenv('CACHE_DEFAULT_TIMEOUT', '300'))
    CACHE_REDIS_URL = os.getenv('CACHE_REDIS_URL', 'redis://localhost:6379/0')
    
    # Security
    HTTPS_ONLY = os.getenv('HTTPS_ONLY', 'False').lower() == 'true'
    
    # Rate limiting
    RATE_LIMIT_ENABLED = os.getenv('RATE_LIMIT_ENABLED', 'False').lower() == 'true'
    RATE_LIMIT_PER_MINUTE = int(os.getenv('RATE_LIMIT_PER_MINUTE', '60'))
    
    # External APIs
    MARKET_DATA_API_KEY = os.getenv('MARKET_DATA_API_KEY')
    NEWS_API_KEY = os.getenv('NEWS_API_KEY')
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    SQLALCHEMY_ECHO = True
    ENABLE_MODEL_TRAINING = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    SQLALCHEMY_ECHO = False
    HTTPS_ONLY = True
    RATE_LIMIT_ENABLED = True

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config(config_name=None):
    """Get configuration based on environment"""
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    return config.get(config_name, config['default'])