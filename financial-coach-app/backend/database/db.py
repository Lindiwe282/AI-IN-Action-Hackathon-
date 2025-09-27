from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

# Database instance (will be initialized in app.py)
db = None
migrate = None

def init_database(app):
    """Initialize database with Flask app"""
    global db, migrate
    
    # Configure database
    if os.getenv('DATABASE_URL'):
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    else:
        # Default to SQLite for development
        basedir = os.path.abspath(os.path.dirname(__file__))
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "..", "financial_coach.db")}'
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions
    from flask_sqlalchemy import SQLAlchemy
    from flask_migrate import Migrate
    
    db = SQLAlchemy(app)
    migrate = Migrate(app, db)
    
    # Import models to register them
    from models.user_schema import User, FinancialPlan, Transaction, Investment, LoanApplication, FinancialTip
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    return db

def get_db():
    """Get database instance"""
    return db

def create_sample_data():
    """Create sample data for development/testing"""
    if not db:
        return
    
    # Check if sample data already exists
    from models.user_schema import User, FinancialTip
    
    if User.query.first():
        return  # Data already exists
    
    # Create sample user
    sample_user = User(
        email='demo@financialcoach.com',
        first_name='Demo',
        last_name='User',
        monthly_income=5000.0,
        monthly_expenses=3500.0,
        current_savings=10000.0,
        total_debt=15000.0,
        dependents=1,
        risk_tolerance='medium',
        investment_experience='beginner'
    )
    
    # Create sample financial tips
    sample_tips = [
        FinancialTip(
            title='Start an Emergency Fund',
            content='An emergency fund is a cash reserve that's specifically set aside for unplanned expenses or financial emergencies. Aim to save 3-6 months of living expenses.',
            category='saving',
            difficulty='beginner',
            tags=['emergency', 'savings', 'basics'],
            is_featured=True
        ),
        FinancialTip(
            title='Understand Compound Interest',
            content='Compound interest is the addition of interest to the principal sum of a loan or deposit. The power of compounding can significantly grow your investments over time.',
            category='investing',
            difficulty='beginner',
            tags=['investing', 'compound_interest', 'basics']
        ),
        FinancialTip(
            title='Create a Budget with the 50/30/20 Rule',
            content='Allocate 50% of your income to needs, 30% to wants, and 20% to savings and debt repayment. This simple rule helps ensure balanced financial planning.',
            category='budgeting',
            difficulty='beginner',
            tags=['budgeting', '50-30-20', 'basics'],
            is_featured=True
        ),
        FinancialTip(
            title='Diversify Your Investment Portfolio',
            content='Don\'t put all your eggs in one basket. Spread your investments across different asset classes, sectors, and geographic regions to reduce risk.',
            category='investing',
            difficulty='intermediate',
            tags=['investing', 'diversification', 'risk_management']
        ),
        FinancialTip(
            title='Pay Off High-Interest Debt First',
            content='Focus on paying off debts with the highest interest rates first (debt avalanche method). This saves money on interest payments over time.',
            category='debt',
            difficulty='beginner',
            tags=['debt', 'strategy', 'interest']
        )
    ]
    
    try:
        db.session.add(sample_user)
        for tip in sample_tips:
            db.session.add(tip)
        
        db.session.commit()
        print("Sample data created successfully!")
        
    except Exception as e:
        db.session.rollback()
        print(f"Error creating sample data: {e}")

class DatabaseManager:
    """Database management utilities"""
    
    @staticmethod
    def backup_database(backup_path=None):
        """Create a backup of the database"""
        import shutil
        from datetime import datetime
        
        if not backup_path:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_path = f'backup_financial_coach_{timestamp}.db'
        
        try:
            # For SQLite databases
            if 'sqlite' in str(db.engine.url):
                db_path = str(db.engine.url).replace('sqlite:///', '')
                shutil.copy2(db_path, backup_path)
                return f"Database backed up to {backup_path}"
            else:
                return "Backup not implemented for this database type"
        except Exception as e:
            return f"Backup failed: {e}"
    
    @staticmethod
    def get_database_stats():
        """Get database statistics"""
        from models.user_schema import User, FinancialPlan, Transaction, Investment, LoanApplication, FinancialTip
        
        stats = {
            'users': User.query.count(),
            'financial_plans': FinancialPlan.query.count(),
            'transactions': Transaction.query.count(),
            'investments': Investment.query.count(),
            'loan_applications': LoanApplication.query.count(),
            'financial_tips': FinancialTip.query.count(),
        }
        
        return stats
    
    @staticmethod
    def clean_old_data(days_old=90):
        """Clean old data from database"""
        from datetime import datetime, timedelta
        from models.user_schema import Transaction
        
        cutoff_date = datetime.utcnow() - timedelta(days=days_old)
        
        try:
            # Clean old completed transactions
            old_transactions = Transaction.query.filter(
                Transaction.created_at < cutoff_date,
                Transaction.status == 'completed',
                Transaction.is_flagged == False
            ).delete()
            
            db.session.commit()
            return f"Cleaned {old_transactions} old transactions"
            
        except Exception as e:
            db.session.rollback()
            return f"Cleanup failed: {e}"
    
    @staticmethod
    def reset_database():
        """Reset database (USE WITH CAUTION)"""
        try:
            # Drop all tables
            db.drop_all()
            # Recreate all tables
            db.create_all()
            # Create sample data
            create_sample_data()
            return "Database reset successfully"
        except Exception as e:
            return f"Database reset failed: {e}"

# Utility functions for common database operations
def get_user_by_id(user_id):
    """Get user by ID"""
    from models.user_schema import User
    return User.query.get(user_id)

def get_user_by_email(email):
    """Get user by email"""
    from models.user_schema import User
    return User.query.filter_by(email=email).first()

def create_user(user_data):
    """Create a new user"""
    from models.user_schema import User
    
    try:
        user = User(**user_data)
        db.session.add(user)
        db.session.commit()
        return user
    except Exception as e:
        db.session.rollback()
        raise e

def update_user(user_id, user_data):
    """Update user information"""
    from models.user_schema import User
    
    try:
        user = User.query.get(user_id)
        if not user:
            return None
        
        for key, value in user_data.items():
            if hasattr(user, key):
                setattr(user, key, value)
        
        db.session.commit()
        return user
    except Exception as e:
        db.session.rollback()
        raise e

def get_user_transactions(user_id, limit=100):
    """Get user transactions"""
    from models.user_schema import Transaction
    
    return Transaction.query.filter_by(user_id=user_id)\
                          .order_by(Transaction.timestamp.desc())\
                          .limit(limit).all()

def get_flagged_transactions(user_id=None):
    """Get flagged transactions"""
    from models.user_schema import Transaction
    
    query = Transaction.query.filter_by(is_flagged=True)
    if user_id:
        query = query.filter_by(user_id=user_id)
    
    return query.order_by(Transaction.timestamp.desc()).all()

def create_financial_plan(user_id, plan_data):
    """Create a financial plan"""
    from models.user_schema import FinancialPlan
    
    try:
        plan_data['user_id'] = user_id
        plan = FinancialPlan(**plan_data)
        db.session.add(plan)
        db.session.commit()
        return plan
    except Exception as e:
        db.session.rollback()
        raise e

def get_user_plans(user_id):
    """Get user's financial plans"""
    from models.user_schema import FinancialPlan
    
    return FinancialPlan.query.filter_by(user_id=user_id)\
                             .order_by(FinancialPlan.created_at.desc()).all()

def get_featured_tips(limit=5):
    """Get featured financial tips"""
    from models.user_schema import FinancialTip
    
    return FinancialTip.query.filter_by(is_featured=True, is_active=True)\
                            .order_by(FinancialTip.views.desc())\
                            .limit(limit).all()

def get_tips_by_category(category, difficulty=None, limit=10):
    """Get tips by category and difficulty"""
    from models.user_schema import FinancialTip
    
    query = FinancialTip.query.filter_by(category=category, is_active=True)
    
    if difficulty:
        query = query.filter_by(difficulty=difficulty)
    
    return query.order_by(FinancialTip.created_at.desc()).limit(limit).all()