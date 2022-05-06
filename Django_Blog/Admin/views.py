from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic import ListView
from .utils import AdminGroupTest
from django.contrib.auth.mixins import LoginRequiredMixin
from Users.models import User
from Blog.models import Article
from Users.models import City
from Blog.models import Category


class AdminTemplateView(LoginRequiredMixin, AdminGroupTest, TemplateView):
    template_name = 'admin/panel-admin.html'


class UsersListView(LoginRequiredMixin, AdminGroupTest, ListView):
    template_name = 'admin/listado-usuarios.html'
    context_object_name = 'usuarios'
    model = User
    queryset = User.objects.all().order_by('-id_user')


class ArticlesListView(LoginRequiredMixin, AdminGroupTest, ListView):
    template_name = 'admin/listado-articulos.html'
    context_object_name = 'articulos'
    model = Article
    queryset = Article.objects.all().order_by('-modified')


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
