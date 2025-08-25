from src.core.servicios.service import Service, serv_insti
from src.core.servicios.key_word import Key_Word_Serv
from src.core.instituciones.institution import Institution
from src.core.database import db
from sqlalchemy import func


def list_services():
    """Retorna los servicios"""
    return Service.query.all()


def list_services_filter_by_search(q):
    """Retorna los servicios cuyo nombre o descripcion coincidan o sean parecidos a q"""
    return Service.query.filter((Service.nombre.like(f"%{q}%")) | (Service.descripcion.like(f"%{q}%"))).all()


def list_services_filter_by_search_and_type(q, type):
    """Retorna los servicios cuyo nombre o descripcion coincidan o sean parecidos a q, y sean iguales al tipo ingresado por parámetro"""
    query = Service.query.filter_by(tipo=type)
    query = query.filter((Service.nombre.like(f"%{q}%")) | (
        Service.descripcion.like(f"%{q}%")))
    services = query.all()
    return services


def create_service(**kwargs):
    """Inserta en la bd"""
    service = Service(**kwargs)
    db.session.add(service)
    db.session.commit()

    return service


def create_key_word_serv(**kwargs):
    """Inserta en la bd"""
    key_word_serv = Key_Word_Serv(**kwargs)
    db.session.add(key_word_serv)
    db.session.commit()

    return key_word_serv


def assign_keyword_serv(service, keyword):
    """Agrega palabras claves al servicio"""
    service.palabras_clave.extend(keyword)
    db.session.add(service)
    db.session.commit()
    return service


def assign_institution_service(service, institution):
    """Asigna instituciones a cargo de un servicio"""
    service.centrosACargo.extend(institution)
    db.session.add(service)
    db.session.commit()
    return service


def update_service(service):
    """Actualiza un servicio"""
    db.session.add(service)
    db.session.commit()

    return service


def delete_service(id):
    """Elimina un servicio"""
    try:
        eliminado = db.session.query(Service).get(id)
        service = Service.query.get(id)
        db.session.delete(service)
        db.session.commit()
        return eliminado
    except:
        db.session.rollback()


def update_service(service):
    """Actualiza un servicio"""
    db.session.add(service)
    db.session.commit()

    return service


def get_servicio_id(id):
    """Busca un servicio por su ID"""
    service = db.session.query(Service).get(id)

    return service


def buscar_servicio_por_nombre(nombre):
    """Busca un servicio por su nombre"""
    return Service.query.filter_by(nombre=nombre).first()


def buscar_palabra_por_nombre(nombre):
    """Busca una palabra por su nombre"""
    return Key_Word_Serv.query.filter_by(name=nombre).first()


def desvincular_palabra_clave(service, keyword):
    """Desvincula una palabra clave del servicio"""
    service.palabras_clave.remove(keyword)
    db.session.add(service)
    db.session.commit()
    return service


def desvincular_centro(service, institution):
    """Desvincula un centro de un servicio"""
    service.centrosACargo.remove(institution)
    db.session.add(service)
    db.session.commit()
    return service


def listar_con_palabras_centros():
    """Retorna el servicio, sus palabras clave y centros a cargo"""
    servicios = Service()
    servicios = (db.session.query(Service).outerjoin(
        Key_Word_Serv, Service.palabras_clave).outerjoin(Institution, Service.centrosACargo))
    return servicios


def get_centros_a_cargo(id):
    """Retorna los centros a cargo de un servicio cuyo id fue recibido por parametro"""
    service = Service.query.get(id)
    return service.centrosACargo


def comprobar_vinculo_servicio_institucion(id_service, id_institution):
    """Retorna boolean, cuyo valor es determinado si la relacion entre un servicio y una institucion existe"""
    if db.session.query(serv_insti).filter_by(service_id=id_service, institution_id=id_institution).first():
        return True
    else:
        return False


def buscar_servicio_por_nombre_repetido(nombre, exclude_id=None):
    """Busca si hay otro servicio con el mismo nombre globalmente"""
    q = Service.query.filter(
        func.lower(Service.nombre) == func.lower((nombre or "").strip())
    )
    if exclude_id is not None:
        q = q.filter(Service.id != exclude_id)
    return q.first()  # None si no hay repetido

