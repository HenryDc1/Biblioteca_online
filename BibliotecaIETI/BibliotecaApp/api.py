from django.http import JsonResponse
from .models import *
 
 
def get_ItemCatalogo(request):
    query = request.GET.get('search', '')
    if query:
        # Filtrar los resultados según la consulta
        jsonData = list(ItemCatalogo.objects.filter(titulo__icontains=query).values())
    else:
        # Si no hay consulta, devolver todos los elementos
        jsonData = list(ItemCatalogo.objects.all().values())
    
    return JsonResponse({
        "status": "OK",
        "ItemCatalogo": jsonData,
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