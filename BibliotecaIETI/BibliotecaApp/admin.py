from django.contrib import admin
from .models import User, ItemCatalogo, Libro, CD, DVD, BR, Dispositivo, Ejemplar, Reserva, Prestamo, Peticion, Log


class LogAdmin(admin.ModelAdmin):
    list_display = ('evento', 'nivel', 'fecha_registro', 'usuario')
    list_filter = ('nivel',)  # Agrega el filtro por nivel

class PrestamoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'ejemplar', 'fecha_prestamo', 'fecha_devolucion')
    list_filter = ('fecha_prestamo',)  # Filtro por fecha de préstamo

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

