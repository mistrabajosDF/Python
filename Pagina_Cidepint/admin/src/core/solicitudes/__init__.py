from src.core.solicitudes.user_service_request import User_Service_Request
from src.core.servicios.service import Service
from src.core.solicitudes.note import Note
from src.core.database import db
from sqlalchemy.orm import joinedload


def create_user_service_request(**kwargs):
    """Inserta una solicitud de servicio en la bd"""
    user_service_request = User_Service_Request(**kwargs)
    db.session.add(user_service_request)
    db.session.commit()

    return user_service_request


def create_user_service_request_with_user_and_data(user_id, data):
    """Inserta una solicitud de servicio en la bd"""
    user_service_request = User_Service_Request(user_id=user_id, **data)
    db.session.add(user_service_request)
    db.session.commit()

    return user_service_request


def create_note(**kwargs):
    """Inserta una nota en la bd"""
    note = Note(**kwargs)
    db.session.add(note)
    db.session.commit()

    return note


def create_note_with_request_and_description(request_id, description):
    """Inserta una nota en la bd"""
    note = Note(request_id=request_id, description=description)
    db.session.add(note)
    db.session.commit()

    return note


def get_solicitud_id(id):
    """Busca un servicio por su ID"""
    solicitud = db.session.query(User_Service_Request).get(id)
    return solicitud


def list_requests(id_user):
    """Retorna las solicitudes de servicios de un usuario"""
    if id_user:
        return User_Service_Request.query.filter_by(user_id=id_user).all()
    else:
        return []


def list_requests_with_servs(id_user):
    """Retorna las solicitudes de servicios de un usuario con información del servicio asociado"""
    if id_user:
        return (
            User_Service_Request.query
            .join(Service, User_Service_Request.service_id == Service.id)
            .add_columns(
                User_Service_Request.id, 
                User_Service_Request.status, 
                User_Service_Request.request_date, 
                User_Service_Request.change_status_date, 
                User_Service_Request.observation,
                User_Service_Request.obs_est_act,
                Service.nombre,
                Service.tipo)
            .filter(User_Service_Request.user_id == id_user)
            .all()
        )
    else:
        return []


def get_request_by_user_and_id_request(id_user, id_request):
    """Retorna una solicitud de servicio, realizadas por un usuario"""
    if id_user:
        return User_Service_Request.query.filter_by(user_id=id_user).filter_by(id=id_request).all()
    else:
        return []


def list_services_requests(id_inst):
    """Retorna una lista de solicitudes de servicio"""
    if id_inst:
        return User_Service_Request.query.filter_by(institution_id=id_inst).all()
    else:
        return []


def list_notes_by_request_id(id_req):
    """Retorna una lista de notas de una solicitud de servicio"""
    return Note.query.filter_by(request_id=id_req).all()


def get_request_by_id(id_req):
    """Retorna una solicitud de servicio por su id"""
    return User_Service_Request.query.get(id_req)


def solicitud_delete(id):
    '''Elimina una solicitud con el id recibido por parámetro de la base de datos'''
    eliminada = db.session.query(User_Service_Request).get(id)
    solicitud = User_Service_Request.query.get(id)
    db.session.delete(solicitud)
    db.session.commit()
    return eliminada


def eliminar_notas(id):
    """Elimina notas de una solicitud"""
    eliminadas = Note.query.filter_by(request_id=id).all()
    for nota in eliminadas:
        db.session.delete(nota)
        db.session.commit()
    return eliminadas


def get_all_requests():
    """Retorna todas las solicitudes"""
    return User_Service_Request.query.all()