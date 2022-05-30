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
from .models import Like
from django.http import Http404


def category_view(request, slug):
    """
    Vista encargada de ver el detalle de una categoria.
    """

    categoria = Category.objects.get(slug=slug)

    if categoria.state == 'Desactivo' and not request.user.is_staff:
        raise Http404()

    articulos = Article.objects.filter(
        category=categoria, state='Activo').order_by('-id_article')

    if request.GET.get('q'):
        parametro_busqueda = request.GET.get('q')
        articulos = busqueda_articulos_por_categoria(
            request, parametro_busqueda, categoria)

        if articulos.count() == 0:
            messages.error(
                request, f'No se encontraron coincidencias con {parametro_busqueda}')
            articulos = Article.objects.filter(
                category=categoria, state='Activo').order_by('-id_article')
        else:
            messages.success(
                request, f'Se encontraron {articulos.count()} articulos para {request.GET.get("q")}')

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
    """
    Vista encargada de mostrar el detalle de una publicacion.
    """

    template_name = 'blog/detalle-articulo.html'
    model = Article

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articulo'] = context['object']
        context['comentarios'] = Comment.objects.filter(
            article=context['articulo'], state='Activo').order_by('-modified')

        if context['articulo'].state == 'Desactivo' and not self.request.user.is_staff:
            raise Http404()

        return context


@login_required
def add_comment(request, slug):
    """
    Vista encargada de agregar un comentario.
    """

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
    """
    Vista encargada de eliminar un comentario.
    """

    if request.method == 'POST':
        comentario = Comment.objects.get(id_comment=request.POST.get('id'))
        comentario.state = 'Desactivo'
        comentario.save()

        messages.success(request, 'Comentario eliminado con exito!')

    return redirect(reverse('Blog:articulo', kwargs={'slug': slug}))


@login_required
def edit_comment(request, slug):
    """
    Vista encargada de editar un comentario.
    """

    if request.method == 'POST':
        comentario = Comment.objects.get(id_comment=request.POST.get('id'))
        comentario.content = request.POST.get('comentario')
        comentario.save()

        messages.success(request, 'Comentario editado con exito!')

    return redirect(reverse('Blog:articulo', kwargs={'slug': slug}))


@login_required
def like_view(request, slug):
    """
    Vista para dar o quitar el me gusta de una publicacion.
    """

    article = Article.objects.get(slug=slug)
    like = Like.objects.filter(article=article, author=request.user)

    if like.first():
        like.delete()
    else:
        Like.objects.create(article=article, author=request.user)

    return redirect('Blog:articulo', slug)
