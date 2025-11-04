"""
Quick script to check database connection and table creation
"""

from app import create_app
from extensions import db
from models import User, RiskProfile, Portfolio, Holding, Transaction, KYCDocument, Goal, BehavioralMetrics, AIInsight, EducationProgress, MarketFeatures, SentimentAnalysis

def check_database():
    """Check database connection and tables"""
    app = create_app()
    
    with app.app_context():
        print("=" * 60)
        print("Database Connection Check")
        print("=" * 60)
        print()
        
        try:
            # Test connection
            db.session.execute(db.text("SELECT 1"))
            print("✅ Database connection successful")
        except Exception as e:
            print(f"❌ Database connection failed: {str(e)}")
            return False
        
        print()
        print("Checking tables...")
        print("-" * 60)
        
        # Check if tables exist
        inspector = db.inspect(db.engine)
        existing_tables = inspector.get_table_names()
        
        required_tables = [
            'users', 'risk_profiles', 'portfolios', 'holdings',
            'transactions', 'kyc_documents', 'goals', 'behavioral_metrics',
            'ai_insights', 'education_progress', 'market_features',
            'sentiment_analysis'
        ]
        
        missing_tables = []
        for table in required_tables:
            if table in existing_tables:
                print(f"✅ {table}")
            else:
                print(f"❌ {table} - MISSING")
                missing_tables.append(table)
        
        print()
        print("-" * 60)
        
        if missing_tables:
            print(f"⚠️  {len(missing_tables)} table(s) missing!")
            print()
            print("To create tables, run:")
            print("  python setup.py")
            print()
            print("Or use Flask-Migrate:")
            print("  flask db init")
            print("  flask db migrate -m 'Initial migration'")
            print("  flask db upgrade")
            return False
        else:
            print("✅ All tables exist!")
            return True

if __name__ == '__main__':
    check_database()

