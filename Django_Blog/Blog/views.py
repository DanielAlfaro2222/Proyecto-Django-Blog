from django.shortcuts import render
from django.views.generic.detail import DetailView
from .models import Article
from .models import Category
from .utils import busqueda_articulos_por_categoria
from django.contrib import messages

# class CategoryDetailView(DetailView):
#     template_name = 'blog/detalle-categoria.html'
#     model = Category

#     def articulos_categoria(request, categoria):
#         # Aca suponemos que no se ha realizado ninguna busqueda en la categoria, por ende trae todos los articulos de la categoria
#         resultado = Article.objects.filter(category = categoria, state = True).order_by('-id_article')

#         if request.GET.get('q'):
#             parametro_busqueda = request.GET.get('q')

#             if len(busqueda_articulos_por_categoria(request, parametro_busqueda, categoria)) == 0:
#                 messages.error(request, f'No se encontraron coincidencias con {parametro_busqueda}')
#             else:
#                 resultado = busqueda_articulos_por_categoria(request, parametro_busqueda, categoria)

#         return resultado

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['categoria'] = context['object']
#         context['articulos'] = self.articulos_categoria(request, context['categoria'])

#         return context

def category_view(request, slug):
    categoria = Category.objects.get(slug = slug)
    articulos = Article.objects.filter(category = categoria, state = True).order_by('-id_article')

    if request.GET.get('q'):
        parametro_busqueda = request.GET.get('q')

        if len(busqueda_articulos_por_categoria(request, parametro_busqueda, categoria)) == 0:
            messages.error(request, f'No se encontraron coincidencias con {parametro_busqueda}')
        else:
            articulos = busqueda_articulos_por_categoria(request, parametro_busqueda, categoria)

    return render(request, 'blog/detalle-categoria.html', context = {
        'categoria': categoria,
        'articulos': articulos
    })



class ArticleDetailView(DetailView):
    template_name = 'blog/detalle-articulo.html'
    model = Article

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articulo'] = context['object']

        return context