import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
db = SQLAlchemy(app)
migrate = Migrate(app, db) 
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
SECRET_TOKEN = os.getenv('SECRET_TOKEN')

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
    
    print("Received notification request")
    # auth_header = request.headers.get('Authorization')
    # if not auth_header or not auth_header.startswith("Bearer "):
    #     return jsonify({"error": "Missing or invalid Authorization header"}), 401

    # token = auth_header.split(" ")[1]
    # if token != SECRET_TOKEN:
    #     return jsonify({"error": "Unauthorized"}), 403

    # data = request.get_json()
    # if not data:
    #     return jsonify({"error": "Missing JSON body"}), 400

    # required = ["booking_id", "user", "event", "facilitator_id"]
    # missing = [f for f in required if f not in data]
    # if missing:
    #     return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400
    
    
    # db.session.commit()

    # notification = Notification(
    #     session_id=data["session_id"],
    #     user=data["user"],
    #     event=data["event"],
    #     facilitator_id=data["facilitator_id"]
    # )
    # db.session.add(notification)
    # db.session.commit()

    return jsonify({"message": "Facilitator notified and stored"}), 200

if __name__ == '__main__':
    app.run(port=5001)
