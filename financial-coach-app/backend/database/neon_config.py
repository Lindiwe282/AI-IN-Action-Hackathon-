"""
Neon PostgreSQL Database Configuration for Financial Coach App
This module provides database connection and configuration utilities
"""

import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
import psycopg2
from contextlib import contextmanager

logger = logging.getLogger(__name__)

class NeonDatabaseConfig:
    """Neon PostgreSQL database configuration class"""
    
    def __init__(self):
        self.database_url = os.getenv("DATABASE_URL", "postgresql://postgres:Afri_Sam10@localhost:5432/stocksdb")
        self.pool_size = int(os.getenv("DB_POOL_SIZE", "10"))
        self.max_overflow = int(os.getenv("DB_MAX_OVERFLOW", "20"))
        self.pool_recycle = int(os.getenv("DB_POOL_RECYCLE", "3600"))
        self.pool_pre_ping = os.getenv("DB_POOL_PRE_PING", "True").lower() == "true"
        
    def get_engine_config(self):
        """Get SQLAlchemy engine configuration"""
        return {
            'pool_size': self.pool_size,
            'pool_recycle': self.pool_recycle,
            'pool_pre_ping': self.pool_pre_ping,
            'max_overflow': self.max_overflow,
            'poolclass': QueuePool
        }
    
    def get_flask_config(self):
        """Get Flask-SQLAlchemy configuration"""
        return {
            'SQLALCHEMY_DATABASE_URI': self.database_url,
            'SQLALCHEMY_TRACK_MODIFICATIONS': False,
            'SQLALCHEMY_ENGINE_OPTIONS': self.get_engine_config()
        }
    
    def create_engine(self):
        """Create SQLAlchemy engine with Neon-optimized settings"""
        return create_engine(
            self.database_url,
            **self.get_engine_config()
        )
    
    def create_session_factory(self):
        """Create session factory for direct database access"""
        engine = self.create_engine()
        return sessionmaker(bind=engine)
    
    @contextmanager
    def get_connection(self):
        """Get raw psycopg2 connection for direct SQL operations"""
        conn = None
        try:
            conn = psycopg2.connect(self.database_url)
            yield conn
        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"Database connection error: {str(e)}")
            raise
        finally:
            if conn:
                conn.close()
    
    def test_connection(self):
        """Test database connection"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT version();")
                version = cursor.fetchone()
                logger.info(f"Connected to PostgreSQL: {version[0]}")
                return True
        except Exception as e:
            logger.error(f"Connection test failed: {str(e)}")
            return False

# Global instance
neon_config = NeonDatabaseConfig()

def get_neon_config():
    """Get the global Neon configuration instance"""
    return neon_config

def apply_neon_config_to_app(app):
    """Apply Neon database configuration to Flask app"""
    config = neon_config.get_flask_config()
    for key, value in config.items():
        app.config[key] = value
    
    logger.info("Applied Neon PostgreSQL configuration to Flask app")
    return app

def verify_neon_connection():
    """Verify connection to Neon database"""
    return neon_config.test_connection()