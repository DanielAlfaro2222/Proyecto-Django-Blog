from .models import Article
from django.db.models import Q

# Busca todos los articulos que coincidan con el parametro de busqueda, sin importar la categoria
def busqueda_articulos(request, parametro_busqueda):
    resultado = Article.objects.filter(
        Q(name__icontains = parametro_busqueda) | 
        Q(resume__icontains = parametro_busqueda) | Q(content__icontains = parametro_busqueda), state = True
    ).order_by('-id_article')

    return resultado

# Buscar todos los articulos relacionados a una categoria que coincidan con el parametro de busqueda 
def busqueda_articulos_por_categoria(request, parametro_busqueda, categoria):
    resultado = Article.objects.filter(
        Q(name__icontains = parametro_busqueda) | 
        Q(resume__icontains = parametro_busqueda) | Q(content__icontains = parametro_busqueda), state = True,
        category = categoria
    ).order_by('-id_article')

    return resultado