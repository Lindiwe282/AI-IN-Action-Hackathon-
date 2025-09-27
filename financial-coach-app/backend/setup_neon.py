#!/usr/bin/env python3
"""
Test and Setup Script for Neon PostgreSQL Integration
Run this script to test the connection and set up the database for Financial Coach App
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.neon_config import verify_neon_connection, get_neon_config
from database.migrate_to_neon import migrate_neon_schema
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_neon_setup():
    """Test the complete Neon setup"""
    logger.info("=== FINANCIAL COACH APP - NEON POSTGRESQL SETUP ===")
    
    # Step 1: Test connection
    logger.info("Step 1: Testing Neon PostgreSQL connection...")
    if verify_neon_connection():
        logger.info("✅ Connection successful!")
    else:
        logger.error("❌ Connection failed!")
        return False
    
    # Step 2: Show configuration
    logger.info("\nStep 2: Database configuration:")
    config = get_neon_config()
    logger.info(f"  Database URL: {config.database_url[:50]}...")
    logger.info(f"  Pool Size: {config.pool_size}")
    logger.info(f"  Max Overflow: {config.max_overflow}")
    logger.info(f"  Pool Recycle: {config.pool_recycle}s")
    
    # Step 3: Run migration
    logger.info("\nStep 3: Running database migration...")
    if migrate_neon_schema():
        logger.info("Migration successful!")
    else:
        logger.error(" Migration failed!")
        return False
    
    logger.info("\nNeon PostgreSQL setup completed successfully!")
    logger.info("\nYour Financial Coach App is now configured to use the same")
    logger.info("Neon PostgreSQL database as your Portfolio Analyzer!")
    
    return True

def main():
    """Main function"""
    try:
        if test_neon_setup():
            logger.info("\n Setup completed successfully!")
            logger.info("\nNext steps:")
            logger.info("1. Install dependencies: pip install -r requirements.txt")
            logger.info("2. Run your Flask app with the new database configuration")
            logger.info("3. The app will automatically use the Neon PostgreSQL database")
            sys.exit(0)
        else:
            logger.error("\nSetup failed!")
            sys.exit(1)
    except Exception as e:
        logger.error(f"Setup error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()