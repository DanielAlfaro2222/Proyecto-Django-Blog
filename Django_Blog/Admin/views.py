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


class AdminTemplateView(LoginRequiredMixin, AdminGroupTest, TemplateView):
    template_name = 'admin/panel-admin.html'


class ArticlesListView(LoginRequiredMixin, AdminGroupTest, ListView):
    template_name = 'admin/articulos/listado-articulos.html'
    context_object_name = 'articulos'
    model = Article
    queryset = Article.objects.all().order_by('-modified')


class ArticleCreateView(LoginRequiredMixin, AdminGroupTest, CreateView):
    template_name = 'admin/articulos/nuevo-articulo.html'
    model = Article
    form_class = ArticleModelForm
    success_url = reverse_lazy('Admin:articles')
    success_message = 'Articulo creado exitosamente'


class ArticleUpdateView(LoginRequiredMixin, AdminGroupTest, UpdateView):
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
        form = self.form_class({
            'name': articulo.name,
            'image': articulo.image,
            'resume': articulo.resume,
            'content': articulo.content,
            'author': articulo.author,
            'category': articulo.category,
            'state': articulo.state
        })

        return render(request, self.template_name, {
            'form': form,
        })


class UsersListView(LoginRequiredMixin, AdminGroupTest, ListView):
    template_name = 'admin/listado-usuarios.html'
    context_object_name = 'usuarios'
    model = User
    queryset = User.objects.all().order_by('-id_user')


class CitiesListView(LoginRequiredMixin, AdminGroupTest, ListView):
    template_name = 'admin/listado-ciudades.html'
    context_object_name = 'ciudades'
    model = City
    queryset = City.objects.all().order_by('-modified')


class CategoriesListView(LoginRequiredMixin, AdminGroupTest, ListView):
    template_name = 'admin/listado-categorias.html'
    context_object_name = 'categorias'
    model = Category
    queryset = Category.objects.all().order_by('-modified')
