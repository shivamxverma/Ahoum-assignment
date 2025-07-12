from flask import Blueprint, request, jsonify, current_app
from models.event import Event
from models import db
from datetime import datetime

event_bp = Blueprint('event', __name__, url_prefix='/api/events')

@event_bp.route('/', methods=['GET'])
def get_events():
    events = Event.query.all()
    return jsonify([event.to_dict() for event in events]), 200

@event_bp.route('/<int:event_id>', methods=['GET'])
def get_event(event_id):    
    event = Event.query.get(event_id)
    if event:
        return jsonify(event.to_dict()), 200
    return jsonify({'message': 'Event not found'}), 404

