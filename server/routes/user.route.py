from flask import Blueprint, request, jsonify, current_app, url_for
from models.user import User
from models import db
from datetime import datetime, timedelta
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import logging

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
            user = User.query.get(data['user_id'])
            if not user:
                return jsonify({'error': 'User not found'}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
        return f(user, *args, **kwargs)
    return decorated

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already exists'}), 409
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 409

    hashed_pw = generate_password_hash(password)
    user = User(email=email, username=username, password=hashed_pw)
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter((User.email == email) | (User.username == username)).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({'error': 'Invalid credentials'}), 401

    token = jwt.encode({
        'user_id': user.id,
        'exp': datetime.utcnow() + timedelta(hours=24)
    }, current_app.config['SECRET_KEY'], algorithm='HS256')

    return jsonify({'message': 'Login successful', 'token': token}), 200

@auth_bp.route('/login/google', methods=['GET'])
def google_login():
    return current_app.google.authorize_redirect(url_for('auth.google_callback', _external=True))

@auth_bp.route('/login/google/callback', methods=['GET'])
def google_callback():
    token = current_app.google.authorize_access_token()
    user_info = current_app.google.parse_id_token(token)
    email = user_info.get('email')
    username = user_info.get('name')

    user = User.query.filter_by(email=email).first()
    if not user:
        hashed_pw = generate_password_hash('google_oauth')
        user = User(email=email, username=username, password=hashed_pw)
        db.session.add(user)
        db.session.commit()

    token = jwt.encode({
        'user_id': user.id,
        'exp': datetime.utcnow() + timedelta(hours=24)
    }, current_app.config['SECRET_KEY'], algorithm='HS256')

    return jsonify({'message': 'Google login successful', 'token': token}), 200

@auth_bp.route('/protected', methods=['GET'])
@token_required
def protected(user):
    return jsonify({'message': 'Welcome!', 'username': user.username}), 200
