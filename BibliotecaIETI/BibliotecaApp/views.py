from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from .forms import ChangePassword
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
import requests
from .models import Log, User

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
            registrar_evento(f'Inici de sessió "{user}" reeixit', 'INFO')
            messages.success(request, 'User Ok')
            return redirect('index')
        else:
            # Aqui deberia ir un mensaje de error.
            registrar_evento('Inici de sessió fallit', 'ERROR')
            messages.success(request, 'Email o contrasenya incorrectes')
            return redirect('index')
    else:
        return render(request, 'myapp/index.html', {})
    
@login_required
def dashboard(request):
    users = User.objects.all()
    # actualizar dades del usuari
    if request.method == "POST":
        user_id = request.POST.get('id')
        if user_id:
            try:
                user = User.objects.get(pk=user_id)
                user.first_name = request.POST.get('first_name', user.first_name)
                user.last_name = request.POST.get('last_name', user.last_name)
                user.centro = request.POST.get('centro', user.centro)
                user.ciclo = request.POST.get('ciclo', user.ciclo)
                user.save()
                messages.success(request, 'Dades actualitzades correctament')
                registrar_evento(f'Dades de "{user}" actualitzades correctament', 'INFO')
                return redirect('dashboard')
            except User.DoesNotExist:
                messages.error(request, 'El usuari no existeix')
                registrar_evento(f'Intent d\'actualització de dades per a un usuari inexistent', 'ERROR')
                return redirect('dashboard')
        else:
            messages.error(request, 'Falta el camp ID')
            registrar_evento('Intent d\'actualització de dades sense ID', 'ERROR')
            return redirect('dashboard')
    return render(request, 'myapp/dashboard/dashboard.html', {'users': users})


def logout_user(request):
    logout(request)
    messages.success(request, 'Fins aviat!')
    registrar_evento('Sessió tancada amb èxit', 'INFO')
    return redirect('index')

@login_required
def canviar_contrasenya(request):
    if request.method == "POST":
        form = ChangePassword(request.user, request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password1']
            request.user.set_password(new_password)
            request.user.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, 'Contraseña cambiada correctamente')
            registrar_evento('Contrasenya canviada correctament', 'INFO')
            return redirect('index')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)   
            return render(request, 'myapp/dashboard/canviar_contrasenya.html', {'form': form})             
    else:
        form = ChangePassword(request.user)
        return render(request, 'myapp/dashboard/canviar_contrasenya.html', {'form': form})
    


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
                registrar_evento('Error al obtener resultados de la búsqueda', 'ERROR')
                return render(request, 'myapp/cerca_cataleg.html', {'query': query, 'error_message': error_message})
        else:
            # Si la longitud de la consulta es menor a 3 caracteres, mostrar un mensaje de error
            error_message = 'La consulta debe tener al menos 3 caracteres'
            return render(request, 'myapp/cerca_cataleg.html', {'query': query, 'error_message': error_message})
    else:
        # Si la solicitud no es POST, simplemente renderizar la plantilla sin ningún dato
        return render(request, 'myapp/cerca_cataleg.html')
    
def registrar_evento(evento, nivel):
    Log.objects.create(evento=evento, nivel=nivel)