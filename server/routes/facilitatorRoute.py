from flask import Blueprint, request, jsonify, current_app
from models.model import Event, Booking, Session, User,Facilitator
from datetime import datetime
from database import db

facilitator_bp = Blueprint('facilitator', __name__, url_prefix='/api/facilitators')


