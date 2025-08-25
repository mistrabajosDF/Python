from datetime import datetime
from src.core.database import db


rol_permission = db.Table(
    'rol_permission',
    db.Column('role_id', db.Integer, db.ForeignKey(
        'roles.id'), primary_key=True),
    db.Column('permission_id', db.Integer, db.ForeignKey(
        'permissions.id'), primary_key=True),
)


class Role (db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(50))
    permissions = db.relationship('Permission', secondary=rol_permission)

    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    inserted_at = db.Column(db.DateTime, default=datetime.utcnow)
