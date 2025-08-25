"""Modulo que provee el modelo de la configuracion"""
from datetime import datetime
from src.core.database import db


class Configuration (db.Model):
    """Modelo de configuracion"""
    __tablename__ = 'configuration'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    items_por_pagina = db.Column(db.Integer)
    info_contacto = db.Column(db.String(50))
    mantenimiento_modo = db.Column(db.Boolean)
    mantenimiento_mensaje = db.Column(db.String(100))

    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    inserted_at = db.Column(db.DateTime, default=datetime.utcnow)
