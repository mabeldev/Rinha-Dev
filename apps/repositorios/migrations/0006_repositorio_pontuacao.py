# Generated by Django 5.0.1 on 2024-01-08 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repositorios', '0005_alter_repositorio_repository_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='repositorio',
            name='pontuacao',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
