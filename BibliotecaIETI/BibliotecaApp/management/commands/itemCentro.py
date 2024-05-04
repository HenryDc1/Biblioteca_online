import random
from django.core.management.base import BaseCommand
from BibliotecaApp.models import ItemCatalogo, ItemPorCentro, Centro

class Command(BaseCommand):
    help = 'Genera datos de prueba para ItemPorCentro asociados a todos los centros'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Generando datos de prueba para ItemPorCentro...'))

        # Obtener todos los centros disponibles
        centros = Centro.objects.all()

        # Iterar sobre todos los ItemCatalogo y relacionarlos con cada centro
        for item in ItemCatalogo.objects.all():
            # Para cada centro, asignar una cantidad aleatoria entre 0 y 10
            for centro in centros:
                cantidad_disponible = random.randint(0, 10)
                
                # Crear o actualizar el ItemPorCentro
                item_por_centro, created = ItemPorCentro.objects.get_or_create(
                    centro=centro,
                    item=item,
                    defaults={'cantidad_disponible': cantidad_disponible}
                )

                # Si no es creado, actualizar la cantidad disponible
                if not created:
                    item_por_centro.cantidad_disponible = cantidad_disponible
                    item_por_centro.save()

                # Actualizar la cantidad en el ItemCatalogo correspondiente
                item.cantidad += cantidad_disponible
                item.save()

        self.stdout.write(self.style.SUCCESS('Datos de prueba generados exitosamente.'))
