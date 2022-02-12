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
    list_per_page = 15

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id_comment', 'state', 'author', 'article', 'create', 'modified']
    list_per_page = 15