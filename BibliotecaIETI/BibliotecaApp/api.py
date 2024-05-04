from django.forms import model_to_dict
from django.http import JsonResponse
from .models import *
from django.db.models import Q

from django.db.models import Sum, F

def get_ItemCatalogo(request):
    query = request.GET.get('search', '')
    only_available = request.GET.get('only_available', '')

    # Obtener todos los elementos del catálogo
    items = ItemCatalogo.objects.all()

    # Filtrar los resultados según la consulta (título o autor) si está presente
    if query:
        items = items.filter(Q(titulo__icontains=query) | Q(autor__icontains=query))

    # Filtrar los resultados por disponibilidad si se solicita
    if only_available == 'true':
        items = items.annotate(total_disponible=Sum('itemporcentro__cantidad_disponible'))
        items = items.filter(total_disponible__gt=0)

    # Crear una lista para almacenar los datos de los items junto con la información de los centros
    items_data = []
    for item in items:
        item_data = model_to_dict(item)  # Convertir el objeto modelo a un diccionario
        # Obtener la información de los centros para este item y agregarla al diccionario de datos del item
        centros_data = list(ItemPorCentro.objects.filter(item=item).values('centro_id', 'cantidad_disponible', 'reservado', 'prestado', 'no_disponible'))
        item_data['centros'] = centros_data

        items_data.append(item_data)

    return JsonResponse({
        "status": "OK",
        "ItemCatalogo": items_data,
    }, safe=False)

    
    
    
    
def create_log(request):
    if request.method == 'POST':
        evento = request.POST.get('evento', '')
        nivel = request.POST.get('nivel', '')

        if evento and nivel:
            # Crear una nueva instancia del modelo Log
            log = Log.objects.create(evento=evento, nivel=nivel)
            # Devolver una respuesta JSON indicando que el registro se ha creado correctamente
            return JsonResponse({'status': 'OK', 'message': 'Log creado correctamente'}, status=201)
        else:
            # Si falta algún dato, devolver un error
            return JsonResponse({'status': 'Error', 'message': 'Faltan datos en la solicitud'}, status=400)
    else:
        # Si la solicitud no es POST, devolver un error de método no permitido
        return JsonResponse({'status': 'Error', 'message': 'Método no permitido'}, status=405)