import os
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.utils import formats
from datetime import datetime
from dateutil import parser
from .forms import ChangePassword, Importar
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
import requests
from .models import Log, User
from django.views.decorators.csrf import csrf_exempt
import csv
from django.core.files.uploadedfile import SimpleUploadedFile

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
            registrar_evento(f'Inicio de sesión exitoso', 'INFO', request.user)
            messages.success(request, 'Inici de sessió correcte!')
            return redirect('index')
        else:
            # Aqui deberia ir un mensaje de error.
            registrar_evento('Inici de sessió fallit', 'ERROR')
            messages.error(request, 'Email o contrasenya incorrectes')
            return redirect('index')
    else:
        return render(request, 'myapp/index.html', {})
    

@login_required
def usuari(request):
    users = User.objects.all()

    # actualizar datos del usuario
    if request.method == "POST":
        user_id = request.POST.get('id')

        if user_id:
            try:
                user = User.objects.get(pk=user_id)
                user.first_name = request.POST.get('first_name', user.first_name)
                user.last_name = request.POST.get('last_name', user.last_name)
                user.centro = request.POST.get('centro', user.centro)
                user.ciclo = request.POST.get('ciclo', user.ciclo)
                user.fecha_nacimiento = parser.parse(request.POST.get('fecha_nacimiento', user.fecha_nacimiento))
                user.save()
                messages.success(request, 'Datos actualizados correctamente')
                registrar_evento(f'Datos de "{user}" actualizados correctamente', 'INFO')
                return redirect('usuari')
            except User.DoesNotExist:
                messages.error(request, 'El usuario no existe')
                registrar_evento(f'Intento de actualización de datos para un usuario inexistente', 'ERROR')
                return redirect('usuari')
        else:
            messages.error(request, 'Falta el campo ID')
            registrar_evento('Intento de actualización de datos sin ID', 'ERROR')
            return redirect('usuari')

    # Obtener fecha de nacimiento del usuario
    fecha_nacimiento = None
    if request.user.fecha_nacimiento:
        fecha_nacimiento = request.user.fecha_nacimiento.strftime('%Y-%m-%d')

    return render(request, 'myapp/dashboard/usuari.html', {'users': users, 'fecha_nacimiento': fecha_nacimiento})

@login_required
def dashboard(request):
    return render(request, 'myapp/dashboard/dashboard.html')

@login_required
def logout_user(request):
    logout(request)
    messages.info(request, 'Fins aviat!')
    registrar_evento('Sessió tancada amb èxit', 'INFO')
    return redirect('index')

@login_required
def canviar_contrasenya(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Actualiza la sesión para que el usuario no sea deslogueado
            messages.success(request, 'Contraseña cambiada correctamente')
            registrar_evento('Contrasenya canviada correctament', 'INFO')
            return redirect('usuari')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = PasswordChangeForm(request.user)
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
    
def registrar_evento(evento, nivel, usuario=None):
    # Si no se proporciona un usuario, se asumirá como Anónimo
    if usuario is None:
        usuario = User.objects.get(username='Anonimo')

    # Crear el registro de log
    Log.objects.create(evento=evento, nivel=nivel, usuario=usuario)

@csrf_exempt
def guardar_log(request):
    if request.method == 'POST':
        evento = request.POST.get('evento')
        nivel = request.POST.get('nivel')
        
        if request.user.is_authenticated:
            usuario = request.user
        else:
            usuario_anonimo = User.objects.get(username='Anonimo')
            usuario = usuario_anonimo
        
        Log.objects.create(evento=evento, nivel=nivel, usuario=usuario)
        
        return JsonResponse({'mensaje': 'Log guardado correctamente.'})
    else:
        return JsonResponse({'error': 'Método no permitido.'}, status=405)

def process_csv(csv_file, centre_educatiu,request):
    # Guardar el archivo CSV en el sistema de archivos
    file_path = os.path.join('/home/super/Baixades/', csv_file.name)
    with open(file_path, 'wb+') as destination:
        for chunk in csv_file.chunks():
            destination.write(chunk)
    
    # Ahora abrir el archivo CSV desde la ubicación guardada
    with open(file_path, 'r', encoding='ISO-8859-1') as file:
        csv_reader = csv.reader(file, delimiter=',')
        # Iterar sobre cada fila del archivo CSV
        for line_number, row in enumerate(csv_reader, start=1):
            try:
                # Supongamos que el archivo CSV tiene el formato: nombre, apellidos, email, fecha de nacimiento, ciclo, roles
                username, last_name, email, fecha_nacimiento, ciclo, centro, roles, telefono  = row
                # Crea un nuevo objeto User y asigna los valores
                user = User(
                    username=username,
                    last_name=last_name,
                    email=email,
                    fecha_nacimiento=fecha_nacimiento,
                    centro=centre_educatiu,
                    ciclo=ciclo,
                    roles=roles, # Guarda la imagen y asigna la ruta
                    telefono=telefono
                )
                # Guarda el objeto User en la base de datos
                user.save()
            except ValueError:
                # Manejar el caso donde la fila no tiene el formato correcto
                messages.warning(request, f"Línea {line_number}: No se importó correctamente. Formato incorrecto.")

# En tu vista Django
def upload_file(request):
    if request.method == 'POST':
        form = Importar(request.POST, request.FILES)
        if form.is_valid():  # Verificar si el formulario es válido
            csv_file = request.FILES.get('csv_file')  # Obtener el archivo CSV si existe
            if csv_file:  # Verificar si se proporcionó un archivo CSV
                print("Paso por aqui 2") 
                centre_educatiu = form.cleaned_data.get('centre_educatiu') 
                process_csv(csv_file, centre_educatiu,request)
                messages.success(request, 'El archivo CSV se ha importado correctamente.')
                return render(request, 'myapp/dashboard/importar.html', {'form': form})
            else:
                # Manejar el caso donde no se proporciona el archivo CSV
                messages.error(request, 'No se proporcionó un archivo CSV')
                print(form.errors)  # Imprime los errores del formulario en la consola
    else:
        form = Importar()
        print("Paso por aqui 3") 
    return render(request, 'myapp/dashboard/importar.html', {'form': form})