from django.core.exceptions import ValidationError


def send_email():
    pass


def validate_image(fieldfile_obj):
    filesize = fieldfile_obj.file.size
    megabyte_limit = 1
    if filesize > megabyte_limit*1024*1024:
        raise ValidationError(
            f"El tamaño maximo del archivo debe ser {megabyte_limit}MB")
