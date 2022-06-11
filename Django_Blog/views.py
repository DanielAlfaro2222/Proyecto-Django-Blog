from django.shortcuts import render
from Blog.models import Article
from Blog.utils import busqueda_articulos
from django.contrib import messages
from django.core.paginator import Paginator
from django.views.generic import TemplateView
from django.contrib.auth.forms import PasswordResetForm
from Users.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from .utils import send_email
from django.shortcuts import redirect
import threading


def index_view(request):
    """
    Vista encargada de mostrar la pagina principal de la aplicacion.
    """

    articulos = Article.objects.filter(state='Activo').order_by('-id_article')

    if request.GET.get('q'):
        parametro_busqueda = request.GET.get('q')
        articulos = busqueda_articulos(request, parametro_busqueda)

        if articulos.count() == 0:
            messages.error(
                request, f'No se encontraron coincidencias con {parametro_busqueda}')
            articulos = Article.objects.filter(
                state='Activo').order_by('-id_article')
        else:
            messages.success(
                request, f'Se encontraron {articulos.count()} articulos para {request.GET.get("q")}')

    # Paginacion por cada 5 articulos
    paginacion = Paginator(articulos, 7)
    num_pagina = request.GET.get('page')
    articulos = paginacion.get_page(num_pagina)

    return render(request, 'index.html', context={
        'articulos': articulos,
        'paginacion': paginacion,
    })


class Error400TemplateView(TemplateView):
    """
    Vista encargada de renderizar el template personalizado del error 400.
    """

    template_name = 'codigos_error/400.html'


class Error403TemplateView(TemplateView):
    """
    Vista encargada de renderizar el template personalizado del error 403.
    """

    template_name = 'codigos_error/403.html'


class Error404TemplateView(TemplateView):
    """
    Vista encargada de renderizar el template personalizado del error 404.
    """

    template_name = 'codigos_error/404.html'


class Error500TemplateView(TemplateView):
    """
    Vista encargada de renderizar el template personalizado del error 500.
    """

    template_name = 'codigos_error/500.html'

    @classmethod
    def as_error_view(cls):

        v = cls.as_view()

        def view(request):
            r = v(request)
            r.render()
            return r
        return view


def reset_password(request):
    """
    Vista encargada de enviar el correo al usuario para restablecer la contraseña.
    """

    form = PasswordResetForm(request.POST or None)

    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()

        if user:
            try:
                protocolo = 'https' if request.is_secure() else 'http'
                template = 'mails/email_recuperar_contraseña.html'
                context = {
                    'usuario': user.get_short_name(),
                    'dominio': get_current_site(request).domain,
                    'uuid':  str(urlsafe_base64_encode(force_bytes(user.id_user))),
                    'token': default_token_generator.make_token(user),
                    'protocolo': protocolo,
                }

                thread = threading.Thread(target=send_email, args=[
                                          template, context, 'Recuperar contraseña', email])

                thread.start()

                messages.success(
                    request, 'Le enviamos las instrucciones por correo electrónico para configurar su nueva contraseña')

                return redirect('reset_password')
            except:
                messages.error(
                    request, 'Error no se pudo enviar el correo electronico, por favor intente mas tarde')

        else:
            messages.error(
                request, 'Error el usuario no esta registrado en el sistema.')

    return render(request, 'recuperar-contraseña/recuperar-contraseña.html', context={
        'form': form
    })
