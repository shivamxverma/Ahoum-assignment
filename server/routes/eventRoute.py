from flask import Blueprint, request, jsonify, current_app
from models.model import Event, Booking, Session, User
from app import db
from datetime import datetime
import requests

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
    print("Booking a session")
    print("Request data:", request.get_json())
    data = request.get_json()
    session_id = data.get('sessionId')
    user_id = data.get('userId')

    if not session_id or not user_id:
        return jsonify({'error': 'Session ID and User ID are required'}), 400

    session = Session.query.get(session_id)
    if not session:
        return jsonify({'error': 'Session not found'}), 404

    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Uncomment if you want to prevent duplicate bookings
    # existing_booking = Booking.query.filter_by(user_id=user_id, session_id=session_id).first()
    # if existing_booking:
    #     return jsonify({'error': 'User already booked for this session'}), 400

    # booking = Booking(
    #     user_id=user_id,
    #     session_id=session_id,
    #     status="booked"
    # )
    
    # print(f"Booking details: User ID: {user_id}, Session ID: {session_id}")
    # db.session.add(booking)
    # db.session.commit()

    try:
        response = requests.post(
            'http://127.0.0.1:5001/notify',
            json={
                'sessionId': session.id,
                'user': {
                    'id': user.id,
                    'name': user.name
                },
                'event': 'session_booked',
                'facilitator_id': session.facilitator.id if session.facilitator else None
            },
            # headers={
            #     'Authorization': f'Bearer {current_app.config["SECRET_TOKEN"]}'
            # }
        )
        response.raise_for_status()
    except requests.RequestException as e:
        current_app.logger.error(f"Notification failed: {str(e)}")

    return jsonify({'message': 'Session booked successfully'}), 200