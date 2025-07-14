import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'shivam-super-secret-key')
    SQLALCHEMY_DATABASE_URI = 'postgresql://neondb_owner:npg_oNER6t4xULGX@ep-wild-flower-adjr05gg-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('SECRET_KEY', 'shivam-jwt-secret')
    CORS_ORIGINS = ["http://localhost:5173"] 
    GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
    
