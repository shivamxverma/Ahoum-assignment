from flask import Blueprint, request, jsonify, current_app, url_for
from models.model import db, User, Facilitator
from authlib.integrations.flask_client import OAuth
from datetime import datetime, timedelta
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import logging
from sqlalchemy import or_
from authlib.integrations.base_client.errors import OAuthError

auth_bp = Blueprint('auth', __name__, url_prefix='/api')
logger = logging.getLogger(__name__)

# JWT protection
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        if not token:
            return jsonify({"error": "Token is missing"}), 401
        try:
            data = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
            user = User.query.get(data.get('user_id'))
            facilitator = Facilitator.query.get(data.get('facilitator_id'))
            if not (user or facilitator):
                return jsonify({'error': 'User or Facilitator not found'}), 401
            return f(user or facilitator, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
    return decorated

def get_user_or_facilitator(model, identifier, password):
    """Helper to fetch user/facilitator and check password."""
    obj = model.query.filter(
        or_(model.email == identifier, getattr(model, 'username', None) == identifier)
    ).first()
    if not obj or not obj.check_password(password):
        return None
    return obj

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    role = data.get('role', 'user').lower()
    if role not in ['user', 'facilitator']:
        return jsonify({'error': 'Invalid role'}), 400
    
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    phone = data.get('phone')

    if role == 'facilitator':
        print(f"Registering facilitator with email: {email}, name: {name}, phone: {phone}")
        if not all([email, name, phone, password]):
            return jsonify({'error': 'Missing required fields for facilitator'}), 400
        if Facilitator.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already exists'}), 409
        facilitator = Facilitator(
            name=name,
            email=email,
            phone=phone,
            password=generate_password_hash(password, method='pbkdf2:sha256')
        )
        db.session.add(facilitator)
        db.session.commit()
        return jsonify({'message': 'Facilitator registered successfully'}), 201
    else:
        username = data.get('username')
        if not all([email, username, password]):
            return jsonify({'error': 'Missing required fields for user'}), 400
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already exists'}), 409
        if User.query.filter_by(username=username).first():
            return jsonify({'error': 'Username already exists'}), 409
        user = User(
            name=name,
            email=email,
            username=username,
            password=generate_password_hash(password, method='pbkdf2:sha256')
        )
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'User registered successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    role = data.get('role', 'user').lower()
    if role not in ['user', 'facilitator']:
        return jsonify({'error': 'Invalid role'}), 400
    
    identifier = data.get('email') or data.get('username')
    password = data.get('password')

    if not identifier or not password:
        return jsonify({'error': 'Missing credentials'}), 400

    if role == 'facilitator':
        facilitator = get_user_or_facilitator(Facilitator, identifier, password)
        if not facilitator:
            return jsonify({'error': 'Invalid credentials or facilitator not found'}), 401
        token = jwt.encode({
            'facilitator_id': facilitator.id,
            'exp': datetime.utcnow() + timedelta(hours=24)
        }, current_app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({
            'message': 'Facilitator login successful',
            'token': token,
            'facilitatorId': facilitator.id,
            'name': facilitator.name
        }), 200
    else:
        user = get_user_or_facilitator(User, identifier, password)
        if not user:
            return jsonify({'error': 'Invalid credentials'}), 401
        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.utcnow() + timedelta(hours=24)
        }, current_app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({
            'message': 'Login successful',
            'token': token,
            'userId': user.id,
            'username': user.username
        }), 200

@auth_bp.route('/login/google', methods=['GET'])
def google_login():
    try:
        redirect_uri = url_for('auth.google_callback', _external=True)
        logger.info(f"Redirecting to Google for login: {redirect_uri}")
        return current_app.google.authorize_redirect(redirect_uri)
    except Exception as e:
        logger.error(f"Google login error: {str(e)}")
        return jsonify({'error': 'Google login failed'}), 500

@auth_bp.route('/login/google/callback', methods=['GET'])
def google_callback():
    try:
        logger.info("Google callback received")
        token = current_app.google.authorize_access_token()
        user_info = current_app.google.parse_id_token(token, nonce=None)

        email = user_info.get('email')
        username = user_info.get('name')
        google_id = user_info.get('sub')

        if not email or not username:
            return jsonify({'error': 'Invalid Google user information'}), 400

        user = User.query.filter_by(email=email).first()
        if not user:
            user = User(
                email=email,
                username=username,
                google_id=google_id,
                password=generate_password_hash(str(google_id), method='pbkdf2:sha256')
            )
            db.session.add(user)
            db.session.commit()
        elif user.google_id != google_id:
            user.google_id = google_id
            db.session.commit()

        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.utcnow() + timedelta(hours=24)
        }, current_app.config['SECRET_KEY'], algorithm='HS256')

        logging.info(f"Google login successful: {user.username}")
        return jsonify({
            'message': 'Google login successful',
            'username': user.username,
            'token': token
        }), 200
    except OAuthError as e:
        logger.error(f"Google OAuth error: {str(e)}")
        return jsonify({'error': 'Google authorization failed'}), 500
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({'error': 'Unexpected error during Google authorization'}), 500

@auth_bp.route('/protected', methods=['GET'])
@token_required
def protected(user):
    username = user.username if hasattr(user, 'username') else user.name
    return jsonify({'message': 'Welcome!', 'username': username}), 200