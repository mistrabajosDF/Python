from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from src.core.solicitudes.user_service_request import User_Service_Request
from src.core.database import db


class Note (db.Model):
    __tablename__ = 'notes'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    request_id = db.Column(db.Integer, ForeignKey('user_service_requests.id'))
    request = relationship("User_Service_Request",
                           primaryjoin=request_id == User_Service_Request.id)
    description = db.Column(db.String(250))

    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    inserted_at = db.Column(db.DateTime, default=datetime.utcnow)

    def as_dict(self):
        return {
            "id": self.id,
            "request_id": self.request_id,
            "description": self.description,
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            "inserted_at": self.inserted_at.strftime("%Y-%m-%d %H:%M:%S")
        }
