from flask import Blueprint, request, jsonify, current_app
from models.model import Event, Booking, Session, User
from app import db  # Import db from the main app file
from datetime import datetime
import requests
from requests.exceptions import RequestException

event_bp = Blueprint('event', __name__, url_prefix='/api/events')

@event_bp.route('/', methods=['GET'])
def get_events():
    try:
        print("Fetching all events")
        events = Event.query.all()
        result = [
            {
                'id': event.id,
                'title': event.name,
                'description': event.description,
                'date': event.date.strftime('%Y-%m-%d'),
                'location': event.location,
                'sessions': [
                    {
                        'id': session.id,
                        'name': session.name,
                        'time': session.start_time.isoformat(),
                        'facilitator': {
                            'id': session.facilitator.id,
                            'name': session.facilitator.name
                        } if session.facilitator else None
                    }
                    for session in event.sessions
                ]
            }
            for event in events
        ]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@event_bp.route('/<int:event_id>', methods=['GET'])
def get_event(event_id):
    event = Event.query.get(event_id)
    if event:
        return jsonify(event.to_dict()), 200
    return jsonify({'message': 'Event not found'}), 404

@event_bp.route('/book', methods=['POST'])
def book_session():
    current_app.logger.info("Booking a session")
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Missing JSON body'}), 400

    session_id = data.get('sessionId')
    user_id = data.get('userId')

    if not session_id or not user_id:
        return jsonify({'error': 'Session ID and User ID are required'}), 400

    try:
        session_id = int(session_id)
        user_id = int(user_id)
    except (ValueError, TypeError):
        return jsonify({'error': 'Session ID and User ID must be integers'}), 400

    session = Session.query.get(session_id)
    if not session:
        return jsonify({'error': 'Session not found'}), 404

    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    existing_booking = Booking.query.filter_by(user_id=user_id, session_id=session_id).first()
    if existing_booking:
        return jsonify({'error': 'User already booked for this session'}), 400

    booking = Booking(
        user_id=user_id,
        session_id=session_id,
        status="booked"
    )

    try:
        db.session.add(booking)
        db.session.flush() 

        notification_url = current_app.config.get('NOTIFICATION_URL', 'http://127.0.0.1:5001/notify')
        secret_token = current_app.config.get('SECRET_TOKEN')

        response = requests.post(
            notification_url,
            json={
                'session_id': session.id,  
                'user': {
                    'id': user.id,
                    'name': user.name
                },
                'event': 'session_booked',
                'facilitator_id': session.facilitator.id if session.facilitator else None
            },
            headers={'Authorization': f'Bearer {secret_token}'}
        )
        response.raise_for_status()

        db.session.commit()
        current_app.logger.info(f"Booking created and notification sent for user_id: {user_id}, session_id: {session_id}")
        return jsonify({'message': 'Session booked successfully'}), 200

    except RequestException as e:
        db.session.rollback()
        current_app.logger.error(f"Notification failed: {str(e)}")
        return jsonify({'error': 'Failed to send notification'}), 500
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Booking failed: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500