from django.forms import model_to_dict
from django.http import JsonResponse
from .models import *
from django.db.models import Q

def get_ItemCatalogo(request):
    query = request.GET.get('search', '')
    only_available = request.GET.get('only_available', '')
    
    # Obtener todos los elementos del catálogo disponibles
    if only_available == 'true':
        # Filtrar los resultados por el término de búsqueda y la disponibilidad
        if query:
            items = ItemCatalogo.objects.filter(Q(titulo__icontains=query) | Q(autor__icontains=query), cantidad_disponible__gt=0)
        else:
            items = ItemCatalogo.objects.filter(cantidad_disponible__gt=0)
    else:
        # Si no se especifica que solo se quieren los disponibles, devolver todos los elementos
        if query:
            # Filtrar los resultados según la consulta
            items = ItemCatalogo.objects.filter(Q(titulo__icontains=query) | Q(autor__icontains=query))
        else:
            # Si no hay consulta, devolver todos los elementos
            items = ItemCatalogo.objects.all()
    
    # Crear una lista para almacenar los datos de los items junto con la información de los centros
    items_data = []
    for item in items:
        item_data = model_to_dict(item)  # Convertir el objeto modelo a un diccionario
        # Obtener la información de los centros para este item y agregarla al diccionario de datos del item
        centros_data = list(ItemPorCentro.objects.filter(item=item).values('item_id', 'centro_id', 'cantidad_disponible', 'reservado', 'prestado', 'no_disponible'))
        item_data['centros'] = centros_data
        
        items_data.append(item_data)
        # añadir cdu de libro a partir de la tabla libro (Si empieza por "LB"):
        if item.id_catalogo[:2] == "LB":
            libro = Libro.objects.get(id_catalogo=item.id_catalogo)
            item_data['CDU'] = libro.CDU
            item_data['ISBN'] = libro.ISBN

        
        
    
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