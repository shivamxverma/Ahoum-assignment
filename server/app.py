from flask import Flask, session,request,jsonify
from flask_sqlalchemy import SQLAlchemy
# from flask_session import Session
from flask_cors import CORS
from flask_migrate import Migrate
from config import Config
from app import db
from routes.userRoute import auth_bp
from routes.eventRoute import event_bp
from routes.sesssionRoute import session_bp
from authlib.integrations.flask_client import OAuth
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
import logging
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    handlers=[logging.StreamHandler()]
)

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = app.config['SECRET_KEY']  # Required for session management

# Restrict CORS for production
CORS(app, resources={r"/*": {"origins": "*"}})

# Initialize SQLAlchemy with the Flask app
db.init_app(app)
migrate = Migrate(app, db)

# Configure Google OAuth
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=Config.GOOGLE_CLIENT_ID,
    client_secret=Config.GOOGLE_CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile',
        'nonce': True
    }
)

app.oauth = oauth
app.google = google

app.register_blueprint(auth_bp)
app.register_blueprint(event_bp)
app.register_blueprint(session_bp)


# Create database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)