from flask import Blueprint, request, jsonify, current_app
from models.model import Event, Booking, Session, User
from datetime import datetime
from database import db

session_bp = Blueprint('session', __name__, url_prefix='/api/sessions')


@session_bp.route('/', methods=['GET'])
def get_sessions():
    print("Fetching all sessions")
    try:
        sessions = Session.query.all()
        print(sessions)
        result = [
            {
                'id': session.id,
                'name': session.name,
                'start_time': session.start_time.isoformat(),
                'facilitator': {
                    'id': session.facilitator.id,
                    'name': session.facilitator.name
                } if session.facilitator else None,
                'bookings': [
                    {
                        'id': booking.id,
                        'user_id': booking.user_id,
                        'status': booking.status
                    }
                    for booking in session.bookings
                ]
            }
            for session in sessions
        ]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@session_bp.route('/<int:id>', methods=['GET'])
def get_session(id):
    session = Session.query.get(id)
    try:
        if session:
            return jsonify({
                'id': session.id,
                'name': session.name,
                'start_time': session.start_time.isoformat(),
                'facilitator': {
                    'id': session.facilitator.id,
                    'name': session.facilitator.name
                } if session.facilitator else None,
                'bookings': [
                    {
                        'id': booking.id,
                        'user_id': booking.user_id,
                        'status': booking.status
                    }
                    for booking in session.bookings
                ]
            }), 200
        return jsonify({'message': 'Session not found'}), 404                       
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Endpoint to update a session
@session_bp.route('/<int:id>', methods=['PUT'])
def update_session(id):
    try:
        data = request.get_json()
        session = Session.query.get_or_404(id)
        
        # Update session fields
        session.name = data.get('client', session.name)
        if data.get('date') and data.get('time'):
            from datetime import datetime
            start_time = datetime.strptime(f"{data['date']} {data['time']}", '%Y-%m-%d %I:%M %p')
            session.start_time = start_time
        
        # Update booking status if provided
        if data.get('status') and session.bookings:
            for booking in session.bookings:
                booking.status = data['status']
        
        db.session.commit()
        return jsonify({'message': 'Session updated successfully'})
    except Exception as e: 
        return jsonify({'error': str(e)}), 500

@session_bp.route('/<int:id>/cancel', methods=['PUT'])
def cancel_session(id):
    try:
        session = Session.query.get_or_404(id)
        for booking in session.bookings:
            booking.status = 'Cancelled'
        db.session.commit()
        return jsonify({'message': 'Session cancelled successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

