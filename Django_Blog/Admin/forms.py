from django import forms
from Blog.models import Article
from Blog.models import Category
from Users.models import City
from Users.models import User


class ArticleModelForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['name', 'image', 'resume',
                  'content', 'author', 'category', 'state']
        widgets = {
            'name': forms.TextInput(attrs={
                'autofocus': 'true',
                'class': '',
            }),
        }


class CategoryModelForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'state']
        widgets = {}


class CityModelForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ['description', 'zip_code', 'state']
        widgets = {}


class UserModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'biography',
                  'image', 'gender', 'linkedin', 'twitter', 'city', 'groups', 'state', 'password']
        widgets = {
            'biography': forms.Textarea(attrs={'class': ''}),
            'password': forms.PasswordInput(attrs={'class': ''})
        }

    def clean_password(self):
        contrasena = self.cleaned_data.get('password')

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

        return contrasena

    def clean_image(self):
        imagen = self.cleaned_data.get('image')
        limite = 1024*1024

        if imagen is not None and len(imagen) > limite:
            raise forms.ValidationError(
                'El tamaño maximo del archivo debe ser de 1mb')

        return imagen
