import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
    DB_PATH = str(BASE_DIR / "databases" / "database.db")
    TEMPLATE_FOLDER = str(BASE_DIR / "app" / "templates")
    STATIC_FOLDER = str(BASE_DIR / "static")

class DevConfig(Config):
    DEBUG = True
