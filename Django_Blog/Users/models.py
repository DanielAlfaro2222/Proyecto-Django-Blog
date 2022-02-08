from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core import validators

class UserManager(BaseUserManager):
    use_in_migrations = True

    def save_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('El correo debe ser ingresado')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        return self.save_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('is_superuser should be True')
        
        extra_fields['is_staff'] = True

        return self.save_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    GENDER = [
        ('MALE', 'Hombre'),
        ('FEMALE', 'Mujer'),
        ('OTHER', 'Prefiero no decirlo')
    ]

    id_user = models.AutoField('Id usuario', primary_key = True)
    first_name = models.CharField('Nombre', default = '', max_length = 45)
    last_name = models.CharField('Apellido', default = '', max_length = 45)
    email = models.CharField(
        'Correo', 
        unique = True, 
        max_length = 55, 
        validators = [validators.EmailValidator()]
    )
    image = models.ImageField('Imagen de perfil', upload_to = 'users/profile_image', null = True, blank = True)
    biography = models.TextField('Biografia', null = True, blank = True)
    gender = models.CharField(
        'Genero', 
        choices = GENDER,
        null = True,
        blank = True,
        default = 'Prefiero no decirlo',
        max_length = 19
    )
    linkedin = models.URLField('Linkedin', null = True, blank = True)


    is_staff = models.BooleanField('Administrador', default = False)
    is_active = models.BooleanField('Activo', default = True)

    # Especificar que campo sera el username
    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

