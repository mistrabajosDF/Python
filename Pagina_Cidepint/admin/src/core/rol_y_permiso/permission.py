from datetime import datetime
from src.core.database import db


class Permission (db.Model):
    __tablename__ = "permissions"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    title = db.Column(db.String(100))

    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    inserted_at = db.Column(db.DateTime, default=datetime.utcnow)
