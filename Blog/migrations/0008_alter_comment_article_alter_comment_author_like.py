# Generated by Django 4.0.4 on 2022-05-28 19:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Blog', '0007_alter_article_state_alter_category_state_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='article',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Blog.article', verbose_name='Articulo'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Autor'),
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id_like', models.AutoField(primary_key=True, serialize=False, verbose_name='Id like')),
                ('create', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creacion')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Fecha de modificacion')),
                ('state', models.CharField(choices=[('Activo', 'Activo'), ('Desactivo', 'Desactivo')], default='Activo', max_length=10, verbose_name='Estado')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Blog.article', verbose_name='Articulo')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Autor')),
            ],
            options={
                'verbose_name': 'Me gusta',
                'verbose_name_plural': 'Me gustas',
                'db_table': 'Me gusta',
                'ordering': ['id_like'],
            },
        ),
    ]