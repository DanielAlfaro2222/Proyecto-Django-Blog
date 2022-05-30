from .models import Article
from django.db.models import Q


def busqueda_articulos(request, parametro_busqueda):
    """
    Funcion de ayuda para buscar todos los articulos que coincidan con el parametro de busqueda, sin importar la categoria.
    """

    resultado = Article.objects.filter(
        Q(name__icontains=parametro_busqueda) |
        Q(resume__icontains=parametro_busqueda) | Q(content__icontains=parametro_busqueda), state='Activo'
    ).order_by('-id_article')

    return resultado


def busqueda_articulos_por_categoria(request, parametro_busqueda, categoria):
    """
    Funcion de ayuda para buscar todos los articulos relacionados a una categoria que coincidan con el parametro de busqueda.
    """

    resultado = Article.objects.filter(
        Q(name__icontains=parametro_busqueda) |
        Q(resume__icontains=parametro_busqueda) | Q(content__icontains=parametro_busqueda), state='Activo',
        category=categoria
    ).order_by('-id_article')

    return resultado
