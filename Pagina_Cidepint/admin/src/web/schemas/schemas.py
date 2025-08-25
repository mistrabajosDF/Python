from marshmallow import Schema, fields, EXCLUDE
from src.core.database import ma

# clases para el parseo


class CreateRequestSchema(Schema):
    title = fields.Str()
    description = fields.Str()


create_request_schema = CreateRequestSchema(only=["title", "description"])


class CreateNoteSchema(Schema):
    id = fields.Int(dump_only=True)
    description = fields.Str()


create_note_schema = CreateNoteSchema()


class NoteSchema(Schema):
    id = fields.Int(dump_only=True)
    description = fields.Str()
    inserted_at = fields.DateTime()


note_schema = NoteSchema()
notes_schema = NoteSchema(many=True)


class InstitutionSchema(Schema):
    id = fields.Int(dump_only=True)
    nombre = fields.Str()
    informacion = fields.Str()
    direccion = fields.Str()
    localizacion = fields.Str()
    paginaweb = fields.Str()
    # palabrasclave =
    diasyhorarios = fields.Str()
    contacto = fields.Str()
    habilitada = fields.Bool()
    updated_at = fields.DateTime()
    inserted_at = fields.DateTime()


institution_schema = InstitutionSchema()
institutions_schema = InstitutionSchema(many=True)


class CreateInstitutionSchema(Schema):
    nombre = fields.Str()
    informacion = fields.Str()
    direccion = fields.Str()
    localizacion = fields.Str()
    paginaweb = fields.Str()
    # palabrasclave =
    diasyhorarios = fields.Str()
    contacto = fields.Str()
    habilitada = fields.Bool()


create_institution_schema = CreateInstitutionSchema(
    only=["nombre", "habilitada", "localizacion"], unknown=EXCLUDE)
# Exclude hace que si llega un campo que no existe en institucion lo omita


class UserSchema(Schema):
    nombre = fields.Str()
    apellido = fields.Str()
    email = fields.Email()
    username = fields.Str()


user_schema = UserSchema()  # una sola


class InstitutionMiniSchema(Schema):
    id = fields.Int(dump_only=True)
    nombre = fields.Str()


institution_mini_schema = InstitutionMiniSchema()
institutions_mini_schema = InstitutionMiniSchema(many=True)


class PalabraServSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()


palabra_serv_schema = PalabraServSchema()
palabras_serv_schema = PalabraServSchema(many=True)


class ServiceSchema(Schema):
    id = fields.Int(dump_only=True)
    nombre = fields.Str()
    descripcion = fields.Str()
    palabras_clave = ma.Nested(PalabraServSchema, many=True)
    centrosACargo = ma.Nested(InstitutionSchema, many=True)
    tipo = fields.Str()
    habilitado = fields.Bool()
    updated_at = fields.DateTime()
    inserted_at = fields.DateTime()


service_schema = ServiceSchema()
services_schema = ServiceSchema(many=True)


class CreateServiceSchema(Schema):
    nombre = fields.Str()
    descripcion = fields.Str()
    tipo = fields.Str()
    habilitado = fields.Bool()
    updated_at = fields.DateTime()
    inserted_at = fields.DateTime()


create_service_schema = CreateServiceSchema(unknown=EXCLUDE)


class RequestSchema(Schema):
    id = fields.Int()
    request_date = fields.DateTime()
    status = fields.Str()
    change_status_date = fields.DateTime()
    observation = fields.Str()


request_schema = RequestSchema()
requests_schema = RequestSchema(many=True)


class RequestServSchema(Schema):
    id = fields.Int()
    request_date = fields.DateTime()
    status = fields.Str()
    change_status_date = fields.DateTime()
    observation = fields.Str()
    nombre = fields.Str()
    tipo = fields.Str()
    obs_est_act = fields.Str()


request_serv_schema = RequestServSchema()
requests_serv_schema = RequestServSchema(many=True)
