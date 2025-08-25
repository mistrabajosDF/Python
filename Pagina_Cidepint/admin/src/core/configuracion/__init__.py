"""Modulo que provee la funcionalidad para la configuracion"""
from src.core.configuracion.configuration import Configuration
from src.core.database import db


def listar():
    """Retorna las instituciones"""
    return Configuration.query.all()

def load_configuration(**kwargs):
    """carga/crea la configuracion"""
    config = Configuration(**kwargs)
    db.session.add(config)
    db.session.commit()


def get_configuration():
    """Retorna la configuracion actual de la página"""
    return db.session.query(Configuration).get(1)


def update(config):
    """Actualiza la configuracion en la bd"""
    db.session.add(config)
    db.session.commit()


def item_per_page():
    """Retorna la paginacion"""
    return (Configuration.query.order_by(Configuration.items_por_pagina).first()).items_por_pagina
