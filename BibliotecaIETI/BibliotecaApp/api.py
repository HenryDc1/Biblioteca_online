from django.forms import model_to_dict
from django.http import JsonResponse
from .models import *
from django.db.models import Q

from django.db.models import Sum, F

from django.db.models.functions import ExtractYear

def get_ItemCatalogo(request):
    query = request.GET.get('search', '')
    only_available = request.GET.get('only_available', '')
    max_year = request.GET.get('maxYearSearch', '')
    min_year = request.GET.get('minYearSearch', '')
    tipo_ocio_search = request.GET.getlist('tipo') 
    centro_search = request.GET.getlist('centro')  
    estado_search = request.GET.getlist('estado')
    

    
    # Obtener todos los elementos del catálogo
    items = ItemCatalogo.objects.all()

    # Filtrar los resultados según la consulta (título o autor) si está presente
    if query:
        items = items.filter(Q(titulo__icontains=query) | Q(autor__icontains=query))

    # Filtrar los resultados por disponibilidad si se solicita
    if only_available == 'true':
        items = items.annotate(total_disponible=Sum('itemporcentro__cantidad_disponible'))
        items = items.filter(total_disponible__gt=0)
        
    if tipo_ocio_search:  
        items = items.filter(ocio__in=tipo_ocio_search)
        
    if centro_search:
        # Filtrar los elementos por centro que tengan al menos una cantidad disponible 
        items = items.filter(itemporcentro__centro__id_centro__in=centro_search, itemporcentro__cantidad_disponible__gt=0)
        # comprobar que no hayan duplicados
        items = items.distinct()
        
    if estado_search:
        for estado in estado_search:
            if estado == 'Disponible':
                items = items.filter(cantidad_disponible__gt=0)
            elif estado == 'Reservat':
                items = items.filter(reservado__gt=0)
            elif estado == 'Prestat':
                items = items.filter(prestado__gt=0)
            elif estado == 'No disponible':
                items = items.filter(no_disponible__gt=0)
            else:
                return JsonResponse({'status': 'Error', 'message': 'Estado no válido'}, status=400)

    if max_year.isdigit() and min_year.isdigit():
        items = items.annotate(year=ExtractYear('data_edicion'))
        items = items.filter(year__lte=int(max_year), year__gte=int(min_year))

    # Crear una lista para almacenar los datos de los items junto con la información de los centros
    items_data = []
    for item in items:
        item_data = model_to_dict(item)
        centros_data = list(ItemPorCentro.objects.filter(item=item).values('item_id', 'centro_id', 'cantidad_disponible', 'reservado', 'prestado', 'no_disponible'))
        item_data['centros'] = centros_data

        items_data.append(item_data)

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