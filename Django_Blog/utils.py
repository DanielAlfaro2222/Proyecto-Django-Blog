from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.conf import settings


def send_email(url_template, context, subject, addressee=settings.EMAIL_HOST_USER, copy=None):
    """
    Funcion utilitaria para encapsular la logica de envio de correos para no repetir codigo.
    """

    template = get_template(url_template)

    content = template.render(context)

    email = EmailMultiAlternatives(
        subject=subject,
        body='',
        from_email=settings.EMAIL_HOST_USER,
        to=[addressee],
        cc=[copy if copy != None else '']
    )

    email.attach_alternative(content, 'text/html')

    email.send(fail_silently=False)


def validate_image(fieldfile_obj):
    filesize = fieldfile_obj.file.size
    megabyte_limit = 1
    if filesize > megabyte_limit*1024*1024:
        raise ValidationError(
            f"El tamaño maximo del archivo debe ser {megabyte_limit}MB")


ESTADO = (
    ('Activo', 'Activo'),
    ('Desactivo', 'Desactivo')
)
