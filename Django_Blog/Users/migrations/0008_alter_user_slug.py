# Generated by Django 4.0.2 on 2022-05-05 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0007_alter_user_biography'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True, verbose_name='Url'),
        ),
    ]
