from django.contrib import admin
from .models import User, ItemCatalogo, Libro, CD, DVD, BR, Dispositivo, Ejemplar, Reserva, Prestamo, Peticion, Log, ItemPorCentro, Centro


class LogAdmin(admin.ModelAdmin):
    list_display = ('evento', 'nivel', 'fecha_registro', 'usuario')
    list_filter = ('nivel',)  # Agrega el filtro por nivel

class PrestamoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'ejemplar', 'fecha_prestamo', 'fecha_devolucion')
    list_filter = ('fecha_prestamo',)  # Filtro por fecha de préstamo

class CentroAdmin(admin.ModelAdmin):
    list_display = ('id_centro', 'nombre')
    list_filter = ('nombre',)  # Filtro por nombre

class ItemPorCentroAdmin(admin.ModelAdmin):
    list_display = ('item_id', 'centro_id', 'cantidad_disponible', 'reservado', 'prestado', 'no_disponible')
    list_filter = ('centro_id',)  # Filtro por centro

admin.site.register(User)
admin.site.register(ItemCatalogo)
admin.site.register(Libro)
admin.site.register(CD)
admin.site.register(DVD)
admin.site.register(BR)
admin.site.register(Dispositivo)
admin.site.register(Ejemplar)
admin.site.register(Reserva)
admin.site.register(Prestamo, PrestamoAdmin)
admin.site.register(Peticion)
admin.site.register(Log, LogAdmin)
admin.site.register(ItemPorCentro, ItemPorCentroAdmin)
admin.site.register(Centro, CentroAdmin)

