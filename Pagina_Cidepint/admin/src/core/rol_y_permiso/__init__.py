from src.core.rol_y_permiso.role import Role, rol_permission
from src.core.rol_y_permiso.permission import Permission
from src.core.usuarios.user import user_rol_inst, User
from src.core.database import db
from sqlalchemy.orm import aliased


def create_role(**kwargs):
    """Inserta un rol en la bd"""
    role = Role(**kwargs)
    db.session.add(role)
    db.session.commit()

    return role


def create_permission(**kwargs):
    """Inserta un permiso en la bd"""
    permission = Permission(**kwargs)
    db.session.add(permission)
    db.session.commit()

    return permission


def assign_permission(role, permisos):
    """Asigna permisos a un rol"""
    role.permissions.extend(permisos)
    db.session.add(role)
    db.session.commit()

    return role

def buscar_rol_por_nombre(nombre):
    """Busca un rol por su nombre"""
    return Role.query.filter_by(name=nombre).first()


def obtener_rol_del_usuario_en_institucion(user_email, institucion_id):
    """Obtiene el rol del usuario en la institucion (mail del usuario y de la institucion pasadas por parametro)"""
    usuario= User.query.filter_by(email=user_email).first()
    
    if usuario:
        # Accede a la relación 'rol' usando alias para la tabla intermedia 'user_rol_inst'
        UserRolInst = aliased(user_rol_inst)
        rol_en_institucion = db.session.query(Role).join(
            UserRolInst).filter(
                UserRolInst.c.user_id == usuario.id,
                UserRolInst.c.institution_id == institucion_id
            ).first()

        if rol_en_institucion:
            return rol_en_institucion.name
        else:
            return "rol no encontrado"
    else:
        return "usuario no encontrado"

def obtener_permisos(rol):
    """Obtiene los permisos que tiene determinado rol, pasado por parámetro"""
    rol = Role.query.filter_by(name=rol).first()
    permisos= []
    if rol:
        # Accede a los permisos asociados a ese rol
        permisos_del_rol = rol.permissions

        if permisos_del_rol:
            print(f"Los permisos asociados al rol '{rol.name}' son:")
            for permiso in permisos_del_rol:
                print(permiso.title)  # Suponiendo que el nombre del permiso está en un campo 'nombre'
                permisos.append(permiso.title)
            return permisos
        else:
            return "No hay permisos"
    else:
        return "Hay algo mal con el rol, no podemos obtener permisos"
    
def obtener_lista_permisos(user_email,institucion_id):
    """Función que retorna una lista con los permisos que tiene un usuario en una institucion en específico"""
    rol= obtener_rol_del_usuario_en_institucion(user_email, institucion_id)
    return obtener_permisos(rol)

def es_superadmin(user_email):
    usuario= User.query.filter_by(email=user_email).first()
    es_super= False
    if usuario:
        # Accede a la relación 'rol' usando alias para la tabla intermedia 'user_rol_inst'
        UserRolInst = aliased(user_rol_inst)
        rol_en_institucion = db.session.query(Role).join(
            UserRolInst).filter(
                UserRolInst.c.user_id == usuario.id
            ).all()

        for rol in rol_en_institucion:
            if(rol.name == 'superadmin'):
                es_super= True
                break
        return es_super
    else:
        print("Problemas en la busqueda, posiblemente usuario no encontrado")
        return es_super