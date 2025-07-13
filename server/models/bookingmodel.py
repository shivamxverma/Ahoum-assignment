from models import db

class Booking(db.Model):
    __tablename__ = 'bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    session_id = db.Column(db.Integer, db.ForeignKey('sessions.id'), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    status = db.Column(db.String(50), nullable=False, default='pending')
    
    user = db.relationship('User', back_populates='bookings', lazy=True)
    event = db.relationship('Event', back_populates='bookings', lazy=True)
    session = db.relationship('Session', back_populates='bookings', lazy=True)
