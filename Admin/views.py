from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.views.generic import UpdateView
from .utils import AdminGroupTest
from django.contrib.auth.mixins import LoginRequiredMixin
from Users.models import User
from Blog.models import Article
from Users.models import City
from Blog.models import Category
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import ArticleModelForm
from django.views.generic.detail import SingleObjectMixin
from django.contrib.messages.views import SuccessMessageMixin
from .forms import CategoryModelForm
from .forms import CityModelForm
from .forms import UserModelForm
from django.http import HttpResponseRedirect
from django.contrib import messages
from Blog.models import Comment
from django.db.models import Count
from django.shortcuts import get_object_or_404
from .forms import CommentModelForm
from django.db.models import Q
from django.core.paginator import Paginator


class AdminTemplateView(LoginRequiredMixin, AdminGroupTest, TemplateView):
    """
    Vista encargada de mostrar la pagina principal del panel de administacion.
    """

    template_name = 'admin/panel-admin.html'


class ArticlesListView(LoginRequiredMixin, AdminGroupTest, ListView):
    """
    Vista encargada de mostrar el listado de articulos en el panel de administracion.
    """

    template_name = 'admin/articulos/listado-articulos.html'
    model = Article
    queryset = Article.objects.all().order_by('-modified')
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['paginacion'] = context['paginator']
        context['articulos'] = context['paginacion'].get_page(
            self.request.GET.get('page'))

        if self.request.GET.get('q'):
            parametro_busqueda = self.request.GET.get('q')
            context['query'] = Article.objects.filter(
                Q(name__icontains=parametro_busqueda) | Q(content__icontains=parametro_busqueda) | Q(resume__icontains=parametro_busqueda)).order_by('-modified')
            context['resultado'] = context['query'].count()

            if context['resultado'] != 0:
                context['paginacion'] = Paginator(context['query'], 8)
                context['articulos'] = context['paginacion'].get_page(
                    self.request.GET.get('page'))

        return context


class ArticleCreateView(SuccessMessageMixin, LoginRequiredMixin, AdminGroupTest, CreateView):
    """
    Vista encargada de crear un articulo en el panel de administacion.
    """

    template_name = 'admin/articulos/nuevo-articulo.html'
    model = Article
    form_class = ArticleModelForm
    success_url = reverse_lazy('Admin:articles')
    success_message = 'Articulo creado exitosamente'


class ArticleUpdateView(SuccessMessageMixin, LoginRequiredMixin, AdminGroupTest, UpdateView, SingleObjectMixin):
    """
    Vista encargada de actualizar un articulo en el panel de administacion.
    """

    template_name = 'admin/articulos/editar-articulo.html'
    model = Article
    form_class = ArticleModelForm
    success_url = reverse_lazy('Admin:articles')
    success_message = 'Articulo editado exitosamente'
    slug_field = 'slug'

    def get_queryset(self):
        return Article.objects.filter(slug=self.kwargs.get('slug'))

    def get(self, request, *args, **kwargs):
        articulo = self.get_queryset().first()
        form = self.form_class(instance=articulo)

        return render(request, self.template_name, {
            'form': form,
            'articulo': articulo,
        })


class UsersListView(LoginRequiredMixin, AdminGroupTest, ListView):
    """
    Vista encargada de mostrar el listado de usuarios en el panel de administracion.
    """

    template_name = 'admin/usuarios/listado-usuarios.html'
    model = User
    queryset = User.objects.all().order_by('-id_user')
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['paginacion'] = context['paginator']
        context['usuarios'] = context['paginacion'].get_page(
            self.request.GET.get('page'))

        if self.request.GET.get('q'):
            parametro_busqueda = self.request.GET.get('q')
            context['query'] = User.objects.filter(
                Q(first_name__icontains=parametro_busqueda) | Q(last_name__icontains=parametro_busqueda) | Q(email__icontains=parametro_busqueda))
            context['resultado'] = context['query'].count()

            if context['resultado'] != 0:
                context['paginacion'] = Paginator(context['query'], 8)
                context['usuarios'] = context['paginacion'].get_page(
                    self.request.GET.get('page'))

        return context


class UserCreateView(SuccessMessageMixin, LoginRequiredMixin, AdminGroupTest, CreateView):
    """
    Vista encargada de crear un usuario en el panel de administacion.
    """

    template_name = 'admin/usuarios/nuevo-usuario.html'
    model = User
    form_class = UserModelForm
    success_url = reverse_lazy('Admin:users')
    success_message = 'Usuario creado exitosamente'

    def form_valid(self, form):
        self.object = User.objects.create_user(
            email=form.cleaned_data.get('email'),
            password=form.cleaned_data.get('password'),
        )
        self.object.first_name = form.cleaned_data.get('first_name')
        self.object.last_name = form.cleaned_data.get('last_name')
        self.object.biography = form.cleaned_data.get('biography')
        self.object.image = form.cleaned_data.get('image')
        self.object.gender = form.cleaned_data.get('gender')
        self.object.linkedin = form.cleaned_data.get('linkedin')
        self.object.twitter = form.cleaned_data.get('twitter')
        self.object.city = City.objects.get(
            description=form.cleaned_data.get('city'))
        self.object.state = form.cleaned_data.get('state')
        self.object.groups.set(form.cleaned_data.get('groups'))

        if form.cleaned_data.get('groups').filter(name='Administrador').exists():
            self.object.is_staff = True
            self.object.is_superuser = True

        self.object.save()

        messages.success(
            self.request, self.get_success_message(form.cleaned_data))

        return HttpResponseRedirect(self.get_success_url())


class UserUpdateView(SuccessMessageMixin, LoginRequiredMixin, AdminGroupTest, UpdateView):
    """
    Vista encargada de actualizar un usuario en el panel de administracion.
    """

    template_name = 'admin/usuarios/editar-usuario.html'
    model = User
    form_class = UserModelForm
    success_url = reverse_lazy('Admin:users')
    success_message = 'Usuario editado exitosamente'
    context_object_name = 'usuario'

    def get_queryset(self):
        return User.objects.filter(slug=self.kwargs.get('slug'))

    def get(self, request, *args, **kwargs):
        usuario = self.get_queryset().first()
        form = self.form_class(instance=usuario)

        return render(request, self.template_name, {
            'form': form,
            'usuario': usuario,
        })

    def form_valid(self, form):
        self.object = User.objects.get(email=form.cleaned_data.get('email'))
        self.object.email = email = form.cleaned_data.get('email')
        self.object.set_password(form.cleaned_data.get('password'))
        self.object.first_name = form.cleaned_data.get('first_name')
        self.object.last_name = form.cleaned_data.get('last_name')
        self.object.biography = form.cleaned_data.get('biography')
        self.object.image = form.cleaned_data.get('image')
        self.object.gender = form.cleaned_data.get('gender')
        self.object.linkedin = form.cleaned_data.get('linkedin')
        self.object.twitter = form.cleaned_data.get('twitter')
        self.object.city = City.objects.get(
            description=form.cleaned_data.get('city'))
        self.object.state = form.cleaned_data.get('state')
        if not form.cleaned_data.get('groups').filter(name='Administrador').exists():
            self.object.is_staff = False
            self.object.is_superuser = False

        self.object.groups.set(form.cleaned_data.get('groups'))

        self.object.save()

        messages.success(
            self.request, self.get_success_message(form.cleaned_data))

        return HttpResponseRedirect(self.get_success_url())


class CitiesListView(LoginRequiredMixin, AdminGroupTest, ListView):
    """
    Vista encargada de mostrar el listado de ciudades en el panel de administracion.
    """

    template_name = 'admin/ciudades/listado-ciudades.html'
    model = City
    queryset = City.objects.all().order_by('-modified')
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['paginacion'] = context['paginator']
        context['ciudades'] = context['paginacion'].get_page(
            self.request.GET.get('page'))

        if self.request.GET.get('q'):
            parametro_busqueda = self.request.GET.get('q')
            context['query'] = self.queryset.filter(
                description__icontains=parametro_busqueda)
            context['resultado'] = context['query'].count()

            if context['resultado'] != 0:
                context['paginacion'] = Paginator(
                    context['query'], 8)
                context['ciudades'] = context['paginacion'].get_page(
                    self.request.GET.get('page'))

        return context


class CityCreateView(SuccessMessageMixin, LoginRequiredMixin, AdminGroupTest, CreateView):
    """
    Vista encargada de crear una ciudad en el panel de administacion.
    """

    template_name = 'admin/ciudades/nueva-ciudad.html'
    model = City
    form_class = CityModelForm
    success_url = reverse_lazy('Admin:cities')
    success_message = 'Ciudad creada exitosamente'


class CityUpdateView(SuccessMessageMixin, LoginRequiredMixin, AdminGroupTest, UpdateView):
    """
    Vista encargada de actualizar una ciudad en el panel de administacion.
    """

    template_name = 'admin/ciudades/editar-ciudad.html'
    model = City
    form_class = CityModelForm
    success_url = reverse_lazy('Admin:cities')
    success_message = 'Ciudad editada exitosamente'

    def get_queryset(self):
        return City.objects.filter(pk=self.kwargs.get('pk'))

    def get(self, request, *args, **kwargs):
        ciudad = self.get_queryset().first()
        form = self.form_class(instance=ciudad)

        return render(request, self.template_name, {
            'form': form,
        })


class CategoriesListView(LoginRequiredMixin, AdminGroupTest, ListView):
    """
    Vista encargada de mostrar el listado de categorias en el panel de administracion.
    """

    template_name = 'admin/categorias/listado-categorias.html'
    model = Category
    queryset = Category.objects.all().order_by('-modified')
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['paginacion'] = context['paginator']
        context['categorias'] = context['paginacion'].get_page(
            self.request.GET.get('page'))

        if self.request.GET.get('q'):
            parametro_busqueda = self.request.GET.get('q')
            context['query'] = Category.objects.filter(
                name__icontains=parametro_busqueda)
            context['resultado'] = context['query'].count()

            if context['resultado'] != 0:
                context['paginacion'] = Paginator(context['query'], 8)
                context['categorias'] = context['paginacion'].get_page(
                    self.request.GET.get('page'))

        return context


class CategoriesCreateView(SuccessMessageMixin, LoginRequiredMixin, AdminGroupTest, CreateView):
    """
    Vista encargada de crear una categoria en el panel de administacion.
    """

    template_name = 'admin/categorias/nueva-categoria.html'
    model = Category
    form_class = CategoryModelForm
    success_url = reverse_lazy('Admin:categories')
    success_message = 'Categoria creada exitosamente'


class CategoryUpdateView(SuccessMessageMixin, LoginRequiredMixin, AdminGroupTest, UpdateView):
    """
    Vista encargada de actualizar una categoria en el panel de administacion.
    """

    template_name = 'admin/categorias/editar-categoria.html'
    model = Category
    form_class = CategoryModelForm
    success_url = reverse_lazy('Admin:categories')
    success_message = 'Categoria editada exitosamente'
    slug_field = 'slug'

    def get_queryset(self):
        return Category.objects.filter(slug=self.kwargs.get('slug'))

    def get(self, request, *args, **kwargs):
        categoria = self.get_queryset().first()
        form = self.form_class(instance=categoria)

        return render(request, self.template_name, {
            'form': form,
        })


class ListArticlesWithComments(LoginRequiredMixin, AdminGroupTest, TemplateView):
    """
    Vista encargada de mostrar el listado de articulos con comentarios en el panel de administacion.
    """

    template_name = 'admin/comentarios/listado-articulos-con-comentarios.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articulos'] = Comment.objects.values('article__name', 'article__slug', 'article__author__first_name', 'article__author__last_name', 'article__author__slug').annotate(
            total=Count('article')).order_by('-article_id')

        return context


class ListCommentsByArticle(LoginRequiredMixin, AdminGroupTest, TemplateView):
    """
    Vista encargada de mostrar el listado de comentarios por articulo en el panel de administracion.
    """

    template_name = 'admin/comentarios/comentarios-por-articulo.html'

    def get(self, request, *args, **kwargs):
        articulo = get_object_or_404(Article, slug=self.kwargs.get('slug'))
        comentarios = Comment.objects.filter(
            article=articulo).order_by('-modified')
        resultado = 0

        if self.request.GET.get('q'):
            parametro_busqueda = self.request.GET.get('q')
            comentarios = Comment.objects.filter(
                Q(author__first_name__icontains=parametro_busqueda) | Q(author__last_name__icontains=parametro_busqueda), article=articulo).order_by('-modified')
            resultado = comentarios.count()

            if comentarios.count() == 0:
                comentarios = Comment.objects.filter(
                    article=articulo).order_by('-modified')

        return render(request, self.template_name, {
            'articulo': articulo,
            'comentarios': comentarios,
            'resultado': resultado
        })


class CommentUpdateView(SuccessMessageMixin, LoginRequiredMixin, AdminGroupTest, UpdateView):
    """
    Vista encargada de actualizar un comentario en el panel de administracion.
    """

    template_name = 'admin/comentarios/editar-comentario.html'
    model = Comment
    form_class = CommentModelForm
    success_message = 'Comentario editado exitosamente'

    def get_queryset(self):
        return Comment.objects.filter(pk=self.kwargs.get('pk'))

    def get(self, request, *args, **kwargs):
        comentario = self.get_queryset().first()
        form = self.form_class(instance=comentario)

        return render(request, self.template_name, {
            'form': form,
        })

    def form_valid(self, form):
        self.object = self.get_queryset().first()
        self.object.author = User.objects.get(
            email=form.cleaned_data.get('author'))
        self.object.article = Article.objects.get(
            name=form.cleaned_data.get('article'))
        self.object.content = form.cleaned_data.get('content')
        self.object.state = form.cleaned_data.get('state')

        self.object.save()

        messages.success(
            self.request, self.get_success_message(form.cleaned_data))

        return HttpResponseRedirect(reverse_lazy('Admin:list-comments-by-article', kwargs={'slug': self.kwargs.get('article')}))
