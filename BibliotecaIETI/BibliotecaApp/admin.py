from django.contrib import admin
from .models import User, ItemCatalogo, Libro, CD, DVD, BR, Dispositivo, Ejemplar, Reserva, Prestamo, Peticion, Log




admin.site.register(User)
admin.site.register(ItemCatalogo)
admin.site.register(Libro)
admin.site.register(CD)
admin.site.register(DVD)
admin.site.register(BR)
admin.site.register(Dispositivo)
admin.site.register(Ejemplar)
admin.site.register(Reserva)
admin.site.register(Prestamo)
admin.site.register(Peticion)
admin.site.register(Log)

