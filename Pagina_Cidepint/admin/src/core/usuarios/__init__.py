from src.core.usuarios.user import User
from src.core.rol_y_permiso.role import Role
from src.core.database import db
from src.core.bcrypt import bcrypt
from src.core.usuarios.user import user_rol_inst


def user_index():
    """Retorna todos los usuarios"""
    return User.query.all()


def create_user(**kwargs):
    """Inserta el usuario pasado por parámetro a la base de datos"""
    hash = bcrypt.generate_password_hash(kwargs["password"].encode("utf-8"))
    kwargs.update(password=hash.decode("utf-8"))
    user = User(**kwargs)
    db.session.add(user)
    db.session.commit()

    return user


def find_user_by_email(email):
    """Función que retorna un usuario desde la base de datos o None, dependiendo si encuentra el email que es pasado por parámetro"""
    return User.query.filter_by(email=email).first()


def find_user_by_username(username):
    """Función que retorna un usuario desde la base de datos o None, dependiendo si encuentra el username que es pasado por parámetro"""
    return User.query.filter_by(username=username).first()


def check_user(email, password):
    """Función que retorna un usuario desde la base de datos o None, dependiendo de si encuentra al email que es pasado por parámetro y su contraseña es correcta"""
    user = find_user_by_email(email)
    print(user)
    passwords_equals = bcrypt.check_password_hash(
        user.password, password.encode("utf-8"))
    if user and passwords_equals and user.activo == True:
        return user
    else:
        return None


def user_update(user):
    '''Actualiza un usuario recibido por parámetro en la base de datos'''

    db.session.add(user)
    db.session.commit()


def user_delete(id):
    '''Elimina un usuario con el id recibido por parámetro de la base de datos'''
    try:
        eliminado = db.session.query(User).get(id)
        user = User.query.get(id)
        db.session.delete(user)
        db.session.commit()
        return eliminado
    except:
        db.session.rollback()


def user_show(id):
    '''Retorna un usuario con el id ingresado, en caso de que exista'''
    user = User.query.get(id)

    return user


def user_search_email(email):
    '''Retorna user por su email, en caso de existir. De lo contrario, retorna None'''

    return User.query.filter_by(email=email).first()


def users_search_state(state):
    '''Retorna un listado de users por su estado, en caso de existir. De lo contrario, retorna una lista vacia'''

    return User.query.filter_by(activo=state).all()


def user_assign_roles(id, role_names):
    '''Asigna o desasigna roles a un usuario'''
    user = User.query.get(id)

    if user is None:
        raise ValueError('Usuario no encontrado')

    # Obtener roles existentes
    roles = Role.query.filter(Role.name.in_(role_names)).all()

    # Asignar o desasignar roles al usuario
    user.rol = roles

    db.session.commit()


def user_toggle_status(id):
    '''Activa o bloquea un usuario, evitando bloquear Super Administradores'''
    user = User.query.get(id)

    if user is None:
        raise ValueError('Usuario no encontrado')

    if user.rol and any(role.name == 'superadmin' for role in user.rol):
        # Si el usuario tiene el rol de Super Administrador, no permitir bloquearlo
        raise ValueError('No se puede bloquear a un Super Administrador')
    else:
        # Alternar el estado activo del usuario
        user.activo = not user.activo
        db.session.commit()


def assign_institution_role(user, institution, role):
    """Asigna una institución y un rol a un usuario"""
    try:
        user_institution_role = user_rol_inst.insert().values(
            user_id=user.id, institution_id=institution.id, role_id=role.id)

        # Agrega la instancia a la sesión y realiza el commit
        db.session.execute(user_institution_role)
        db.session.commit()

        return True
    except:
        db.session.rollback()
        return False


def user_register_confirmation(id):
    """Activa a un usuario luego de haberse registrado en el sistema"""
    user = User.query.get(id)

    if user is None:
        raise ValueError('Usuario no encontrado')

    user.activo = True
    db.session.commit()


def get_usuario_id(id):
    """Busca un usuario por su ID"""
    user = db.session.query(User).get(id)

    return user
