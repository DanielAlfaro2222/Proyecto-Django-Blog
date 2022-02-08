from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from Users.models import User
import uuid

class Category(models.Model):
    id_category = models.AutoField('Id categoria', primary_key = True)
    name = models.CharField('Nombre categoria', max_length = 45, unique = True)
    slug = models.SlugField('Url', null = True, blank = True)
    create = models.DateTimeField('Fecha de creacion', auto_now_add = True)
    modified = models.DateTimeField('Fecha de modificacion', auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['id_category']
        db_table = 'Categoria'

class Article(models.Model):
    id_article = models.AutoField('Id articulo', primary_key = True)
    name = models.CharField('Nombre', max_length = 55, unique = True)
    image = models.ImageField('Imagen', upload_to = 'article/images')
    content = models.TextField('Contenido')
    resume = models.CharField('Descripcion del articulo', max_length = 150)
    create = models.DateTimeField('Fecha de creacion', auto_now_add = True)
    modified = models.DateTimeField('Fecha de modificacion', auto_now =True)
    author = models.ForeignKey(User, verbose_name = 'Autor', on_delete = models.DO_NOTHING)
    category = models.ForeignKey(Category, verbose_name = 'Categoria', on_delete = models.DO_NOTHING)
    slug = models.SlugField('Url', null = True, blank = True)
    state = models.BooleanField('Estado', default = True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Articulo'
        verbose_name_plural = 'Articulos'
        ordering = ['id_article']
        db_table = 'Articulo'


# Creacion del callback para asignar el slug unico a cada categoria
def set_slug_category(sender, instance, *args, **kwargs):
    if instance.name and not instance.slug:
        slug = slugify(instance.name)

        while Category.objects.filter(slug = slug).exists():
            slug = slugify(
                f'{instance.name}-{str(uuid.uuid4())[:5]}'
            )

        instance.slug = slug

# Unir el callback al modelo category
pre_save.connect(set_slug_category, sender = Category)

# Creacion del callback para asignar el slug unico a cada articulo
def set_slug_articulo(sender, instance, *args, **kwargs):
    if instance.name and not instance.slug:
        slug = slugify(instance.name)

        while Article.objects.filter(slug = slug).exists():
            slug = slugify(
                f'{instance.name}-{str(uuid.uuid4())[:5]}'
            )

        instance.slug = slug

# Unir el callback al modelo category
pre_save.connect(set_slug_articulo, sender = Article)