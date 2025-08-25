from datetime import datetime
from src.core.database import db

"""
Tabla que indica el rol dentro de una institución para un usuario
"""
user_rol_inst = db.Table(
    'user_rol_inst',
    db.Column('user_id', db.Integer, db.ForeignKey(
        'users.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey(
        'roles.id'), primary_key=True),
    db.Column('institution_id', db.Integer, db.ForeignKey(
        'institutions.id'), primary_key=True),
    db.UniqueConstraint('user_id', 'institution_id',
                        name='unique_user_institution')
)


class User (db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    nombre = db.Column(db.String(50))
    apellido = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(255))
    activo = db.Column(db.Boolean)
    rol = db.relationship('Role', secondary=user_rol_inst)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    inserted_at = db.Column(db.DateTime, default=datetime.utcnow)
