# Generated by Django 4.0.4 on 2022-06-12 00:58

import Django_Blog.utils
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id_article', models.AutoField(primary_key=True, serialize=False, verbose_name='Id articulo')),
                ('name', models.CharField(max_length=55, unique=True, verbose_name='Nombre')),
                ('image', models.ImageField(upload_to='article/images', validators=[Django_Blog.utils.validate_image], verbose_name='Imagen')),
                ('content', models.TextField(verbose_name='Contenido')),
                ('resume', models.CharField(max_length=150, verbose_name='Descripcion del articulo')),
                ('create', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creacion')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Fecha de modificacion')),
                ('slug', models.SlugField(blank=True, max_length=255, null=True, verbose_name='Url')),
                ('state', models.CharField(choices=[('Activo', 'Activo'), ('Desactivo', 'Desactivo')], default='Activo', max_length=10, verbose_name='Estado')),
            ],
            options={
                'verbose_name': 'Articulo',
                'verbose_name_plural': 'Articulos',
                'db_table': 'Articulo',
                'ordering': ['id_article'],
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id_category', models.AutoField(primary_key=True, serialize=False, verbose_name='Id categoria')),
                ('name', models.CharField(max_length=45, unique=True, verbose_name='Nombre categoria')),
                ('slug', models.SlugField(blank=True, max_length=255, null=True, verbose_name='Url')),
                ('create', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creacion')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Fecha de modificacion')),
                ('state', models.CharField(choices=[('Activo', 'Activo'), ('Desactivo', 'Desactivo')], default='Activo', max_length=10, verbose_name='Estado')),
            ],
            options={
                'verbose_name': 'Categoria',
                'verbose_name_plural': 'Categorias',
                'db_table': 'Categoria',
                'ordering': ['id_category'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id_comment', models.AutoField(primary_key=True, serialize=False, verbose_name='Id comentario')),
                ('content', models.TextField(verbose_name='Contenido')),
                ('create', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creacion')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Fecha de modificacion')),
                ('state', models.CharField(choices=[('Activo', 'Activo'), ('Desactivo', 'Desactivo')], default='Activo', max_length=10, verbose_name='Estado')),
            ],
            options={
                'verbose_name': 'Comentario',
                'verbose_name_plural': 'Comentarios',
                'db_table': 'Comentario',
                'ordering': ['id_comment'],
            },
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id_like', models.AutoField(primary_key=True, serialize=False, verbose_name='Id like')),
                ('create', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creacion')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Fecha de modificacion')),
                ('state', models.CharField(choices=[('Activo', 'Activo'), ('Desactivo', 'Desactivo')], default='Activo', max_length=10, verbose_name='Estado')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Blog.article', verbose_name='Articulo')),
            ],
            options={
                'verbose_name': 'Me gusta',
                'verbose_name_plural': 'Me gustas',
                'db_table': 'Me gusta',
                'ordering': ['id_like'],
            },
        ),
    ]
