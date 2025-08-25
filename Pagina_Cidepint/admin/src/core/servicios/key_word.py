from datetime import datetime
from src.core.database import db


class Key_Word_Serv (db.Model):
    __tablename__ = 'key_words_serv'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(50))

    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    inserted_at = db.Column(db.DateTime, default=datetime.utcnow)
