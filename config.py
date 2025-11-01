import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "secret-key")
    SQLALCHEMY_DATABASE_URI = "sqlite:///rent_management.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
