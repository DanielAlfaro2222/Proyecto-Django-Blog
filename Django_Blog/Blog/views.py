from django.shortcuts import render
from django.views.generic.detail import DetailView
from .models import Article
from .models import Category
from .utils import busqueda_articulos_por_categoria
from django.contrib import messages
from .models import Comment
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.urls import reverse


def category_view(request, slug):
    categoria = Category.objects.get(slug=slug)
    articulos = Article.objects.filter(
        category=categoria, state=True).order_by('-id_article')

    if request.GET.get('q'):
        parametro_busqueda = request.GET.get('q')

        if len(busqueda_articulos_por_categoria(request, parametro_busqueda, categoria)) == 0:
            messages.error(
                request, f'No se encontraron coincidencias con {parametro_busqueda}')
        else:
            articulos = busqueda_articulos_por_categoria(
                request, parametro_busqueda, categoria)

    # Paginacion por cada 8 articulos
    paginacion = Paginator(articulos, 8)
    num_pagina = request.GET.get('page')
    articulos = paginacion.get_page(num_pagina)

    return render(request, 'blog/detalle-categoria.html', context={
        'categoria': categoria,
        'articulos': articulos,
        'paginacion': paginacion
    })


class ArticleDetailView(DetailView):
    template_name = 'blog/detalle-articulo.html'
    model = Article

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articulo'] = context['object']
        context['comentarios'] = Comment.objects.filter(
            article=context['articulo'], state=True).order_by('-modified')

        return context


@login_required
def add_comment(request, slug):
    if request.method == 'POST':
        comentario = Comment.objects.create(
            author=request.user,
            article=Article.objects.get(slug=slug),
            content=request.POST.get('comentario')
        )
        messages.success(request, 'Comentario agregado con exito!')

    return redirect(reverse('Blog:articulo', kwargs={'slug': slug}))


@login_required
def delete_comment(request, slug):
    if request.method == 'POST':
        comentario = Comment.objects.get(id_comment=request.POST.get('id'))
        comentario.state = False
        comentario.save()

        messages.success(request, 'Comentario eliminado con exito!')

    return redirect(reverse('Blog:articulo', kwargs={'slug': slug}))


@login_required
def edit_comment(request, slug):
    if request.method == 'POST':
        comentario = Comment.objects.get(id_comment=request.POST.get('id'))
        comentario.content = request.POST.get('comentario')
        comentario.save()

        messages.success(request, 'Comentario editado con exito!')

    return redirect(reverse('Blog:articulo', kwargs={'slug': slug}))
