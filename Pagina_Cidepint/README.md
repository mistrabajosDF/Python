### Trabajo final grupal: Sistema para CIDEPINT. 

## Funcionalidades:
    Buscador de servicios ofrecidos por las instituciones.
    Dar de alta organizaciones y publicar los servicios que ofrecen.
    Realizar un pedido de servicio: los usuarios podrán solicitar un servicio.
	Gestión de usuarios.
	API.

## Tecnoogías:

Aplicación de administración en Python y Flask

Portal en Vue.js

Base de datos PostgreSQL

## Comandos:
flask resetbd: Elimina y crea la BD
flask seedsdb: Carga la BD con datos de prueba
flask run: Corre el sistema en http://127.0.0.1:5000, control + c para detener
Opcional, antes de flask run, $env:FLASK_DEBUG=1

## Usuarios de prueba:
Rol propietario:
        email="propietario@gmail.com",
        password="Contraseña.1",
Rol superadmin:
        email="superadmin@gmail.com",
        password="Contraseña.1",
Rol admin
        email="admin@gmail.com",
        password="Contraseña.1",
Rol operador
        email="operador@gmail.com",
        password="Contraseña.1",
