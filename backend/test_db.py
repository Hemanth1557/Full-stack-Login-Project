#!/usr/bin/env python3
"""
Simple script to test database connection and create tables
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./users.db")
print(f"🔍 DATABASE_URL: {DATABASE_URL}")

# Test database connection
from sqlalchemy import create_engine
from app.models import Base

try:
    if DATABASE_URL.startswith("sqlite"):
        engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    else:
        engine = create_engine(DATABASE_URL)
    
    print("✅ Engine created successfully")
    
    # Test connection
    with engine.connect() as conn:
        print("✅ Database connection successful!")
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created successfully!")
    
    # Check if users.db file exists (for SQLite)
    if DATABASE_URL.startswith("sqlite"):
        db_file = DATABASE_URL.replace("sqlite:///", "")
        if os.path.exists(db_file):
            print(f"✅ SQLite database file created: {db_file}")
            print(f"📊 File size: {os.path.getsize(db_file)} bytes")
        else:
            print(f"❌ SQLite database file not found: {db_file}")

except Exception as e:
    print(f"❌ Error: {e}")
