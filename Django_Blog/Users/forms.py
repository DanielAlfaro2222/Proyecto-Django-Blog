from django import forms
from django.contrib.auth import authenticate

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
        })
    )
    contrasena = forms.CharField(
        required = True,
        widget = forms.PasswordInput(attrs = {
            'tab-index': 2,
            'placeholder': 'Contraseña',
        })
    )

    def autenticar_usuario(self):
        return authenticate(
                username = self.cleaned_data.get('correo'),
                password = self.cleaned_data.get('contrasena')
            )

class RegisterForm(forms.Form):
    def save(self):
        pass

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