from django import forms
from django.contrib.auth import authenticate
from .models import User

from django.core.mail import send_mail
from django.conf import settings

class LoginForm(forms.Form):
    correo = forms.EmailField(
        required = True,
        widget = forms.EmailInput(attrs = {
            'autofocus': 'true',
            'tab-index': 1,
            'placeholder': 'Correo',
            'max_length': 25,
            'class': 'container-form-login__input'
        })
    )
    contrasena = forms.CharField(
        required = True,
        widget = forms.PasswordInput(attrs = {
            'tab-index': 2,
            'placeholder': 'Contraseña',
            'class': 'container-form-login__input'
        })
    )

    def autenticar_usuario(self):
        return authenticate(
                username = self.cleaned_data.get('correo'),
                password = self.cleaned_data.get('contrasena')
            )

class RegisterForm(forms.Form):
    GENDER = [
        ('', '--'),
        ('MALE', 'Hombre'),
        ('FEMALE', 'Mujer'),
        ('OTHER', 'Prefiero no decirlo')
    ]

    nombre = forms.CharField(
        required = True,
        max_length = 45,
        min_length = 4,
        widget = forms.TextInput(attrs = {
            'autofocus': 'true',
            'tab-index': 1,
            'class': 'container-label-register__input'
        })
    )

    apellido = forms.CharField(
        required = True,
        max_length = 45,
        min_length = 4,
        widget = forms.TextInput(attrs = {
            'tab-index': 2,
            'class': 'container-label-register__input'
        })
    )

    correo = forms.EmailField(
        required = True,
        max_length = 55,
        widget = forms.EmailInput(attrs = {
            'tab-index': 5,
            'class': 'container-label-register__input'
        })
    )

    genero = forms.TypedChoiceField(
        required = True,
        widget = forms.Select(attrs = {
            'tab-index': 3,
            'class': 'container-label-register__select'
        }),
        choices = GENDER
    )
    imagen = forms.ImageField(
        required = False,
        widget = forms.FileInput(attrs = {
            'tab-index': 4,
            'class': 'container-label-register__image'
        })
    )

    contrasena = forms.CharField(
        required = True,
        widget = forms.PasswordInput(attrs = {
            'tab-index': 6,
            'class': 'container-label-register__input'
        })
    )

    def save(self):
        email = self.cleaned_data.get('correo')
        password = self.cleaned_data.get('contrasena')

        usuario = User.objects.create_user(email, password)

        usuario.first_name = self.cleaned_data.get('nombre')
        usuario.last_name = self.cleaned_data.get('apellido')
        usuario.gender = self.cleaned_data.get('genero')
        usuario.save()

        return usuario



class ContactForm(forms.Form):
    nombre = forms.CharField(
        required = True,
        widget = forms.TextInput(attrs = {
            'autofocus': 'true',
            'tab-index': 1,
            'placeholder': 'Nombre',
            'max_length': 25,
        })
    )

    asunto = forms.CharField(
        required = True,
        widget = forms.TextInput(attrs = {
            'tab-index': 2,
            'placeholder': 'Asunto',
            'max_length': 45,
        })
    )
    correo = forms.EmailField(
        required = True,
        widget = forms.EmailInput(attrs = {
            'tab-index': 3,
            'placeholder': 'Correo',
            'max_length': 25,
        })
    )

    mensaje = forms.CharField(
        required = True,
        widget = forms.Textarea(attrs = {
            'tab-index': 4,
            'placeholder': 'Mensaje'
        })
    )

    def enviar_correo(self):
        mensaje = f"""
            Nombre: {self.cleaned_data.get('nombre')} Asunto: {self.cleaned_data.get('asunto')} Correo: {self.cleaned_data.get('correo')} Mensaje: {self.cleaned_data.get('mensaje')}
        """

        try:
            send_mail(
                'Nuevo mensaje de contacto', 
                mensaje, 
                settings.EMAIL_HOST_USER, 
                ['kdalfaro45@misena.edu.co']
            )
            return True
        except:
            return False