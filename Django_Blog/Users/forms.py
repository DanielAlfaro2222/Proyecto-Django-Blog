from django import forms
from django.contrib.auth import authenticate
from .models import User
from .models import City
from Blog.models import Article

from django.core.mail import send_mail
from django.conf import settings


class LoginForm(forms.Form):
    correo = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'autofocus': 'true',
            'tab-index': 1,
            'placeholder': 'Correo',
            'max_length': 25,
            'class': 'container-form-login__input'
        })
    )
    contrasena = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'tab-index': 2,
            'placeholder': 'Contraseña',
            'class': 'container-form-login__input'
        })
    )

    def autenticar_usuario(self):
        return authenticate(
            username=self.cleaned_data.get('correo'),
            password=self.cleaned_data.get('contrasena')
        )


class RegisterForm(forms.Form):
    GENDER = [
        ('', '--'),
        ('MALE', 'Hombre'),
        ('FEMALE', 'Mujer'),
        ('OTHER', 'Prefiero no decirlo')
    ]

    nombre = forms.CharField(
        required=True,
        max_length=45,
        min_length=4,
        widget=forms.TextInput(attrs={
            'autofocus': 'true',
            'class': 'container-label-register__input'
        })
    )

    apellido = forms.CharField(
        required=True,
        max_length=45,
        min_length=4,
        widget=forms.TextInput(attrs={
            'class': 'container-label-register__input'
        })
    )

    correo = forms.EmailField(
        required=True,
        max_length=55,
        widget=forms.EmailInput(attrs={
            'class': 'container-label-register__input',
            'placeholder': 'ejemplo@gmail.com'
        })
    )

    genero = forms.TypedChoiceField(
        required=True,
        widget=forms.Select(attrs={
            'class': 'container-label-register__select'
        }),
        choices=GENDER
    )
    imagen = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'container-label-register__image'
        })
    )

    contrasena = forms.CharField(
        required=True,
        min_length=8,
        widget=forms.PasswordInput(attrs={
            'class': 'container-label-register__input'
        })
    )

    ciudad = forms.ModelChoiceField(
        required=True,
        widget=forms.Select(attrs={
            'class': 'container-label-register__select',
        }),
        queryset=City.objects.filter(state=True),
        empty_label="--",
    )

    linkedin = forms.URLField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'container-label-register__input',
            'placeholder': 'https://www.linkedin.com'
        })
    )

    twitter = forms.URLField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'container-label-register__input',
            'placeholder': 'https://twitter.com'
        })
    )

    biografia = forms.CharField(
        required=True,
        max_length=120,
        widget=forms.Textarea(attrs={
            'class': 'container-label-register__textarea'
        })
    )

    def clean_correo(self):
        correo = self.cleaned_data.get('correo')

        if User.objects.filter(email=correo).exists():
            raise forms.ValidationError(
                'El correo ya esta registrado en el sistema.')

        return correo

    def clean_contrasena(self):
        contrasena = self.cleaned_data.get('contrasena')

        mayusculas = 0
        numeros = 0
        simbolos = 0

        for caracter in contrasena:
            if caracter in "!#$%&'()*+,-./:;=?{|}~[\]^_`@·½¬><":
                simbolos += 1
            elif caracter in '0123456789':
                numeros += 1
            elif caracter == caracter.upper():
                mayusculas += 1

        if mayusculas < 1 or numeros < 1 or simbolos < 1:
            raise forms.ValidationError(
                'La contraseña debe tener minimo 8 caracteres y debe contener 1 mayuscula, 1 simbolo y 1 numero.')

    def clean_ciudad(self):
        ciudad = self.cleaned_data.get('ciudad')

        if ciudad == None:
            raise forms.ValidationError(CAMPO_OBLIGATORIO)

        return ciudad

    def save(self):
        email = self.cleaned_data.get('correo')
        password = self.cleaned_data.get('contrasena')

        usuario = User.objects.create_user(email, password)

        usuario.first_name = self.cleaned_data.get('nombre').strip()
        usuario.last_name = self.cleaned_data.get('apellido').strip()
        usuario.gender = self.cleaned_data.get('genero')
        usuario.city = City.objects.get(
            description=self.cleaned_data.get('ciudad'))
        usuario.save()

        return usuario


class ContactForm(forms.Form):
    nombre = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'autofocus': 'true',
            'tab-index': 1,
            'max_length': 30,
            'class': 'container-form-contact__input'
        })
    )

    asunto = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'tab-index': 2,
            'max_length': 45,
            'class': 'container-form-contact__input'
        })
    )
    correo = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'tab-index': 3,
            'placeholder': 'ejemplo@gmail.com',
            'max_length': 25,
            'class': 'container-form-contact__input'
        })
    )

    mensaje = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            'tab-index': 4,
            'class': 'container-form-contact__textarea'
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


class CreateArticleModelForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['name', 'author', 'image',
                  'resume', 'state', 'content', 'category']
        widgets = {
            'name': forms.TextInput(attrs={'class': ''}),
            'image': forms.FileInput(attrs={'class': ''}),
            'resume': forms.TextInput(attrs={'class': ''}),
            'content': forms.Textarea(attrs={'class': ''}),
            'category': forms.Select(attrs={'class': ''}),
            'author': forms.Select(attrs={'hidden': 'true'})
        }
