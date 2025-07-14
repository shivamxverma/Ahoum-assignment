from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

from database import db

# -------------------------------
# User Table
# -------------------------------
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=True)
    username = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password = db.Column(db.String(256), nullable=True)
    google_id = db.Column(db.String(120), unique=True, nullable=True, index=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    bookings = db.relationship('Booking', back_populates='user')

    def set_password(self, password):
        self.password = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        return check_password_hash(self.password, password)

# -------------------------------
# Facilitator Table
# -------------------------------
class Facilitator(db.Model):
    __tablename__ = 'facilitators'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    phone = db.Column(db.String(20), nullable=True)
    password = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    sessions = db.relationship('Session', back_populates='facilitator')

    def check_password(self, password):
        """Verify the provided password against the stored hash."""
        return check_password_hash(self.password, password)

# -------------------------------
# Event Table
# -------------------------------
class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    sessions = db.relationship('Session', back_populates='event')

# -------------------------------
# Session Table
# -------------------------------
class Session(db.Model):
    __tablename__ = 'sessions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    facilitator_id = db.Column(db.Integer, db.ForeignKey('facilitators.id'), nullable=False)

    event = db.relationship('Event', back_populates='sessions')
    facilitator = db.relationship('Facilitator', back_populates='sessions')
    bookings = db.relationship('Booking', back_populates='session')

# -------------------------------
# Booking Table
# -------------------------------
class Booking(db.Model):
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(50), nullable=False, default='pending')
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    session_id = db.Column(db.Integer, db.ForeignKey('sessions.id'), nullable=False)

    user = db.relationship('User', back_populates='bookings')
    session = db.relationship('Session', back_populates='bookings')
