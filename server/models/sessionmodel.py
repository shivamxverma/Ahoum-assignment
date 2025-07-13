from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Session(db.Model):
    __tablename__ = 'sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    name = db.Column(db.String(120), nullable=False)  # Example field
    start_time = db.Column(db.DateTime, nullable=False)  # Example field
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    event = db.relationship('Event', back_populates='sessions', lazy=True)
    bookings = db.relationship('Booking', back_populates='session', lazy=True)