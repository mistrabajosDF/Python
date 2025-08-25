from src.core.database import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from src.core.usuarios.user import User
from src.core.servicios.service import Service


class User_Service_Request(db.Model):
    __tablename__ = 'user_service_requests'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'))
    user = relationship("User", primaryjoin=user_id == User.id)
    service_id = db.Column(db.Integer, ForeignKey('services.id'))
    service = relationship("Service", primaryjoin=service_id == Service.id)
    institution_id = db.Column(db.Integer, db.ForeignKey('institutions.id'))
    request_date = db.Column(db.DateTime)
    status = db.Column(db.String(50), default='Pendiente')
    change_status_date = db.Column(db.DateTime)
    observation = db.Column(db.String(250))
    obs_est_act = db.Column(db.String(100))

    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    inserted_at = db.Column(db.DateTime, default=datetime.utcnow)

    def as_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "service_id": self.service_id,
            "institution_id": self.institution_id,
            "request_date": self.request_date,
            "status": self.status,
            "change_status_date": self.change_status_date,
            "observation": self.observation,
            "updated_at": self.updated_at,
            "inserted_at": self.inserted_at
        }
