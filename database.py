from flask_sqlalchemy import SQLAlchemy

# Create the SQLAlchemy instance without binding it to any specific app
db = SQLAlchemy()

def init_db(app):
    """Initialize the database with the Flask app"""
    db.init_app(app)

    with app.app_context():
        db.create_all()