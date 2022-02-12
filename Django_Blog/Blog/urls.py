from django.urls import path
from Blog import views

app_name = 'Blog'

urlpatterns = [
    path('article/<slug:slug>', views.ArticleDetailView.as_view(), name = 'articulo'),
    path('category/<slug:slug>', views.category_view, name = 'categoria'),
    path('add_comment/<slug:slug>', views.add_comment, name = 'agregar_comentario'),
    path('delete_comment/<slug:slug>', views.delete_comment, name = 'eliminar_comentario'),
    path('edit_comment/<slug:slug>', views.edit_comment, name = 'editar_comentario'),
]
