from django.shortcuts import render
from django.views.generic.detail import DetailView
from .models import Article
from .models import Category

class CategoryDetailView(DetailView):
    template_name = 'blog/detalle-categoria.html'
    model = Category

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categoria'] = context['object']
        context['articulos'] = Article.objects.filter(category = context['object'], state = True).order_by('-id_article')

        return context


class ArticleDetailView(DetailView):
    template_name = 'blog/detalle-articulo.html'
    model = Article

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articulo'] = context['object']

        return context