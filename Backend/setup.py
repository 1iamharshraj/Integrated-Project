"""
Setup script for ZeTheta FinArcade Backend
Run this script to initialize the database and create necessary tables
"""

import os
from app import create_app
from extensions import db
from models import *

def setup_database():
    """Initialize database and create tables"""
    app = create_app()
    
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("Database tables created successfully!")
        print("\nYou can now run the application with: python app.py")

if __name__ == '__main__':
    setup_database()

