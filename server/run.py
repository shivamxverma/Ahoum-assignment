from app import create_app
from server.database import db

app = create_app()

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(port=5000, debug=True)
