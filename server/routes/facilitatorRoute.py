from flask import Blueprint, request, jsonify, current_app
from models.model import Event, Booking, Session, User,Facilitator
from datetime import datetime
from app import db

facilitator_bp = Blueprint('facilitator', __name__, url_prefix='/api/facilitators')


