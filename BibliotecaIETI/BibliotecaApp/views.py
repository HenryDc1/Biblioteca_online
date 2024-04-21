from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.models import User
from .forms import ChangePassword
from django.contrib import messages
import json
from django.http import JsonResponse
import requests


# Create your views here.
def index(request):
    if request.method == "POST":
        # Validate using the User model
        username = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Aqui deberia ir un mensaje de exito.
            messages.success(request, 'User Ok')
            return redirect('index')
        else:
            # Aqui deberia ir un mensaje de error.
            messages.success(request, 'Email o contrasenya incorrectes')
            return redirect('index')
    else:
        return render(request, 'myapp/index.html', {})
    
    
def logout_user(request):
    logout(request)
    messages.success(request, 'Fins aviat!')
    return redirect('index')

def canviar_contrasenya(request):
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == "POST":
            form = ChangePassword(current_user,request.POST)
            if form.is_valid():
                new_password = form.cleaned_data['new_password1']
                current_user.set_password(new_password)
                current_user.save()
                update_session_auth_hash(request, current_user)
                messages.success(request, 'Contraseña cambiada correctamente')
                return redirect('index')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)   
                    return render(request, 'myapp/dashboard/canviar_contrasenya.html', {'form': form})             
        else:
            form = ChangePassword(current_user)
            return render(request, 'myapp/dashboard/canviar_contrasenya.html', {'form': form})
    else:
        messages.error(request, 'No estás autenticat. Inicia sessió per canviar la contrasenya.')
        return redirect('index')

    return render(request, 'myapp/dashboard/canviar_contrasenya.html', {})


def cerca_cataleg(request):
    if request.method == 'POST':
        query = request.POST.get('query', '')  # Obtener el término de búsqueda del formulario
        
        # Verificar si la longitud de la consulta es mayor o igual a 3 caracteres
        if len(query) >= 3:
            # Realizar la solicitud a la API de búsqueda
            response = requests.get(f'http://127.0.0.1:8000/get_ItemCatalogo?search={query}')
            
            # Verificar si la solicitud fue exitosa (código de estado 200)
            if response.status_code == 200:
                # Obtener los resultados de la respuesta JSON
                data = response.json().get('ItemCatalogo', [])
                # Renderizar la plantilla con los resultados de la búsqueda
                return render(request, 'myapp/cerca_cataleg.html', {'query': query, 'resultados': data})
            else:
                # Si la solicitud no fue exitosa, mostrar un mensaje de error
                error_message = 'Error al obtener resultados de la búsqueda'
                return render(request, 'myapp/cerca_cataleg.html', {'query': query, 'error_message': error_message})
        else:
            # Si la longitud de la consulta es menor a 3 caracteres, mostrar un mensaje de error
            error_message = 'La consulta debe tener al menos 3 caracteres'
            return render(request, 'myapp/cerca_cataleg.html', {'query': query, 'error_message': error_message})
    else:
        # Si la solicitud no es POST, simplemente renderizar la plantilla sin ningún dato
        return render(request, 'myapp/cerca_cataleg.html')