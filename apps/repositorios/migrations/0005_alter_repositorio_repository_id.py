# Generated by Django 5.0.1 on 2024-01-08 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repositorios', '0004_repositorio_added_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repositorio',
            name='repository_id',
            field=models.IntegerField(),
        ),
    ]