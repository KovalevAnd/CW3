from project.dao.models.base import BaseMixin
from project.setup_db import db
import hashlib


class User(BaseMixin, db.Model):
    __tablename__ = "users"

    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    surname = db.Column(db.String(100))
    favorite_genre = db.Column(db.String(100))

    def get_hash(self):
        return hashlib.md5(self.encode('utf-8')).hexdigest()

    def __repr__(self):
        return f"<User '{self.email.title()}'>"
