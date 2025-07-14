from flask import Blueprint, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from database import db
from models.model import Booking, Session, Event, User
from datetime import datetime

bookings_bp = Blueprint('bookings', __name__,url_prefix='/api/bookings')

CORS(bookings_bp, resources={r"/*": {"origins": ["http://localhost:5173", "*"]}}) 

@bookings_bp.route('/', methods=['GET'])
def get_user_bookings():
    try:
        print("Fetching user bookings")
        user_id = request.args.get('userId')
        
        if not user_id:
            return jsonify({'message': 'userId is required'}), 400
        
        try:
            user_id = int(user_id)  
        except ValueError:
            return jsonify({'message': 'userId must be a valid integer'}), 400

        bookings = Booking.query.filter_by(user_id=user_id).all()
        
        if not bookings:
            return jsonify({'message': 'No bookings found for this user'}), 404

        bookings_data = []
        for booking in bookings:
            session = Session.query.get(booking.session_id)
            if not session:
                print(f"Session {booking.session_id} not found for booking {booking.id}")
                continue

            event = Event.query.get(session.event_id)
            if not event:
                print(f"Event {session.event_id} not found for session {session.id}")
                continue

            facilitator = session.facilitator
            facilitator_data = {
                'id': facilitator.id,
                'name': facilitator.name
            } if facilitator else {'id': None, 'name': 'No facilitator'}

            bookings_data.append({
                'id': booking.id,
                'status': booking.status,
                'created_at': booking.created_at.isoformat(),
                'event': {
                    'id': event.id,
                    'title': event.name,
                    'description': event.description,
                    'date': event.date.isoformat(),
                    'location': event.location
                },
                'session': {
                    'id': session.id,
                    'name': session.name,
                    'time': session.start_time.isoformat(),
                    'facilitator': facilitator_data
                }
            })

        return jsonify(bookings_data), 200
    except Exception as e:
        print(f"Error fetching bookings: {str(e)}") 
        return jsonify({'message': f'Error fetching bookings: {str(e)}'}), 500

# @bookings_bp.route('/events/book', methods=['POST'])
# def book_session():
#     try:
#         data = request.get_json()
#         user_id = data.get('userId')
#         session_id = data.get('sessionId')
#         event_id = data.get('eventId')

#         if not user_id or not session_id or not event_id:
#             return jsonify({'message': 'Missing required fields'}), 400

#         if int(user_id) != current_user.id:
#             return jsonify({'message': 'Unauthorized access'}), 403

#         session = Session.query.get(session_id)
#         if not session or session.event_id != event_id:
#             return jsonify({'message': 'Invalid session or event'}), 404

#         existing_booking = Booking.query.filter_by(user_id=user_id, session_id=session_id).first()
#         if existing_booking:
#             return jsonify({'message': 'Session already booked'}), 400

#         booking = Booking(
#             user_id=user_id,
#             session_id=session_id,
#             status='confirmed',
#             created_at=datetime.utcnow()
#         )
#         db.session.add(booking)
#         db.session.commit()

#         return jsonify({
#             'message': 'Session booked successfully',
#             'booking': {
#                 'id': booking.id,
#                 'status': booking.status,
#                 'created_at': booking.created_at.isoformat(),
#                 'eventId': event_id,
#                 'sessionId': session_id
#             }
#         }), 200
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({'message': f'Error booking session: {str(e)}'}), 500