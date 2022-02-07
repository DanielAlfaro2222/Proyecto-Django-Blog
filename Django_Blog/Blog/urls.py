from django.urls import path
from Blog import views

app_name = 'Blog'

urlpatterns = [
    path('article/<slug:slug>', views.ArticleDetailView.as_view(), name = 'articulo'),
    path('category/<slug:slug>', views.CategoryDetailView.as_view(), name = 'categoria'),
]
