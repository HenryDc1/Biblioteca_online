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