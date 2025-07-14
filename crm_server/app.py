import os
from flask import Flask, request, jsonify, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import logging
import json
from flask_cors import CORS

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///notifications.db')  # Fallback for dev
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-secret-key') 
SECRET_TOKEN = os.getenv('SECRET_TOKEN', 'default-token')  
CORS(app)  

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String, nullable=False)
    user = db.Column(db.String, nullable=False)
    event = db.Column(db.String, nullable=False)
    facilitator_id = db.Column(db.String, nullable=False)
    received_at = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

@app.route('/notify', methods=['POST'])
def notify():
    current_app.logger.info("Received notification request")
    
    # auth_header = request.headers.get('Authorization')
    # if not auth_header or not auth_header.startswith("Bearer "):
    #     current_app.logger.warning("Missing or invalid Authorization header")
    #     return jsonify({"error": "Missing or invalid Authorization header"}), 401

    # token = auth_header.split(" ")[1]
    # if token != current_app.config.get('SECRET_TOKEN'):
    #     current_app.logger.warning("Unauthorized access attempt")
    #     return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()
    if not data:
        current_app.logger.error("Missing JSON body")
        return jsonify({"error": "Missing JSON body"}), 400

    required_fields = ["session_id", "user", "event", "facilitator_id"]
    missing = [field for field in required_fields if field not in data]
    if missing:
        current_app.logger.error(f"Missing fields: {', '.join(missing)}")
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    # Validate user object structure
    if not isinstance(data["user"], dict) or not all(key in data["user"] for key in ["id", "name"]):
        current_app.logger.error("Invalid user object structure")
        return jsonify({"error": "User object must contain id and name"}), 400

    try:
        notification = Notification(
            session_id=data["session_id"],
            user=json.dumps(data["user"]), 
            event=data["event"],
            facilitator_id=data["facilitator_id"]
        )
        db.session.add(notification)
        db.session.commit()
        current_app.logger.info(f"Notification stored for session_id: {data['session_id']}")
        return jsonify({"message": "Facilitator notified and stored"}), 200
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error saving notification: {str(e)}")
        return jsonify({"error": f"Failed to save notification: {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5001)) 
    app.run(host='0.0.0.0', port=port, debug=os.getenv('FLASK_ENV') == 'development')