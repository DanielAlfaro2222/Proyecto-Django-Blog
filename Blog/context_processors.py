from .models import Category


def get_categories(request):
    categorias = Category.objects.filter(state='Activo')

    return {'categorias': categorias}
