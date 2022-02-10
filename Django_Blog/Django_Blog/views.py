from django.shortcuts import render
from Blog.models import Article
from Blog.utils import busqueda_articulos
from django.contrib import messages
from django.core.paginator import Paginator

def index_view(request):
    articulos = Article.objects.all().order_by('-id_article')

    if request.GET.get('q'):
        parametro_busqueda = request.GET.get('q')

        if len(busqueda_articulos(request, parametro_busqueda)) == 0:
            messages.error(request, f'No se encontraron coincidencias con {parametro_busqueda}')
        else:
            articulos = busqueda_articulos(request, request.GET.get('q'))

    # Paginacion por cada 5 articulos
    paginacion = Paginator(articulos, 5)
    num_pagina = request.GET.get('page')
    articulos = paginacion.get_page(num_pagina)

    return render(request, 'index.html', context = {
        'articulos': articulos,
        'paginacion': paginacion,
    })