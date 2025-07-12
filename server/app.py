import os
import logging
from flask import Flask, request, jsonify,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import jwt
from datetime import datetime, timedelta
from functools import wraps
from authlib.integrations.flask_client import OAuth


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')

db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    
    def set_password(self, password):
        self.password = generate_password_hash(password, method='pbkdf2:sha256')
        
    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<User {self.username}>'
    

oauth = OAuth(app)


google = oauth.register(
    name='google',
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile',
    }
)


# JWT token required decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].replace('Bearer ', '')
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.filter_by(id=data['user_id']).first()
            if not current_user:
                return jsonify({'error': 'User not found'}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
            
        return f(current_user, *args, **kwargs)
    return decorated

# Initialize database
with app.app_context():
    db.create_all()

# Input validation
def validate_user_input(data):
    email = data.get('email', '').strip()
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    
    if not email or not username or not password:
        return False, 'All fields are required'
    
    if len(password) < 8:
        return False, 'Password must be at least 8 characters long'
    
    if not all(c.isalnum() or c == '_' for c in username):
        return False, 'Username can only contain alphanumeric characters and underscores'
        
    return True, None

@app.route('/')
def home():
    return jsonify({'message': 'Welcome to the Flask app!'}), 200

@app.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No input data provided'}), 400
            
        is_valid, error = validate_user_input(data)
        if not is_valid:
            return jsonify({'error': error}), 400

        email = data['email']
        username = data['username']
        password = data['password']

        # Check for existing users
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already exists'}), 409
        if User.query.filter_by(username=username).first():
            return jsonify({'error': 'Username already exists'}), 409

        # Create new user
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(email=email, username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        logger.info(f"New user registered: {username}")
        return jsonify({
            'message': 'User registered successfully',
            'username': username
        }), 201

    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No input data provided'}), 400

        email = data.get('email')
        username = data.get('username')
        password = data.get('password')

        if not (email or username) or not password:
            return jsonify({'error': 'Email/username and password are required'}), 400

        # Find user by email or username
        user = User.query.filter((User.email == email) | (User.username == username)).first()

        if not user:
            logger.warning(f"Login attempt failed: User not found for email/username")
            return jsonify({'error': 'User not found'}), 404

        if not check_password_hash(user.password, password):
            logger.warning(f"Login attempt failed: Invalid password for {user.username}")
            return jsonify({'error': 'Invalid credentials'}), 401

        # Generate JWT token
        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.utcnow() + timedelta(hours=24)
        }, app.config['SECRET_KEY'], algorithm='HS256')

        logger.info(f"Successful login: {user.username}")
        return jsonify({
            'message': 'Login successful',
            'username': user.username,
            'token': token
        }), 200

    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/protected', methods=['GET'])
@token_required
def protected(current_user):
    return jsonify({
        'message': 'Protected route accessed successfully',
        'username': current_user.username
    }), 200
    


@app.route('/api/login/google', methods=['GET'])
def google_login():
    try:
        redirect_uri = url_for('google_callback', _external=True)
        print("Redirecting to Google for login...", redirect_uri)
        return google.authorize_redirect(redirect_uri)
    except Exception as e:
        logger.error(f"Google login error: {str(e)}")
        return jsonify({'error': 'Google login failed'}), 500


@app.route('/api/login/google/callback', methods=['GET'])
def google_callback():
    try:
        print("Google callback received")
        token = google.authorize_access_token()
        user_info = google.parse_id_token(token)

        email = user_info.get('email')
        username = user_info.get('name')

        if not email or not username:
            return jsonify({'error': 'Invalid Google user information'}), 400

        user = User.query.filter_by(email=email).first()
        if not user:
            hashed_password = generate_password_hash('google_oauth', method='pbkdf2:sha256')
            user = User(email=email, username=username, password=hashed_password)
            db.session.add(user)
            db.session.commit()

        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.utcnow() + timedelta(hours=24)
        }, app.config['SECRET_KEY'], algorithm='HS256')

        logger.info(f"Google login successful: {user.username}")
        return jsonify({
            'message': 'Google login successful',
            'username': user.username,
            'token': token
        }), 200
    except Exception as e:
        logger.error(f"Google authorization error: {str(e)}")
        return jsonify({'error': 'Google authorization failed'}), 500

if __name__ == '__main__':
    app.run(debug=True)