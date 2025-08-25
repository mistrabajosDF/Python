from src.core import instituciones, servicios, usuarios, rol_y_permiso, solicitudes, configuracion
from datetime import datetime


def run():

    config = configuracion.load_configuration(
        items_por_pagina=5,
        info_contacto="admin@pinturapp.com",
        mantenimiento_modo=False,
        mantenimiento_mensaje="El sitio está en mantenimiento, visítenos más tarde",
    )

    # roles
    role_superadmin = rol_y_permiso.create_role(
        name="superadmin",
    )
    role_owner = rol_y_permiso.create_role(
        name="owner",
    )
    role_admin = rol_y_permiso.create_role(
        name="admin",
    )
    role_operator = rol_y_permiso.create_role(
        name="operator",
    )

    # permisos
    p1 = rol_y_permiso.create_permission(
        title="user_index",
    )
    p2 = rol_y_permiso.create_permission(
        title="user_new",
    )
    p3 = rol_y_permiso.create_permission(
        title="user_destroy",
    )
    p4 = rol_y_permiso.create_permission(
        title="user_update",
    )
    p5 = rol_y_permiso.create_permission(
        title="user_show",
    )
    p6 = rol_y_permiso.create_permission(
        title="inst_index",
    )
    p7 = rol_y_permiso.create_permission(
        title="inst_show",
    )
    p8 = rol_y_permiso.create_permission(
        title="inst_update",
    )
    p9 = rol_y_permiso.create_permission(
        title="inst_create",
    )
    p10 = rol_y_permiso.create_permission(
        title="inst_destroy",
    )
    p11 = rol_y_permiso.create_permission(
        title="inst_activate",
    )
    p12 = rol_y_permiso.create_permission(
        title="inst_deactivate",
    )
    p13 = rol_y_permiso.create_permission(
        title="serv_index",
    )
    p14 = rol_y_permiso.create_permission(
        title="serv_show",
    )
    p15 = rol_y_permiso.create_permission(
        title="serv_update",
    )
    p16 = rol_y_permiso.create_permission(
        title="serv_create",
    )
    p17 = rol_y_permiso.create_permission(
        title="serv_destroy",
    )
    p18 = rol_y_permiso.create_permission(
        title="req_index",
    )
    p19 = rol_y_permiso.create_permission(
        title="req_show",
    )
    p20 = rol_y_permiso.create_permission(
        title="req_update",
    )
    p21 = rol_y_permiso.create_permission(
        title="req_destroy",
    )
    p22 = rol_y_permiso.create_permission(
        title="config_show",
    )
    p23 = rol_y_permiso.create_permission(
        title="config_update",
    )
    p24 = rol_y_permiso.create_permission(
        title="admin_user_index",
    )
    p25 = rol_y_permiso.create_permission(
        title="admin_user_create",
    )
    p26 = rol_y_permiso.create_permission(
        title="admin_user_destroy",
    )
    p27 = rol_y_permiso.create_permission(
        title="admin_user_update",
    )



    # usuarios
    user1 = usuarios.create_user(
        nombre="Mikasa",
        apellido="Ackerman",
        email="propietario@gmail.com",
        username="mika",
        password="Contraseña.1",
        activo=True,
    )
    user2 = usuarios.create_user(
        nombre="Kakashi",
        apellido="Hatake",
        email="superadmin@gmail.com",
        username="kakashi",
        password="Contraseña.1",
        activo=True,
    )
    user3 = usuarios.create_user(
        nombre="Tanjiro",
        apellido="Kamado",
        email="admin@gmail.com",
        username="tanji",
        password="Contraseña.1",
        activo=True,
    )
    user4 = usuarios.create_user(
        nombre="Violet",
        apellido="Evergarden",
        email="operador@gmail.com",
        username="violete",
        password="Contraseña.1",
        activo=True,
    )

    user5 = usuarios.create_user(
        nombre="Iroh",
        apellido="Superadmin2",
        email="superadmin2@gmail.com",
        username="iroh",
        password="Contraseña.1",
        activo=True,
    )

    user6 = usuarios.create_user(
        nombre="Emmett",
        apellido="Brown",
        email="docbrown@gmail.com",
        username="docbrown",
        password="Contraseña.1",
        activo=True,
    )

    user7 = usuarios.create_user(
        nombre="Madara",
        apellido="Itachi",
        email="madara@gmail.com",
        username="madara",
        password="Contraseña.1",
        activo=True,
    )

    user8 = usuarios.create_user(
        nombre="Orochimaru",
        apellido="Sama",
        email="aguantenlasserpientes@gmail.com",
        username="orochi",
        password="Contraseña.1",
        activo=True,
    )

    # instituciones
    insti1 = instituciones.create_institution(
        nombre="Colorín",
        informacion="Expertos en latex",
        direccion="Calle falsa 1234",
        localizacion="-34.915948048256745, -57.9475188189177",
        paginaweb="www.colorin.com",
        diasyhorarios="lunes a viernes de 8 a 17",
        contacto="colorin@gmail.com",
        habilitada=True,
    )
    insti2 = instituciones.create_institution(
        nombre="Centro DOS",
        informacion="Pintan a domilicio",
        direccion="Avenida Siempreviva 742",
        localizacion="-34.90461643619342, -57.93910092100363",
        paginaweb="www.cuento.com",
        diasyhorarios="lunes a viernes de 8 a 13 y 17 a 20",
        contacto="0221-458621",
        habilitada=True,
    )
    insti3 = instituciones.create_institution(
        nombre="Industrias Stark ",
        informacion="Centro de alta tecnología",
        direccion="Avenida Colón 234, Buenos Aires",
        localizacion="-34.83897388749718, -58.370800490308795",
        paginaweb="http://industriasstark.com",
        diasyhorarios="Martes a sábados de 8 a 20",
        contacto="instagram.com/industriasStark",
        habilitada=True,
    )
    insti4 = instituciones.create_institution(
        nombre="Corporación Umbrella",
        informacion="Centro de pintura zombie",
        direccion="Avenida Alem 424, Bahía Blanca",
        localizacion="-38.696515701270734, -62.276863429840446",
        paginaweb="umbrella.com",
        diasyhorarios="Lunes a jueves de 8 a 16 hs",
        contacto=" ",
        habilitada=True,
    )

    # servicios
    serv1 = servicios.create_service(
        nombre="Pintado de rejas",
        descripcion="Pintado de rejas con esmalte sintetico de color a eleccion",
        tipo="Consultoria",
        habilitado=True,
    )
    serv2 = servicios.create_service(
        nombre="Presupuesto",
        descripcion="Presupuesto de pintado",
        tipo="Analisis",
        habilitado=True,
    )
    serv3 = servicios.create_service(
        nombre="Pintado de cielorraso",
        descripcion="Pintado de cielorraso de yeso o placa con reparación de grietas",
        tipo="Desarrollo",
        habilitado=True,
    )
    serv4 = servicios.create_service(
        nombre="Analisis de pinturas",
        descripcion="Estudio de tipo de pinturas para una funcionalidad",
        tipo="Analisis",
        habilitado=True,
    )
    serv5 = servicios.create_service(
        nombre="Pintamos tu casa a domicilio",
        descripcion="Solo de colorin",
        tipo="Consultoría",
        habilitado=True,
    )

    # palabras clave
    palabra1 = instituciones.create_key_word(
        name="PINTURA",
    )
    palabra2 = instituciones.create_key_word(
        name="REJAS",
    )

    # palabras clave en institucion
    instituciones.assign_keyword(insti1, [palabra1])
    instituciones.assign_keyword(insti2, [palabra1, palabra2])
    instituciones.assign_keyword(insti1, [palabra2])

    # Palabras clave de servicios
    p1 = servicios.create_key_word_serv(
        name="ESMALTE",
    )
    p2 = servicios.create_key_word_serv(
        name="LATEX",
    )
    p3 = servicios.create_key_word_serv(
        name="RAPIDO",
    )
    p4 = servicios.create_key_word_serv(
        name="PRESUPUESTO",
    )

    # Palabras clave en servicios
    servicios.assign_keyword_serv(serv1, [p1, p4])
    servicios.assign_keyword_serv(serv2, [p1, p2])
    servicios.assign_keyword_serv(serv3, [p1, p3])
    servicios.assign_keyword_serv(serv4, [p2, p3])
    servicios.assign_keyword_serv(serv5, [p2, p4])

    # Centros a cargo de un servicio
    servicios.assign_institution_service(serv1, [insti1, insti3])
    servicios.assign_institution_service(serv2, [insti1, insti2])
    servicios.assign_institution_service(serv3, [insti1, insti2])
    servicios.assign_institution_service(serv4, [insti1, insti4])
    servicios.assign_institution_service(serv5, [insti1])

    # roles en usuarios
    usuarios.assign_institution_role(user1, insti1, role_owner)
    usuarios.assign_institution_role(user2, insti1, role_superadmin)
    usuarios.assign_institution_role(user3, insti1, role_admin)
    usuarios.assign_institution_role(user4, insti1, role_operator)

    usuarios.assign_institution_role(user1, insti2, role_owner)
    usuarios.assign_institution_role(user3, insti2, role_admin)
    usuarios.assign_institution_role(user4, insti2, role_operator)

    usuarios.assign_institution_role(user1, insti3, role_owner)
    usuarios.assign_institution_role(user3, insti3, role_admin)
    usuarios.assign_institution_role(user4, insti3, role_operator)

    usuarios.assign_institution_role(user1, insti4, role_owner)
    usuarios.assign_institution_role(user3, insti4, role_admin)
    usuarios.assign_institution_role(user4, insti4, role_operator)

    # solicitud de un usuario
    date_str1 = "2023-10-10"
    date_str2 = "2023-10-15"
    date_str3 = "2023-10-20"
    date_format = "%Y-%m-%d"

    solicitud1 = solicitudes.create_user_service_request(
        user_id=user2.id,
        service_id=serv1.id,
        institution_id=insti1.id,
        request_date=datetime.strptime(date_str1, date_format),
        status="Pendiente",
        observation="Buenas, quiero el servicio para antes del 4 de diciembre. Gracias",
        obs_est_act="",
    )
    solicitud2 = solicitudes.create_user_service_request(
        user_id=user2.id,
        service_id=serv1.id,
        institution_id=insti1.id,
        request_date=datetime.strptime(date_str2, date_format),
        status="Pendiente",
        observation="Hola, necesito el servicio con materiales de primera calidad",
        obs_est_act="",
    )
    solicitud3 = solicitudes.create_user_service_request(
        user_id=user2.id,
        service_id=serv2.id,
        institution_id=insti1.id,
        request_date=datetime.strptime(date_str3, date_format),
        status="Rechazada",
        observation="observacion",
    )
    solicitud4 = solicitudes.create_user_service_request(
        user_id=user1.id,
        service_id=serv3.id,
        institution_id=insti1.id,
        request_date=datetime.strptime(date_str3, date_format),
        status="Aceptada",
        observation="¿Me pueden pasar el presupuesto por favor?",
    )
    solicitud5 = solicitudes.create_user_service_request(
        user_id=user5.id,
        service_id=serv2.id,
        institution_id=insti3.id,
        request_date=datetime.strptime(date_str3, date_format),
        status="Aceptada",
        observation="Quisiera que se realice con materiales de primera calidad",
    )
    solicitud6 = solicitudes.create_user_service_request(
        user_id=user6.id,
        service_id=serv4.id,
        institution_id=insti4.id,
        request_date=datetime.strptime(date_str3, date_format),
        status="Aceptada",
        observation="En la semana paso por la sucursal para ultimar detalles",
    )
    solicitud7 = solicitudes.create_user_service_request(
        user_id=user4.id,
        service_id=serv3.id,
        institution_id=insti2.id,
        request_date=datetime.strptime(date_str3, date_format),
        status="Rechazada",
        observation="¿Me pueden pasar el presupuesto por favor?",
    )
    solicitud8 = solicitudes.create_user_service_request(
        user_id=user1.id,
        service_id=serv1.id,
        institution_id=insti3.id,
        request_date=datetime.strptime(date_str3, date_format),
        status="Rechazada",
        observation="Lo necesito para la semana que viene, gracias.",
    )
    solicitud9 = solicitudes.create_user_service_request(
        user_id=user4.id,
        service_id=serv2.id,
        institution_id=insti3.id,
        request_date=datetime.strptime(date_str3, date_format),
        status="Pendiente",
        observation="Me gustaría coordinar una reunión para hablar de esto. MG.",
    )


    # notas
    nota1 = solicitudes.create_note(
        request_id=solicitud1.id,
        description="Comprar materiales necesarios",
    )
    nota2 = solicitudes.create_note(
        request_id=solicitud1.id,
        description="Coordinar reunion",
    )
    nota3 = solicitudes.create_note(
        request_id=solicitud2.id,
        description="María habló con cliente",
    )
    nota4 = solicitudes.create_note(
        request_id=solicitud3.id,
        description="No estamos pudiendo encontrar al cliente",
    )
    nota5 = solicitudes.create_note(
        request_id=solicitud4.id,
        description="Hay que ir a ver el trabajo",
    )
    nota6 = solicitudes.create_note(
        request_id=solicitud5.id,
        description="Es necesario ajustar el presupuesto",
    )
