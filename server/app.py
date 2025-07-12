from flask import Flask
from flask_cors import CORS
from config import Config
from models import db
from routes.user.route import auth_bp
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)
db.init_app(app)

app.register_blueprint(auth_bp)

oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=Config.GOOGLE_CLIENT_ID,
    client_secret=Config.GOOGLE_CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)

app.oauth = oauth
app.google = google

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
