import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'shivam-super-secret-key')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('SECRET_KEY', 'shivam-jwt-secret')
    CORS_ORIGINS = ["http://localhost:5173"] 
    GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
    
