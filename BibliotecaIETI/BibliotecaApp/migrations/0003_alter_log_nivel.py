# Generated by Django 5.0.4 on 2024-04-22 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BibliotecaApp', '0002_alter_libro_isbn_alter_libro_coleccion_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='nivel',
            field=models.CharField(choices=[('INFO', 'INFO'), ('WARNING', 'WARNING'), ('ERROR', 'ERROR'), ('FATAL', 'FATAL')], max_length=20),
        ),
    ]