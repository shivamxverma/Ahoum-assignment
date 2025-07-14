from flask import Blueprint, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from database import db
from models.model import Booking, Session, Event, User
# import jwt
from datetime import datetime
# from auth_middleware import token_required

bookings_bp = Blueprint('bookings', __name__,url_prefix='/api/bookings')

@bookings_bp.route('/', methods=['GET'])
def get_user_bookings():
    try:
        print("Fetching user bookings")
        # user_id = request.args.get('userId')
        # if not user_id or int(user_id) != current_user.id:
        #     return jsonify({'message': 'Unauthorized access'}), 403

        bookings = Booking.query.filter_by(user_id=2).all()
        bookings_data = []
        for booking in bookings:
            session = Session.query.get(booking.session_id)
            event = Event.query.get(session.event_id)
            facilitator = session.facilitator
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
                    'facilitator': {
                        'id': facilitator.id,
                        'name': facilitator.name
                    }
                }
            })
        return jsonify(bookings_data), 200
    except Exception as e:
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