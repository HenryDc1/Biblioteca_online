# Generated by Django 5.0.4 on 2024-05-01 15:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BibliotecaApp', '0003_prestamo_devuelto'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='prestamo',
            options={'ordering': ['fecha_devolucion']},
        ),
    ]
