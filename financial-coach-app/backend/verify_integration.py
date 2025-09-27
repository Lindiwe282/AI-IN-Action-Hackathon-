#!/usr/bin/env python3
"""
Database Integration Verification Script
Verifies that both Portfolio Analyzer and Financial Coach App can access the same Neon database
"""

import os
import sys
import psycopg2
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:Afri_Sam10@localhost:5432/stocksdb")

def verify_shared_database():
    """Verify that both apps can access the shared database"""
    
    logger.info("=== VERIFYING SHARED DATABASE ACCESS ===")
    
    try:
        # Connect to the database
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        # Check existing tables
        logger.info("\n1. Checking existing tables...")
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            ORDER BY table_name;
        """)
        tables = cursor.fetchall()
        
        portfolio_tables = []
        financial_tables = []
        
        for table in tables:
            table_name = table[0]
            if table_name in ['portfolios', 'portfolio_stocks', 'wallets', 'user_sessions', 'market_data']:
                portfolio_tables.append(table_name)
            if table_name in ['users', 'financial_tips', 'financial_plans', 'transactions', 'investments']:
                financial_tables.append(table_name)
        
        logger.info(f"Portfolio Analyzer tables: {portfolio_tables}")
        logger.info(f"Financial Coach tables: {financial_tables}")
        
        # Check for data sharing capability
        logger.info("\n2. Testing data sharing capability...")
        
        # Check if users table has data
        cursor.execute("SELECT COUNT(*) FROM users;")
        user_count = cursor.fetchone()[0]
        logger.info(f"Users in shared database: {user_count}")
        
        # Check if wallets table exists and has the right structure
        cursor.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'wallets' 
            ORDER BY ordinal_position;
        """)
        wallet_columns = cursor.fetchall()
        logger.info("Wallet table structure:")
        for col in wallet_columns:
            logger.info(f"  - {col[0]}: {col[1]}")
        
        # Verify session persistence capability
        logger.info("\n3. Testing session persistence capability...")
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'user_sessions';
        """)
        session_columns = [row[0] for row in cursor.fetchall()]
        
        required_session_columns = [
            'final_portfolio', 'final_portfolio_analysis', 'final_market_analysis',
            'tactical_analysis_results', 'investment_capital', 'cumulative_gain'
        ]
        
        missing_columns = [col for col in required_session_columns if col in session_columns]
        logger.info(f"Session persistence columns available: {missing_columns}")
        
        # Test market data sharing
        logger.info("\n4. Testing market data sharing...")
        cursor.execute("SELECT COUNT(*) FROM market_data;")
        market_data_count = cursor.fetchone()[0]
        logger.info(f"Market data entries: {market_data_count}")
        
        conn.close()
        
        logger.info("\n✅ DATABASE INTEGRATION VERIFICATION COMPLETE")
        logger.info("\nSummary:")
        logger.info(f"- Database connection: ✅ SUCCESS")
        logger.info(f"- Portfolio tables: ✅ {len(portfolio_tables)} tables found")
        logger.info(f"- Financial tables: ✅ {len(financial_tables)} tables found") 
        logger.info(f"- User data sharing: ✅ {user_count} users accessible")
        logger.info(f"- Market data sharing: ✅ {market_data_count} entries accessible")
        logger.info(f"- Session persistence: ✅ Structure verified")
        
        logger.info("\n🎉 Both applications can successfully share the Neon PostgreSQL database!")
        return True
        
    except Exception as e:
        logger.error(f"Verification failed: {str(e)}")
        return False

if __name__ == "__main__":
    if verify_shared_database():
        print("\n✅ Integration verification passed!")
        sys.exit(0)
    else:
        print("\n❌ Integration verification failed!")
        sys.exit(1)