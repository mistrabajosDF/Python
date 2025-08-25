from flask import Blueprint
from flask import jsonify, request, session
from collections import defaultdict
from src.web.controllers.auth import generar_token, validar_token, validar_token_no_json
from src.core import instituciones, servicios
from src.core.usuarios import check_user, find_user_by_email
from src.core.servicios import get_servicio_id, comprobar_vinculo_servicio_institucion, list_services_filter_by_search, list_services_filter_by_search_and_type
from src.core.solicitudes import list_requests_with_servs, get_request_by_user_and_id_request, create_user_service_request_with_user_and_data, create_note_with_request_and_description, get_all_requests, list_notes_by_request_id
from src.core.instituciones import get_institucion_id
from src.core.rol_y_permiso import obtener_rol_del_usuario_en_institucion, obtener_permisos
from src.web.schemas.schemas import institutions_schema, institution_schema, user_schema, service_schema, request_schema, requests_schema, services_schema, create_note_schema, requests_serv_schema, note_schema
import json
from src.core import configuracion


# from src.web.schemas.issue import errores_schema, services_type_schema

api_issue_bp = Blueprint("issues_api", __name__, url_prefix="/api")


@api_issue_bp.get("/")
def home():
    """Endpoint de la API que sirve para comprobar su funcionamiento"""
    data = {"status": "ok"}
    return jsonify(data), 200


@api_issue_bp.post("/auth")
def obtener_autenticacion():
    """Función que sirve para crear un nuevo token, en base a un mail y contraseña pasados por body"""
    user = request.json['user']
    password = request.json['password']
    if check_user(user, password):
        token = str(generar_token(data=request.get_json())).split("'")[1]
        return jsonify({"token": token}), 200
    else:
        return jsonify({"error": "usuario no encontrado"}), 400


@api_issue_bp.get("/validate")
def verificar_autenticacion_api():
    """Función que sirve para comprobar que un token sea valido, siempre y cuando se incluya este token en el header Authorization. Pero utilizando una ruta"""
    token = request.headers['Authorization']
    if token == None:
        return jsonify({"error": "Parámetros inválidos"}), 400
    return validar_token(token, salida=True)


@api_issue_bp.get("/services-types")
def obtener_tipos_de_servicios():
    """Función para obtener los tipos de servicios."""
    data = {"data": ["Analisis", "Consultoria", "Desarrollo"]}
    return jsonify(data), 200


@api_issue_bp.get("/institutions")
def obtener_instituciones():
    """Lista las instituciones en formato JSON a partir de los parametros page y per_page que recibe en la URL, para la api"""
    pagina = request.args.get('page', type=int)
    por_pagina = request.args.get('per_page', type=int)
    if (pagina and por_pagina is not None):
        inicio = por_pagina*(pagina-1)+1
        fin = por_pagina*pagina
        institutions = instituciones.list_institutions()
        instituciones_mostradas = institutions[inicio-1:fin]
        if instituciones_mostradas != []:
            # Con dumps sale ordenado, con dump sale mas bonito(?
            data = institutions_schema.dump(instituciones_mostradas)
            return data, 200
        else:
            return {'Error': 'Ya no hay valores para esta página'}, 404
    else:
        inicio = 1
        fin = 1
        institutions = instituciones.list_institutions()
        instituciones_mostradas = institutions[inicio-1:fin]
        if instituciones_mostradas != []:
            # Con dumps sale ordenado, con dump sale mas bonito(?
            data = institutions_schema.dump(instituciones_mostradas)
            return data, 200


@api_issue_bp.get("/me/profile")
def obtener_informacion_perfil():
    """Función para obtener datos de mi perfil. Requiere token de autenticación."""
    if 'Authorization' in request.headers:
        token = request.headers['Authorization']
        if (validar_token_no_json(token)):
            dict_usuario = validar_token(token, salida=True)
            data = find_user_by_email(dict_usuario["user"])
            usuario = user_schema.dump(data)
            return jsonify(usuario), 200
        else:
            data = {"error": "Parámetros inválidos"}
            return jsonify(data), 400
    else:
        data = {"error": "Falta autorización"}
        return jsonify(data), 401


@api_issue_bp.get("/me/requests")
def obtener_solicitudes():
    """
    Funcion para obtener todas las solicitudes de un usuario. Requiere token de autenticación. 
    Valores opcionales: 
    - page: página actual
    - per_page: cantidad de elementos por página
    - sort: ordenado por el criterio elegido (por estado, por fecha)
    - order: asc (ascendente) o desc (descendente)
    """
    if 'Authorization' in request.headers:
        token = request.headers['Authorization']
        if (validar_token_no_json(token)):
            # obtener usuario
            dict_usuario = validar_token(token, salida=True)
            data = find_user_by_email(dict_usuario["user"])

            # obtener solicitudes del usuario
            solicitudes = list_requests_with_servs(data.id)

            # ver los parametros utilizados
            pagina = request.args.get('page', default=1, type=int)
            por_pagina = request.args.get('per_page', default=10, type=int)
            sort = request.args.get('sort', default='id')
            order = request.args.get('order', default='asc')  # desc o asc

            if (pagina and por_pagina) is not None:
                inicio = por_pagina*(pagina-1)+1
                fin = por_pagina*pagina
            else:
                inicio = 1
                fin = 1

            # orden y criterio por el cual se ordena
            if sort:
                if sort == 'status' and all(hasattr(solicitud, 'status') for solicitud in solicitudes):
                    solicitudes = sorted(solicitudes, key=lambda solicitud: getattr(
                        solicitud, sort), reverse=(order == "desc"))
                elif sort == "fecha" and all(hasattr(solicitud, 'request_date') for solicitud in solicitudes):
                    solicitudes = sorted(solicitudes, key=lambda solicitud: getattr(
                        solicitud, sort), reverse=(order == "desc"))
                else:
                    solicitudes = sorted(solicitudes, key=lambda solicitud: solicitud.id, reverse=(
                        order.lower() == 'desc'))

            solicitudes_organizadas = solicitudes[inicio-1:fin]
            soli_hecha = requests_serv_schema.dump(solicitudes_organizadas)
            return soli_hecha, 200
        else:
            data = {"error": "Parámetros inválidos"}
            return jsonify(data), 400, {'Content-Type': 'application/json'}
    else:
        data = {"error": "Falta autorización"}
        return jsonify(data), 401


@api_issue_bp.get("/me/requests/<int:id>")
def obtener_solicitud(id):
    """Funcion para obtener una solicitud determinada. Requiere token de autenticación."""
    if 'Authorization' in request.headers:
        token = request.headers['Authorization']
        if (validar_token_no_json(token)):
            dict_usuario = validar_token(token, salida=True)
            data = find_user_by_email(dict_usuario["user"])
            solicitud = get_request_by_user_and_id_request(data.id, id)
            soli_hecha = request_schema.dump(solicitud)
            return soli_hecha, 200
        else:
            data = {"error": "Parámetros inválidos"}
            return jsonify(data), 400
    else:
        data = {"error": "Falta autorización"}
        return jsonify(data), 401


@api_issue_bp.get("/all_services")
def services():
    """Retorna, en formato JSON, todos los servicios de todas las instituciones"""
    services = servicios.list_services()
    data = services_schema.dump(services)
    return jsonify(data), 200


@api_issue_bp.post("/me/requests")
def crear_solicitud():
    """Funcion para crear una solicitud determinada. Requiere token de autenticación. En el body del request se requiere: service_id, institution_id, request_date, status, change_status_date, observation"""
    if 'Authorization' in request.headers:
        token = request.headers['Authorization']
        if (validar_token_no_json(token) and comprobar_vinculo_servicio_institucion(request.json['service_id'], request.json['institution_id'])):
            dict_usuario = validar_token(token, salida=True)
            data = find_user_by_email(dict_usuario["user"])
            user_id = data.id
            solicitud = create_user_service_request_with_user_and_data(user_id, request.json)
            soli_hecha = request_schema.dump(solicitud)
            return soli_hecha, 201
        else:
            data = {"error": "Parámetros inválidos"}
            return jsonify(data), 400
    else:
        data = {"error": "Falta autorización"}
        return jsonify(data), 401


@api_issue_bp.post("/me/requests/<int:id>/notes")
def crear_nota(id):
    """Funcion para crear una nota para una solicitud cuya id es pasada por la url. Requiere token de autenticación. En el body del request se requiere: text"""
    if 'Authorization' in request.headers:
        token = request.headers['Authorization']
        if (validar_token_no_json(token)):
            dict_usuario = validar_token(token, salida=True)
            data = find_user_by_email(dict_usuario["user"])
            request_id = id
            if get_request_by_user_and_id_request(data.id, request_id) == []:
                data = {"error": "La solicitud no existe"}
                return jsonify(data), 400
            description = request.json['text']
            nota = create_note_with_request_and_description(
                request_id, description)
            nota_nueva = create_note_schema.dump(nota)
            return nota_nueva, 200
        else:
            data = {"error": "Parámetros inválidos"}
            return jsonify(data), 400
    else:
        data = {"error": "Falta autorización"}
        return jsonify(data), 401


@api_issue_bp.get("/me/requests/<int:id>/notes/")
def obtener_notas(id):
    """Funcion para obtener las notas de una solicitud determinada. Requiere token de autenticación."""
    if 'Authorization' in request.headers:
        token = request.headers['Authorization']
        if (validar_token_no_json(token)):
            request_id = id
            notas = list_notes_by_request_id(request_id)
            print(notas)
            notas_nuevas = note_schema.dump(notas, many=True)
            print(notas_nuevas)
            return notas_nuevas, 200
        else:
            data = {"error": "Parámetros inválidos"}
            return jsonify(data), 400
    else:
        data = {"error": "Falta autorización"}
        return jsonify(data), 401


@api_issue_bp.get("/services/search")
def obtener_servicios():
    """
    Funcion para obtener servicios filtrado por el criterio de búsqueda.
    Valor obligatorio:
    - q: ordenado por el criterio elegido
    Valores opcionales:
    - type: tipo de busqueda de servicio (Consultoría, Análisis o Desarrollo)
    - page: página actual
    - per_page: cantidad de elementos por página
    """
    # ver los parametros utilizados
    pagina = request.args.get('page', type=int)
    por_pagina = request.args.get('per_page', type=int)
    q = request.args.get('q')
    type = request.args.get('type')  # desc o asc
    if q is None:
        data = {"error": "Parámetros inválidos"}
        return jsonify(data), 400
    if pagina and por_pagina is not None:
        inicio = por_pagina*(pagina-1)+1
        fin = por_pagina*pagina
    else:
        inicio = 1
        fin = 1
    if type is None:
        servicios_obtenidos = list_services_filter_by_search(q)
    else:
        servicios_obtenidos = list_services_filter_by_search_and_type(q, type)
    servicios_paginados = servicios_obtenidos[inicio-1:fin]
    servicios_nuevos = services_schema.dump(servicios_paginados)
    return servicios_nuevos, 200


@api_issue_bp.get("/services/<int:id>")
def obtener_servicio(id):
    """Funcion para obtener un servicio determinado."""
    servicio = get_servicio_id(id)
    data = service_schema.dump(servicio)
    return jsonify(data), 200


@api_issue_bp.get("/institutions/<int:id>")
def obtener_institucion(id):
    """Funcion para obtener una institución determinada."""
    insti = get_institucion_id(id)
    data = institution_schema.dump(insti)
    return jsonify(data), 200


@api_issue_bp.get("/graphics/1")
def cantidad_solicitudes_por_estado():
    """Función para obtener la cantidad de solicitudes por cada estado. Requiere autorización."""
    if 'Authorization' in request.headers:
        token = request.headers['Authorization']
        if (validar_token_no_json(token)):
            lista_solicitudes = get_all_requests()
            # a todos los enteros les pone valor por defecto 0
            solicitudes = defaultdict(int)
            for solicitud in lista_solicitudes:
                print(solicitud.status)
                solicitudes[solicitud.status] += 1
            resultado = [{"status": estado, "cantidad": cantidad}
                         for estado, cantidad in solicitudes.items()]
            json_resultado = json.dumps(resultado, indent=2)
            return json_resultado, 200
        else:
            data = {"error": "Parámetros inválidos"}
            return jsonify(data), 400
    else:
        data = {"error": "Falta autorización"}
        return jsonify(data), 401


@api_issue_bp.get("/graphics/2")
def servicios_mas_solicitados():
    """Función para obtener el ranking de los servicios mas solicitados. Requiere autorización."""
    if 'Authorization' in request.headers:
        token = request.headers['Authorization']
        if (validar_token_no_json(token)):
            lista_solicitudes = get_all_requests()
            # a todos los enteros les pone valor por defecto 0
            solicitudes = defaultdict(int)
            for solicitud in lista_solicitudes:
                solicitudes[solicitud.service_id] += 1
            solicitudes_ordenadas_desc = sorted(
                solicitudes.items(), key=lambda item: item[1], reverse=True)[:15]
            respuesta = []
            for service_id, cantidad in solicitudes_ordenadas_desc:
                servicio = get_servicio_id(service_id)
                respuesta.append(
                    {"servicio": servicio.nombre, "cantidad": cantidad})
            json_resultado = json.dumps(respuesta, indent=2)
            return json_resultado, 200
        else:
            data = {"error": "Parámetros inválidos"}
            return jsonify(data), 400
    else:
        data = {"error": "Falta autorización"}
        return jsonify(data), 401


@api_issue_bp.get("/graphics/3")
def instituciones_con_mas_solicitudes():
    """Función para obtener el top 10 con las instituciones con mas solicitudes. Requiere autorización."""
    if 'Authorization' in request.headers:
        token = request.headers['Authorization']
        if (validar_token_no_json(token)):
            lista_solicitudes = get_all_requests()
            # a todos los enteros les pone valor por defecto 0
            solicitudes = defaultdict(int)
            for solicitud in lista_solicitudes:
                solicitudes[solicitud.institution_id] += 1
            solicitudes_ordenadas_desc = sorted(
                solicitudes.items(), key=lambda item: item[1], reverse=True)[:10]
            respuesta = []
            for institution_id, cantidad in solicitudes_ordenadas_desc:
                institucion = get_institucion_id(institution_id)
                respuesta.append(
                    {"institucion": institucion.nombre, "cantidad": cantidad})
            json_resultado = json.dumps(respuesta, indent=2)
            return json_resultado, 200
        else:
            data = {"error": "Parámetros inválidos"}
            return jsonify(data), 400
    else:
        data = {"error": "Falta autorización"}
        return jsonify(data), 401


def coincidencia_insti(serv, insti):
    """Revisa si una institucion se encuentra en un servicio"""
    for c in serv.centrosACargo:
        if (insti in c.nombre.upper()):
            return True
    else:
        return False


def coincidencia_p(serv, palabra):
    """Revisa si una palabra se encuentra en un servicio"""
    for p in serv.palabras_clave:
        if (palabra in p.name.upper()):
            return True
    else:
        return False


@api_issue_bp.get("/filtrar_serv")
def filtrar_serv():
    """A partir de la ruta /api/filtrar_serv?i=&p=LATEx&n=&d=
    donde i = institucion, p = palabra, d = descripcion,
    devuelve los servicios que coinciden con la busqueda"""
    services = list(servicios.listar_con_palabras_centros())

    insti = request.args.get('i', type=str).upper()
    descripcion = request.args.get('d', type=str).upper()
    nombre = request.args.get('n', type=str).upper()
    tipo = request.args.get('t', type=str)
    palabra = (request.args.get('p', type=str)).upper()
    serv_filtro = []
    for serv in services:
        if (descripcion == "-") or (descripcion in serv.descripcion.upper()):
            if (insti == "-") or (coincidencia_insti(serv, insti)):
                if (palabra == "-") or (coincidencia_p(serv, palabra)):
                    if (nombre == "-") or (nombre in serv.nombre.upper()):
                        if (tipo == "-") or (serv.tipo == tipo):
                            serv_filtro.append(serv)

    if serv_filtro != []:
        data = services_schema.dump(serv_filtro)
        return data, 200
    else:
        return {'Error': 'No hay valores'}, 404


@api_issue_bp.get("/permisos_institucion")
def permisos_por_institucion():
    rol = obtener_rol_del_usuario_en_institucion("violet@gmail.com", 2)
    print(rol)
    permisos = obtener_permisos(rol)
    print(permisos)
    data = {"rol": rol, "permisos_asociados": permisos}
    return jsonify(data), 200


@api_issue_bp.get("/contact")
def info_contacto():
    """Retona la informacion de contacto"""
    config = configuracion.get_configuration()
    return {'info_contacto': config.info_contacto}
    