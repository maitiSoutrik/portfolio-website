from flask_sqlalchemy import SQLAlchemy

# Create the SQLAlchemy instance
db = SQLAlchemy()

def init_db(app):
    """Initialize the SQLAlchemy app"""
    db.init_app(app)

    # Import models here to avoid circular imports
    from models import Contact, BlogPost  # noqa

    with app.app_context():
        # Create all tables
        db.create_all()