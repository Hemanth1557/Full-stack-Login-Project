import os
from dotenv import load_dotenv

# Load .env file from the backend directory
load_dotenv()

# Force SQLite for development
DATABASE_URL = "sqlite:///./users.db"
SECRET_KEY = os.getenv("SECRET_KEY", "dev_key")

print(f"🔍 Using DATABASE_URL: {DATABASE_URL}")
