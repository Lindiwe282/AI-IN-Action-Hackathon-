#!/usr/bin/env python3
"""
Neon PostgreSQL Database Migration Script for Financial Coach App
This script migrates the database schema to match Portfolio Analyzer structure
"""

import os
import sys
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text, inspect
import psycopg2
from psycopg2 import sql

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:Afri_Sam10@localhost:5432/stocksdb")

def connect_to_postgresql():
    """Connect directly to PostgreSQL for schema operations"""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        logger.info("Connected to PostgreSQL database successfully")
        return conn, cursor
    except Exception as e:
        logger.error(f"Failed to connect to PostgreSQL: {str(e)}")
        return None, None

def migrate_neon_schema():
    """Migrate database schema for Neon PostgreSQL"""
    conn, cursor = connect_to_postgresql()
    
    if not conn or not cursor:
        logger.error("Cannot proceed without database connection")
        return False
    
    try:
        logger.info("=== MIGRATING TO NEON POSTGRESQL SCHEMA ===")
        
        # Create users table if it doesn't exist
        logger.info("Creating users table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(80) UNIQUE NOT NULL,
                email VARCHAR(120) UNIQUE NOT NULL,
                password_hash VARCHAR(128),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT TRUE
            );
        """)
        logger.info("✓ Users table created/verified")
        
        # Create portfolios table if it doesn't exist
        logger.info("Creating portfolios table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS portfolios (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id),
                name VARCHAR(100) NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT TRUE
            );
        """)
        logger.info("✓ Portfolios table created/verified")
        
        # Create portfolio_stocks table if it doesn't exist
        logger.info("Creating portfolio_stocks table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS portfolio_stocks (
                id SERIAL PRIMARY KEY,
                portfolio_id INTEGER REFERENCES portfolios(id),
                ticker VARCHAR(20) NOT NULL,
                shares DOUBLE PRECISION NOT NULL,
                purchase_price DOUBLE PRECISION NOT NULL,
                purchase_date DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        logger.info("✓ Portfolio_stocks table created/verified")
        
        # Create wallets table with all required columns
        logger.info("Creating wallets table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS wallets (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id),
                balance DOUBLE PRECISION DEFAULT 0.0,
                currency VARCHAR(3) DEFAULT 'USD',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                cumulative_gain DOUBLE PRECISION DEFAULT 0.0,
                last_gain_update DATE,
                investment_amount DOUBLE PRECISION DEFAULT 350.0
            );
        """)
        logger.info("✓ Wallets table created/verified")
        
        # Create user_sessions table for session persistence
        logger.info("Creating user_sessions table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_sessions (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id),
                session_id VARCHAR(255) UNIQUE NOT NULL,
                data TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP,
                is_active BOOLEAN DEFAULT TRUE,
                final_portfolio TEXT,
                final_portfolio_analysis TEXT,
                final_market_analysis TEXT,
                tactical_analysis_results TEXT,
                tactical_portfolio TEXT,
                tactical_capital DOUBLE PRECISION,
                investment_capital DOUBLE PRECISION,
                cumulative_gain DOUBLE PRECISION DEFAULT 0.0,
                last_gain_update VARCHAR(50)
            );
        """)
        logger.info("✓ User_sessions table created/verified")
        
        # Create market_data table for caching market information
        logger.info("Creating market_data table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS market_data (
                id SERIAL PRIMARY KEY,
                ticker VARCHAR(20) NOT NULL,
                data_type VARCHAR(50) NOT NULL,
                data JSONB,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP,
                UNIQUE(ticker, data_type)
            );
        """)
        logger.info("✓ Market_data table created/verified")
        
        # Create financial_tips table (from existing schema)
        logger.info("Creating financial_tips table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS financial_tips (
                id SERIAL PRIMARY KEY,
                title VARCHAR(200) NOT NULL,
                content TEXT NOT NULL,
                category VARCHAR(50),
                difficulty VARCHAR(20),
                tags TEXT[],
                is_featured BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        logger.info("✓ Financial_tips table created/verified")
        
        # Create financial_plans table (from existing schema)
        logger.info("Creating financial_plans table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS financial_plans (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id),
                goal_type VARCHAR(50) NOT NULL,
                target_amount DOUBLE PRECISION NOT NULL,
                target_date DATE,
                monthly_contribution DOUBLE PRECISION,
                current_savings DOUBLE PRECISION DEFAULT 0.0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT TRUE
            );
        """)
        logger.info("✓ Financial_plans table created/verified")
        
        # Create transactions table (from existing schema)
        logger.info("Creating transactions table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id),
                wallet_id INTEGER REFERENCES wallets(id),
                amount DOUBLE PRECISION NOT NULL,
                transaction_type VARCHAR(20) NOT NULL,
                category VARCHAR(50),
                description TEXT,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_recurring BOOLEAN DEFAULT FALSE,
                tags TEXT[]
            );
        """)
        logger.info("✓ Transactions table created/verified")
        
        # Create investments table (from existing schema)
        logger.info("Creating investments table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS investments (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id),
                portfolio_id INTEGER REFERENCES portfolios(id),
                ticker VARCHAR(20) NOT NULL,
                investment_type VARCHAR(50),
                shares DOUBLE PRECISION,
                purchase_price DOUBLE PRECISION,
                current_price DOUBLE PRECISION,
                purchase_date TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        logger.info("✓ Investments table created/verified")
        
        # Create indexes for better performance
        logger.info("Creating database indexes...")
        index_queries = [
            "CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);",
            "CREATE INDEX IF NOT EXISTS idx_portfolios_user_id ON portfolios(user_id);",
            "CREATE INDEX IF NOT EXISTS idx_portfolio_stocks_portfolio_id ON portfolio_stocks(portfolio_id);",
            "CREATE INDEX IF NOT EXISTS idx_portfolio_stocks_ticker ON portfolio_stocks(ticker);",
            "CREATE INDEX IF NOT EXISTS idx_wallets_user_id ON wallets(user_id);",
            "CREATE INDEX IF NOT EXISTS idx_user_sessions_user_id ON user_sessions(user_id);",
            "CREATE INDEX IF NOT EXISTS idx_user_sessions_session_id ON user_sessions(session_id);",
            "CREATE INDEX IF NOT EXISTS idx_market_data_ticker ON market_data(ticker);",
            "CREATE INDEX IF NOT EXISTS idx_market_data_expires_at ON market_data(expires_at);",
            "CREATE INDEX IF NOT EXISTS idx_transactions_user_id ON transactions(user_id);",
            "CREATE INDEX IF NOT EXISTS idx_transactions_date ON transactions(date);",
            "CREATE INDEX IF NOT EXISTS idx_investments_user_id ON investments(user_id);",
            "CREATE INDEX IF NOT EXISTS idx_investments_ticker ON investments(ticker);"
        ]
        
        for query in index_queries:
            try:
                cursor.execute(query)
            except Exception as e:
                logger.warning(f"Index creation warning: {str(e)}")
        
        logger.info("✓ Database indexes created/verified")
        
        # Commit all changes
        conn.commit()
        logger.info("\n✓ All schema migrations completed successfully!")
        
        # Verify the schema
        logger.info("\n=== VERIFYING NEON DATABASE SCHEMA ===")
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            ORDER BY table_name;
        """)
        tables = cursor.fetchall()
        logger.info("Tables in database:")
        for table in tables:
            logger.info(f"  - {table[0]}")
        
        conn.close()
        logger.info("\n🎉 Neon PostgreSQL migration completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Migration failed: {str(e)}")
        if conn:
            conn.rollback()
            conn.close()
        return False

def main():
    """Main migration function"""
    logger.info("Starting Neon PostgreSQL database migration for Financial Coach App...")
    logger.info(f"Using database URL: {DATABASE_URL}")
    
    if migrate_neon_schema():
        logger.info("✅ Migration completed successfully!")
        sys.exit(0)
    else:
        logger.error("❌ Migration failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()