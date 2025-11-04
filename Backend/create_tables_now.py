"""
Quick script to create database tables immediately
Run this with: python create_tables_now.py
"""

from app import create_app
from extensions import db
from models import *

print("Creating database tables...")
app = create_app()

with app.app_context():
    try:
        db.create_all()
        print("✅ All database tables created successfully!")
        print("\nYou can now test the registration endpoint.")
    except Exception as e:
        print(f"❌ Error creating tables: {str(e)}")
        print("\nMake sure:")
        print("1. Virtual environment is activated")
        print("2. Database connection is working (test_db_connection.py)")
        print("3. All dependencies are installed (requirements.txt)")

