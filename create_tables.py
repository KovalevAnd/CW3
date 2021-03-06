from project.config import DevelopmentConfig
from project.dao.models import base, director, genre, movie, user  # noqa F401, F403
from f import create_app
from project.setup_db import db

app = create_app(DevelopmentConfig)

with app.app_context():
    db.drop_all()
    db.create_all()
