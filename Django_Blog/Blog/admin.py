from django.contrib import admin
from .models import Category
from .models import Comment
from .models import Article

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'create', 'modified']

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = [
        'name', 
        'author', 
        'category', 
        'image', 
        'state', 
        'create', 
        'modified'
    ]

admin.site.register(Comment)