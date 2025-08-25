from datetime import datetime
from src.core.database import db


institution_keyword = db.Table(
    'institution_keyword',
    db.Column('institution_id', db.Integer, db.ForeignKey(
        'institutions.id'), primary_key=True),
    db.Column('keyword_id', db.Integer, db.ForeignKey(
        'key_words.id'), primary_key=True),
)


class Institution (db.Model):
    __tablename__ = "institutions"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    nombre = db.Column(db.String(50), unique=True)
    informacion = db.Column(db.String(100))
    direccion = db.Column(db.String(100))
    localizacion = db.Column(db.String(100))
    paginaweb = db.Column(db.String(50))
    palabrasclave = db.relationship('Key_Word', secondary=institution_keyword)
    diasyhorarios = db.Column(db.String(100))
    contacto = db.Column(db.String(50))
    habilitada = db.Column(db.Boolean)

    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    inserted_at = db.Column(db.DateTime, default=datetime.utcnow)
