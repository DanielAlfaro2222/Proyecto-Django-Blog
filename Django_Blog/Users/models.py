from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core import validators
from django.db.models.signals import pre_save
from django.utils.text import slugify
import uuid

class City(models.Model):
    id_city = models.AutoField("Id Ciudad", primary_key = True)
    description = models.CharField("Descripcion", null = True, blank = True, max_length=45)
    zip_code = models.CharField("Codigo postal", max_length = 6)
    create = models.DateTimeField('Fecha de creacion', auto_now_add = True)
    modified = models.DateTimeField('Fecha de modificacion', auto_now = True)
    state = models.BooleanField('Estado', default = True)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = "Ciudad"
        verbose_name_plural = "Ciudades"
        db_table = "city"
        ordering = ['id_city']

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
    biography = models.CharField('Biografia', null = True, blank = True, max_length = 120)
    gender = models.CharField(
        'Genero', 
        choices = GENDER,
        null = True,
        blank = True,
        default = 'Prefiero no decirlo',
        max_length = 19
    )
    linkedin = models.URLField('Linkedin', null = True, blank = True)
    twitter = models.URLField('Twitter', null = True, blank = True)
    is_staff = models.BooleanField('Administrador', default = False)
    is_active = models.BooleanField('Activo', default = True)
    slug = models.SlugField('Url', null = True, blank = True)
    city = models.ForeignKey(City, verbose_name="Ciudad", on_delete=models.CASCADE, null = True, blank = True)

    # Especificar que campo sera el username
    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        return f'{self.first_name.split()[0]} {self.last_name.split()[0]}'

    def get_quantity_articles(self):
        return self.article_set.filter(state = True).count()

    def has_biography(self):
        return True if self.biography else False

    def has_linkedin(self):
        return True if self.linkedin else False

    def has_image(self):
        return True if self.image else False

    def has_twitter(self):
        return True if self.twitter else False

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

def set_slug_user(sender, instance, *args, **kwargs):
    if instance.first_name and not instance.slug:
        slug = slugify(
            f'{instance.first_name.split()[0]} {instance.last_name.split()[0]}'
        )

        while User.objects.filter(slug = slug).exists():
            slug = slugify(
                f'{instance.first_name[0]}-{instance.last_name.split()[0]}-{str(uuid.uuid4())[:5]}'
            )

        instance.slug = slug

pre_save.connect(set_slug_user, sender = User)