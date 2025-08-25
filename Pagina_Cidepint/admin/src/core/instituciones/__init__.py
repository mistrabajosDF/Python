from src.core.instituciones.institution import Institution
from src.core.instituciones.key_word import Key_Word
from src.core.database import db
from sqlalchemy import func


def list_institutions():
    """Retorna las instituciones"""
    return Institution.query.all()


def create_institution(**kwargs):
    """Inserta en la bd"""
    institution = Institution(**kwargs)
    db.session.add(institution)
    db.session.commit()

    return institution


def create_key_word(**kwargs):
    """Inserta en la bd"""
    key_word = Key_Word(**kwargs)
    db.session.add(key_word)
    db.session.commit()

    return key_word


def assign_keyword(institution, keyword):
    """Agrega palabras claves a la institucion"""
    institution.palabrasclave.extend(keyword)
    db.session.add(institution)
    db.session.commit()

    return institution


def update_institution(institution):
    """Actualiza una institucion"""
    db.session.add(institution)
    db.session.commit()

    return institution


def delete_insitutution(id):
    """Elimina una institucion"""
    try:
        eliminada = db.session.query(Institution).get(id)
        institution = Institution.query.get(id)
        db.session.delete(institution)
        db.session.commit()
        return eliminada
    except:
        db.session.rollback()


def get_institucion_id(id):
    """Busca una institucion por su ID"""
    institucion = db.session.query(Institution).get(id)

    return institucion


def buscar_institucion_por_nombre(nombre):
    """Busca una institucion por su nombre"""
    return Institution.query.filter_by(nombre=nombre).first()


def buscar_palabra_por_nombre(nombre):
    """Busca una palabra por su nombre"""
    return Key_Word.query.filter_by(name=nombre).first()


def desvincular_palabra_clave(institution, keyword):
    """Desvincula palabras claves de la institucion"""
    institution.palabrasclave.remove(keyword)
    db.session.add(institution)
    db.session.commit()

    return institution


def listar_con_palabras():
    """Retorna la institucion y sus palabras clave"""
    instituciones = Institution()
    instituciones = (db.session.query(Institution).outerjoin(
        Key_Word, Institution.palabrasclave))

    return instituciones


def find_institution_by_id(id):
    """Retorna una institucion de la bd"""
    return Institution.query.get(id)


def buscar_institucion_por_nombre_repetido(nombre, exclude_id=None):
    """Busca si hay otra institución con el mismo nombre globalmente"""
    q = Institution.query.filter(
        func.lower(Institution.nombre) == func.lower((nombre or "").strip())
    )
    if exclude_id is not None:
        q = q.filter(Institution.id != exclude_id)
    return q.first()  # None si no hay repetido