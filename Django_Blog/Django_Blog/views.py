from django.shortcuts import render
from Blog.models import Article

def index_view(request):
    articulos = Article.objects.all().order_by('-id_article')

    return render(request, 'index.html', context = {'articulos': articulos})