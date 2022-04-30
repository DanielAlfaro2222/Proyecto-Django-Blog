from django.shortcuts import render
from .forms import LoginForm
from .forms import ContactForm
from django.contrib import messages
from django.contrib.auth import login 
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
from .forms import RegisterForm
from .models import User
from Blog.models import Article
# from django.template.loader import get_template
# from django.conf import settings
# from django.core.mail import EmailMultiAlternatives
# from django.shortcuts import redirect

def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    formulario = LoginForm(request.POST or None)

    if request.method == 'POST' and formulario.is_valid():
        usuario = formulario.autenticar_usuario()

        if usuario:
            login(request, usuario)
            return redirect('index')
        else:
            messages.error(request, 'Correo o contraseña incorrectos')

    return render(request, 'users/login.html', context = {
        'formulario': formulario,
    })


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Sesion cerrada exitosamente')
    return redirect('Users:login')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    formulario = RegisterForm(request.POST or None)

    if request.method == 'POST' and formulario.is_valid():
        usuario = formulario.save()
        imagen = request.FILES.get('imagen')
        usuario.image = imagen
        usuario.save()

        if usuario:
            login(request, usuario)
            return redirect('index')

    return render(request, 'users/register.html', context = {
        'formulario': formulario,
    })

# def create_email(subject, correo_destino, template, context):
#     template = get_template(template)
#     content = template.render(context)

#     mail = EmailMultiAlternatives(
#         subject = subject,
#         body = '',
#         from_email = settings.EMAIL_HOST_USER,
#         to = [correo_destino],
#         cc = [] # enviar una copia del email a otro correo
#     )

#     mail.attach_alternative(content, 'text/html')

#     return mail

# def send_mail_prueba():
#     mail = create_email(
#         'Correo de prueba con estilos',
#         'kdalfaro45@misena.edu.co',
#         'mails/correo.html',
#         { 
#             'mensaje': 'Este es un correo de prueba.'
#         }
#     )

#     mail.send(fail_silently = False)

def contact_view(request):
    # formulario = ContactForm(request.POST or None)

    # if request.method == 'POST' and formulario.is_valid():
    #     if formulario.enviar_correo():
    #         messages.success(request, 'Correo enviado con exito.')
    #     else:
    #         messages.error(request, 'El correo no se pudo enviar')


    return render(request, 'users/contact.html', context = {
    })

# def send_mail(request):
#     send_mail_prueba()
#     return redirect('Users:contact')

class AuthorDetailView(DetailView):
    template_name = 'users/biografia-autor.html'
    model = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['autor'] = context['object']
        context['articulos'] = Article.objects.filter(author = context['autor'], state = True).order_by('-create')

        return context