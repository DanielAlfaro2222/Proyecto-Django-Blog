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
from django.core.paginator import Paginator
from django.shortcuts import HttpResponseRedirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from .forms import CreateArticleModelForm
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from .forms import UserModelForm


def login_view(request):
    """
    Vista encargada del login.
    """

    if request.user.is_authenticated:
        return redirect('index')

    if request.GET.get('next'):
        messages.error(request, 'Error debe iniciar sesion primero')

    formulario = LoginForm(request.POST or None)

    if request.method == 'POST' and formulario.is_valid():
        usuario = formulario.autenticar_usuario()

        if User.objects.filter(email=request.POST.get('correo')).first() is None:
            messages.error(
                request, 'El usuario no esta registrado en el sistema')
        elif usuario:
            login(request, usuario)

            if request.GET.get('next'):
                return HttpResponseRedirect(request.GET.get('next'))
            elif usuario.is_staff:
                return redirect(reverse_lazy('Admin:admin'))
            else:
                return redirect('index')
        else:
            messages.error(request, 'Correo o contraseña incorrectos')

    return render(request, 'users/login.html', context={
        'formulario': formulario,
    })


@login_required
def logout_view(request):
    """
    Vista encargada del cierre de sesion.
    """

    logout(request)
    messages.success(request, 'Sesion cerrada exitosamente')
    return redirect('Users:login')


def register_view(request):
    """
    Vista encargada del registro de los usuarios.
    """

    if request.user.is_authenticated:
        return redirect('index')

    formulario = RegisterForm(request.POST or None, request.FILES or None)

    if request.method == 'POST' and formulario.is_valid():
        usuario = formulario.save()
        imagen = request.FILES.get('imagen')
        usuario.image = imagen
        usuario.save()

        if usuario:
            login(request, usuario)
            return redirect('index')

    return render(request, 'users/register.html', context={
        'formulario': formulario,
    })


def contact_view(request):
    """
    Vista encargada del formulario de contacto.
    """

    formulario = ContactForm(request.POST or None)

    # if request.method == 'POST' and formulario.is_valid():
    #     if formulario.enviar_correo():
    #         messages.success(request, 'Correo enviado con exito.')
    #     else:
    #         messages.error(request, 'El correo no se pudo enviar')

    return render(request, 'users/contact.html', context={
        'formulario': formulario,
    })


class AuthorDetailView(DetailView):
    """
    Vista encargada de mostrar el perfil de un usuario.
    """

    template_name = 'users/biografia-autor.html'
    model = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['autor'] = context['object']
        context['registros'] = Article.objects.filter(
            author=context['autor'], state='Activo').order_by('-create')
        context['paginacion'] = Paginator(context['registros'], 5)
        context['num_pagina'] = self.request.GET.get('page')
        context['articulos'] = context['paginacion'].get_page(
            context['num_pagina'])

        return context


class AccountTemplateView(LoginRequiredMixin, TemplateView):
    """
    Vista encargada del template de mi cuenta de los usuarios.
    """

    template_name = 'users/mi-cuenta.html'


class UpdateDataUserView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Vista encargada de actualizar los datos personales de los usuarios.
    """

    template_name = 'users/actualizar-datos.html'
    form_class = UserModelForm
    success_url = reverse_lazy('Users:account')
    success_message = 'Informacion actualizada exitosamente'
    slug_field = 'slug'

    def get_queryset(self):
        return User.objects.filter(slug=self.kwargs.get('slug'))

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial={
            'first_name': self.request.user.first_name,
            'last_name': self.request.user.last_name,
            'email': self.request.user.email,
            'gender': self.request.user.gender,
            'image': self.request.user.image,
            'city': self.request.user.city,
            'linkedin': self.request.user.linkedin,
            'twitter': self.request.user.twitter,
            'biography': self.request.user.biography,
        })

        return render(request, self.template_name, {
            'formulario': form,
        })

    def post(self, request, *args, **kwargs):
        print(self.request.POST)
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)


class PublicationsListView(ListView):
    """
    Vista encargada de listar las publicaciones de un autor.
    """

    template_name = 'users/mis-publicaciones.html'
    model = Article
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['registros'] = Article.objects.filter(
            author=self.request.user).order_by('-create')
        context['paginacion'] = Paginator(context['registros'], 10)
        context['num_pagina'] = self.request.GET.get('page')
        context['articulos'] = context['paginacion'].get_page(
            context['num_pagina'])

        return context


class CreateArticleView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'users/nuevo-articulo.html'
    form_class = CreateArticleModelForm
    success_url = reverse_lazy('Users:articles-user')
    success_message = 'Articulo publicado exitosamente'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial={'author': self.request.user})
        return render(request, self.template_name, {'form': form})


class UpdateArticleView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'users/editar-articulo.html'
    form_class = CreateArticleModelForm
    success_url = reverse_lazy('Users:articles-user')
    success_message = 'Articulo editado exitosamente'
    slug_field = 'slug'

    def get_queryset(self):
        return Article.objects.filter(slug=self.kwargs.get('slug'))

    def get(self, request, *args, **kwargs):
        articulo = self.get_queryset().first()
        form = self.form_class(initial={
            'state': articulo.state,
            'author': self.request.user,
            'image': articulo.image,
            'category': articulo.category,
            'resume': articulo.resume,
            'content': articulo.content,
            'name': articulo.name
        })
        return render(request, self.template_name, {
            'form': form,
            'articulo': articulo
        })
