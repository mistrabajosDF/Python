from datetime import datetime
from src.core.database import db


service_keyword = db.Table(
    'service_keyword',
    db.Column('service_id', db.Integer, db.ForeignKey(
        'services.id'), primary_key=True),
    db.Column('keywordserv_id', db.Integer, db.ForeignKey(
        'key_words_serv.id'), primary_key=True),
)

serv_insti = db.Table(
    'serv_insti',
    db.Column('service_id', db.Integer, db.ForeignKey(
        'services.id'), primary_key=True),
    db.Column('institution_id', db.Integer, db.ForeignKey(
        'institutions.id'), primary_key=True),
)


class Service (db.Model):
    __tablename__ = "services"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    nombre = db.Column(db.String(50), unique=True)
    descripcion = db.Column(db.String(100))
    palabras_clave = db.relationship(
        'Key_Word_Serv', secondary=service_keyword)
    centrosACargo = db.relationship(
        'Institution', secondary=serv_insti, lazy='subquery')
    tipo = db.Column(db.String(50))
    habilitado = db.Column(db.Boolean)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    inserted_at = db.Column(db.DateTime, default=datetime.utcnow)
