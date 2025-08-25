from time import strftime
from datetime import datetime
from flask import session
from functools import wraps
from sqlalchemy import create_engine, text
from sqlalchemy.sql import or_
from src.web.helpers.auth import user_is_login
from src.web.config import ProductionConfig, DevelopmentConfig
from src.core.usuarios import find_user_by_email
from src.core.instituciones import find_institution_by_id


def user_instis():
    """
        Devuelve una lista de instituciones a las que pertenece el usuario.
    """
    if user_is_login():

        user = find_user_by_email(session["user"])
        user_id = user.id
        """
        engine = create_engine(
            ProductionConfig.SQLALCHEMY_DATABASE_URI
        )
        """
        engine = create_engine(
            DevelopmentConfig.SQLALCHEMY_DATABASE_URI)
        
        query = text(
            'SELECT institution_id FROM user_rol_inst WHERE user_id = :user_id')

        with engine.connect() as con:
            result = con.execute(query, {"user_id": user_id})
            id_instituciones = [record[0] for record in result]

        instituciones = []
        for id in id_instituciones:
            institucion = find_institution_by_id(id)
            if institucion:
                instituciones.append(institucion)

        return instituciones


def add_instis_context(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        instituciones = user_instis()
        return f(instituciones, *args, **kwargs)
    return decorated_function


def get_filtered_service_requests(solicitudes, type_filter, status_filter, client_filter, start_date, end_date):
    """
        Filtra las solicitudes de acuerdo a los parámetros recibidos.
    """
    solicitudes_filtradas = []

    if start_date:
        fecha_inicio = datetime.strptime(start_date, "%Y-%m-%d")
    if end_date:
        fecha_fin = datetime.strptime(end_date, "%Y-%m-%d")

    for solicitud in solicitudes:

        if type_filter and solicitud.service.tipo != type_filter:
            continue
        if status_filter and solicitud.status != status_filter:
            continue
        if client_filter and (client_filter.lower() not in f"{solicitud.user.nombre} {solicitud.user.apellido}".lower()):
            continue
        if start_date and solicitud.request_date < fecha_inicio:
            continue
        if end_date and solicitud.request_date > fecha_fin:
            continue

        solicitudes_filtradas.append(solicitud)
    print(solicitudes_filtradas)
    return solicitudes_filtradas
