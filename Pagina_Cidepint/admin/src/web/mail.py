from flask import render_template_string, url_for
from flask_mail import Mail, Message

mail = Mail()


def init_app(app):
    """
        Inicializa la conf. del mail
    """
    mail.init_app(app)


def send_mail(subject, recipients="proyectomatomaniaco@gmail.com", sender="proyectomatomaniaco@gmail.com"):
    """
        Envia un correo electronico
        -Subject: asunto
        -Recipients: destinatario
        -Sender: remitente
    """
    msg = Message(subject=subject, sender=sender, recipients=[recipients])
    link = "https://admin-grupo22.proyecto2023.linti.unlp.edu.ar/register/confirmation/" + recipients
    msg.html = '<p>Hola! Esto es <strong>PinturApp</strong>, para finalizar tu registro pulsa el <a href="' + \
        link + '"' + '>link</a>.</p>'
    # Actualizar el link cuando lo pushee a main: https://admin-grupo22.proyecto2023.linti.unlp.edu.ar/register/confirmation/ http://localhost:5000/register/confirmation/
    mail.send(msg)


def send_mail_vue(subject, recipients="proyectomatomaniaco@gmail.com", sender="proyectomatomaniaco@gmail.com"):
    """
        Envia un correo electronico
        -Subject: asunto
        -Recipients: destinatario
        -Sender: remitente
    """
    msg = Message(subject=subject, sender=sender, recipients=[recipients])
    link = "http://localhost:5000/register/confirmationVue/" + recipients
    msg.html = '<p>Hola! Esto es <strong>PinturApp</strong>, para finalizar tu registro pulsa el <a href="' + \
        link + '"' + '>link</a>.</p>'
    # Actualizar el link cuando lo pushee a main: https://admin-grupo22.proyecto2023.linti.unlp.edu.ar/register/confirmationVue/ http://localhost:5000/register/confirmationVue/
    mail.send(msg)
