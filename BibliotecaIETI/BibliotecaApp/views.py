import unicodedata
import codecs
import hashlib
import os
import time
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.utils import formats, timezone
from datetime import datetime
from dateutil import parser
from .forms import ChangePassword, Importar
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
import requests
from .models import Centro, Libro, Log, Prestamo, User, ItemCatalogo, Ejemplar, CD, DVD, BR, Dispositivo
from django.views.decorators.csrf import csrf_exempt
import csv
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from django.db.models import Q
from .forms import UserForm
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator


# Create your views here.
def index(request):
    if request.method == "POST":

        # Validate using the User model
        username = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if not user.has_password_changed:
                if user.email == 'admin@admin.com':
                    user.has_password_changed = True
                    user.save()
                    registrar_evento(f'Inicio de sesión exitoso', 'INFO', request.user)
                    messages.success(request, 'Inici de sessió correcte!')
                    return redirect('index')
                else:
                    messages.warning(request, 'La contrasenya predeterminada és insegura. Canvia-la ara mateix per poder accedir als continguts.')
                    return redirect('canviar_contrasenya')
            else:
                # Aqui deberia ir un mensaje de exito.
                registrar_evento(f'Inicio de sesión exitoso', 'INFO', request.user)
                messages.success(request, 'Inici de sessió correcte!')
                return redirect('dashboard')
        else:
            # Aqui deberia ir un mensaje de error.
            registrar_evento('Inici de sessió fallit', 'ERROR')
            messages.error(request, 'Email o contrasenya incorrectes')
            return redirect('index')
    else:
        return render(request, 'myapp/index.html', {})
    

@login_required
def usuari(request):
    user = request.user
    if not user.has_password_changed:
        messages.warning(request, 'La contrasenya predeterminada és insegura. Canvia-la ara mateix per poder accedir als continguts.')
        return render(request, 'myapp/dashboard/canviar_contrasenya.html')
    users = User.objects.all()

    # actualizar datos del usuario
    if request.method == "POST":
        user_id = request.POST.get('id')
        if user_id:
            try:
                user = User.objects.get(pk=user_id)
                image_file = request.FILES.get('image')

                # DESARROLLO:
                if image_file:
                    # Generar un nombre único para la imagen utilizando un hash
                    hash_object = hashlib.md5(image_file.read())
                    hashed_name = hash_object.hexdigest() + '.png'

                    # Guardar la imagen en el directorio adecuado
                    file_path = os.path.join(settings.STATIC_ROOT)
                    with open(file_path, 'wb+') as destination:
                        for chunk in image_file.chunks():
                            destination.write(chunk)
                    
                    # Asignar el nombre de la imagen al usuario
                    user.image = request.FILES.get('image')


                ''' PRODUCCION:
                if image_file:
                    # Generar un nombre único para la imagen utilizando un hash
                    hash_object = hashlib.md5(image_file.read())
                    hashed_name = hash_object.hexdigest() + '.png'

                    # Normalizar el nombre del archivo para eliminar caracteres no ASCII
                    normalized_name = unicodedata.normalize('NFKD', hashed_name).encode('ASCII', 'ignore').decode('ASCII')

                    # Guardar la imagen en el directorio adecuado con el nombre normalizado
                    file_path = os.path.join('/djangoApp/BibliotecaMariCarmen/BibliotecaIETI/static/profile_photos', normalized_name)
                    with open(file_path, 'wb+') as destination:
                        for chunk in image_file.chunks():
                            destination.write(chunk)                    # Asignar el nombre de la imagen al usuario
                    user.image = f'profile_photos/{normalized_name}'
                '''

                if user.first_name != request.POST.get('first_name', user.first_name):
                    user.first_name = request.POST.get('first_name', user.first_name)
                if user.last_name != request.POST.get('last_name', user.last_name):
                    user.last_name = request.POST.get('last_name', user.last_name)
                if user.centro != request.POST.get('centro', user.centro):
                    user.centro = request.POST.get('centro', user.centro)
                if user.ciclo != request.POST.get('ciclo', user.ciclo):
                    user.ciclo = request.POST.get('ciclo', user.ciclo)
                if user.fecha_nacimiento != parser.parse(request.POST.get('fecha_nacimiento', user.fecha_nacimiento)):
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

#Editar Otros usuarios,
@login_required
def editUsuaris(request):
    user = request.user
    if not user.has_password_changed:
        messages.warning(request, 'La contrasenya predeterminada és insegura. Canvia-la ara mateix per poder accedir als continguts.')
        return render(request, 'myapp/dashboard/canviar_contrasenya.html')

    # actualizar datos del usuario
    if request.method == "POST":
        user_id = request.POST.get('id')
        if user_id:
            try:
                user = User.objects.get(pk=user_id)
                image_file = request.FILES.get('image')
                
                # DESARROLLO:
                if image_file:
                    # Generar un nombre único para la imagen utilizando un hash
                    hash_object = hashlib.md5(image_file.read())
                    hashed_name = hash_object.hexdigest() + '.png'

                    # Guardar la imagen en el directorio adecuado
                    file_path = os.path.join(settings.STATIC_ROOT)
                    with open(file_path, 'wb+') as destination:
                        for chunk in image_file.chunks():
                            destination.write(chunk)
                    
                    # Asignar el nombre de la imagen al usuario
                    user.image = request.FILES.get('image')


                ''' PRODUCCION:
                if image_file:
                    # Generar un nombre único para la imagen utilizando un hash
                    hash_object = hashlib.md5(image_file.read())
                    hashed_name = hash_object.hexdigest() + '.png'

                    # Normalizar el nombre del archivo para eliminar caracteres no ASCII
                    normalized_name = unicodedata.normalize('NFKD', hashed_name).encode('ASCII', 'ignore').decode('ASCII')

                    # Guardar la imagen en el directorio adecuado con el nombre normalizado
                    file_path = os.path.join('/djangoApp/BibliotecaMariCarmen/BibliotecaIETI/static/profile_photos', normalized_name)
                    with open(file_path, 'wb+') as destination:
                        for chunk in image_file.chunks():
                            destination.write(chunk)                    # Asignar el nombre de la imagen al usuario
                    user.image = f'profile_photos/{normalized_name}'
                '''
                 
                if user.first_name != request.POST.get('first_name', user.first_name):
                    user.first_name = request.POST.get('first_name', user.first_name)
                if user.last_name != request.POST.get('last_name', user.last_name):
                    user.last_name = request.POST.get('last_name', user.last_name)
                if user.centro != request.POST.get('centro', user.centro):
                    user.centro = request.POST.get('centro', user.centro)
                if user.ciclo != request.POST.get('ciclo', user.ciclo):
                    user.ciclo = request.POST.get('ciclo', user.ciclo)
                if user.telefono != request.POST.get('telefono', user.telefono):
                    user.telefono = request.POST.get('telefono', user.telefono)
                if user.fecha_nacimiento != parser.parse(request.POST.get('fecha_nacimiento', user.fecha_nacimiento)):
                    user.fecha_nacimiento = parser.parse(request.POST.get('fecha_nacimiento', user.fecha_nacimiento))

                user.save()
                messages.success(request, 'Datos actualizados correctamente')
                registrar_evento(f'Datos de "{user}" actualizados correctamente', 'INFO')
                return redirect('usuaris')
            except User.DoesNotExist:
                messages.error(request, 'El usuario no existe')
                registrar_evento(f'Intento de actualización de datos para un usuario inexistente', 'ERROR')
                return redirect('usuaris')
        else:
            messages.error(request, 'Falta el campo ID')
            registrar_evento('Intento de actualización de datos sin ID', 'ERROR')
            return redirect('usuaris')



    return render(request, 'myapp/dashboard/usuaris.html')

@login_required
def EditUsuarisView(request, user_id):
    # Obtener el usuario por su ID
    user = get_object_or_404(User, id=user_id)
    
    # Aquí podrías definir el formulario de edición de usuario
    # Por ejemplo, si estás utilizando forms.py:
    # from .forms import UserForm
    # form = UserForm(instance=user)

    # Obtener la fecha de nacimiento del usuario si está disponible
    fecha_nacimiento = None
    if user.fecha_nacimiento:
        fecha_nacimiento = user.fecha_nacimiento.strftime('%Y-%m-%d')
    
    # Luego, renderizas el template con el formulario y el usuario
    return render(request, 'myapp/dashboard/EditUsuaris.html', {'user': user, 'fecha_nacimiento': fecha_nacimiento})

@login_required
def dashboard(request):
    user = request.user
    if not user.has_password_changed:
        messages.warning(request, 'La contrasenya predeterminada és insegura. Canvia-la ara mateix per poder accedir als continguts.')
        return render(request, 'myapp/dashboard/canviar_contrasenya.html')
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
            if not user.has_password_changed:
                user.has_password_changed = True
                user.save()
                update_session_auth_hash(request, user)  # Actualiza la sesión para que el usuario no sea deslogueado
                messages.success(request, 'Contraseña cambiada correctamente')
                registrar_evento('Contrasenya canviada correctament', 'INFO')
                return redirect('dashboard')
            else:
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


@csrf_exempt
def cerca_cataleg(request):
    if request.method == 'GET':
        query = request.GET.get('cerca', '')
        only_available = request.GET.get('nomes_disponible', '')
        print("Valor de nomes_disponible:", only_available)
        
        if len(query) >= 3:
            if only_available:
                response = requests.get(f'http://127.0.0.1:8000/get_ItemCatalogo?search={query}&only_available=true')
            else:
                response = requests.get(f'http://127.0.0.1:8000/get_ItemCatalogo?search={query}')
            
            if response.status_code == 200:
                data = response.json().get('ItemCatalogo', [])
                for item in data:
                    centros = item.get('centros', [])
                    for centro in centros:
                        centro_id = centro.get('centro_id')
                        centro_name = Centro.objects.get(id=centro_id).nombre  # Obtiene el nombre del centro
                        centro['nombre_centro'] = centro_name  # Agrega el nombre del centro al diccionario
                                                
                
                    
                # Crear objeto Paginator
                paginator = Paginator(data, 25)  # 25 resultados por página por defecto
                
                # Obtener número de página a mostrar
                page_number = request.GET.get('page')
                
                # Obtener página de resultados
                page_obj = paginator.get_page(page_number)
                
                return render(request, 'myapp/cerca_cataleg.html', {'query': query, 'resultados': page_obj})
            else:
                error_message = 'Error al obtener resultados de la búsqueda'
                registrar_evento('Error al obtener resultados de la búsqueda', 'ERROR')
                return render(request, 'myapp/cerca_cataleg.html', {'query': query, 'error_message': error_message})
        else:
            error_message = 'La consulta debe tener al menos 3 caracteres'
            return render(request, 'myapp/cerca_cataleg.html', {'query': query, 'error_message': error_message})
    else:
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
        
        return JsonResponse({'mensaje': 'Log guardat correctament.'})
    else:
        return JsonResponse({'error': 'Mètode no permès.'}, status=405)

def process_csv(csv_file, centre_educatiu, request):
    user = request.user
    if not user.has_password_changed:
        messages.warning(request, 'La contrasenya predeterminada és insegura. Canvia-la ara mateix per poder accedir als continguts.')
        return render(request, 'myapp/dashboard/canviar_contrasenya.html')
    
    # Directorio donde se almacenarán los archivos CSV
    csv_directory = os.path.join(settings.MEDIA_ROOT, 'csv_files')
    
    # Asegurarse de que el directorio exista, si no, créalo
    if not os.path.exists(csv_directory):
        os.makedirs(csv_directory)
    
    # Nombre del archivo
    file_name = csv_file.name
    
    # Ruta relativa del archivo CSV
    file_path = os.path.join(csv_directory, file_name)
    
    # Guardar el archivo CSV en el sistema de archivos
    with open(file_path, 'wb+') as destination:
        for chunk in csv_file.chunks():
            destination.write(chunk)
    
    # Ahora abrir el archivo CSV desde la ubicación guardada
    with open(file_path, 'r', encoding='ISO-8859-1') as file:
        csv_reader = csv.reader(file, delimiter=',')
        # contraseña hash
        hashed_password = make_password("password")

        # Iterar sobre cada fila del archivo CSV
        for line_number, row in enumerate(csv_reader, start=1):
            try:
                # Supongamos que el archivo CSV tiene el formato: nombre, apellidos, email, fecha de nacimiento, ciclo, roles
                username, last_name, email, fecha_nacimiento, ciclo, centro, roles, telefono  = row
                # Crea un nuevo objeto User y asigna los valores
                user = User(
                    username=username,
                    password=hashed_password,  # Guarda la contraseña hasheada
                    first_name=username,
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
                messages.warning(request, f"Línea {line_number}: No s'ha importat correctament. Format incorrecte.")

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
                messages.success(request, "El fitxer CSV s'ha importat correctament.")
                return render(request, 'myapp/dashboard/importar.html', {'form': form})
            else:
                # Manejar el caso donde no se proporciona el archivo CSV
                messages.error(request, "No s'ha proporcionat cap fitxer CSV.")
                print(form.errors)  # Imprime los errores del formulario en la consola
    else:
        form = Importar()
        print("Paso por aqui 3") 
    return render(request, 'myapp/dashboard/importar.html', {'form': form})


@login_required
def usuaris(request):
    # Obtén todos los usuarios excluyendo el usuario anónimo y el superusuario
    centro_usuario_actual = request.user.centro
    users = User.objects.exclude(email='Anonimo@Anonimo.com').exclude(is_superuser=True).exclude(id=request.user.id).filter(centro=centro_usuario_actual,)
    
    # Renderiza el template con la lista de usuarios
    return render(request, 'myapp/dashboard/usuaris.html', {'users': users})

@login_required
def EditUsuaris(request, user_id):
    # Obtener el usuario por su ID
    user = get_object_or_404(User, id=user_id)
    
    # Aquí podrías definir el formulario de edición de usuario
    # Por ejemplo, si estás utilizando forms.py:
    # from .forms import UserForm
    # form = UserForm(instance=user)
    
    # Luego, renderizas el template con el formulario y el usuario
    return render(request, 'myapp/dashboard/EditUsuaris.html', {'user': user})

## Prestamos

@login_required
def prestamos(request):
    
    # Obtén todos los usuarios excluyendo el usuario anónimo y el superusuario
    prestamos = Prestamo.objects.all()

  
    if request.method == 'POST':        
        prestamo_id = request.POST.get('id')
        prestamo = Prestamo.objects.get(pk=prestamo_id)
        ejemplar = Ejemplar.objects.get(pk=prestamo.ejemplar.id)
        elemento = ejemplar.elemento
        elemento.cantidad_disponible += 1
        elemento.save()
        prestamo.delete()
        
        messages.success(request, 'Prestec eliminat correctament!')


    # Renderiza el template con la lista de usuarios
    return render(request, 'myapp/dashboard/prestecs.html', {'prestamos': prestamos})

@login_required
def nou_prestec(request):
    items_catalogo = ItemCatalogo.objects.all()
    users = User.objects.all()
    
    if request.method == 'POST':
        # añadir nuevo Ejemplar a la base de datos 
        ejemplar_objs = []
        elemento = None
        # espera de 0.5s para evitar errores de concurrencia
        time.sleep(0.5)
        if request.POST.get('article').startswith('CD'):
            elemento = CD.objects.get(id_catalogo=request.POST.get('article'))
        elif request.POST.get('article').startswith('DVD'):
            elemento = DVD.objects.get(id_catalogo=request.POST.get('article'))
        elif request.POST.get('article').startswith('BR'):
            elemento = BR.objects.get(id_catalogo=request.POST.get('article'))
        elif request.POST.get('article').startswith('DIS'):
            elemento = Dispositivo.objects.get(id_catalogo=request.POST.get('article'))
        elif request.POST.get('article').startswith('LB'):
            elemento = Libro.objects.get(id_catalogo=request.POST.get('article'))
        # asignar un nuevo codigo a cada ejemplar a partir del ultimo codigo (EJ001)
        codigo = Ejemplar.objects.all().order_by('-codigo').first().codigo
        codigo = f'EJ{int(codigo[2:])+1:03}'
        time.sleep(0.3)
        ejemplar_objs.append(Ejemplar(
            elemento=elemento,
            codigo=codigo,
            disponible=False
        ))
        Ejemplar.objects.bulk_create(ejemplar_objs)

        # restar 1 a la cantidad de ejemplares disponibles
        elemento.cantidad_disponible -= 1
        elemento.save()

        # añadir nuevo prestamo a la base de datos
        usuario = User.objects.get(pk=request.POST.get('usuari'))
        ejemplar = Ejemplar.objects.get(codigo=codigo)

        # convierto la fecha de prestamo a formato datetime
        fecha_fin = timezone.make_aware(datetime.strptime(request.POST.get('date_range'), "%d-%m-%Y %H:%M"))

        print(fecha_fin)
        Prestamo.objects.create(
            usuario=usuario,
            ejemplar=ejemplar,
            fecha_devolucion=fecha_fin,
        )
        messages.success(request, 'Prestec creat correctament!')


    return render(request, 'myapp/dashboard/nou_prestec.html', {'items_catalogo': items_catalogo, 'users': users})
    
# CREAR USUARIO PANEL
def crear_usuari(request):
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        
        try:
            # Contraseña hash
            hashed_password = make_password("P@ssw0rd")

            if form.is_valid():
                username = request.POST.get('username')
                #email = request.POST.get('email')

                if User.objects.filter(username=username).exists():
                    messages.error(request, 'El nom de usuario ja está en us.')
                    return render(request, 'myapp/dashboard/crear_usuari.html', {'form': form})
                
                user = form.save(commit=False)
                user.has_password_changed = False
                user.first_name = request.POST.get('first_name')
                user.last_name = request.POST.get('last_name')
                user.username = request.POST.get('email')
                user.password = hashed_password
                user.save()
                messages.success(request, 'Usuario creat amb éxit.')
                return render(request, 'myapp/dashboard/crear_usuari.html', {'form': form})
            else:
                # Capturar errores de validación específicos del campo email
                email_errors = form.errors.get('email')
                username_errors = form.errors.get('username')

                if email_errors:
                    messages.error(request, email_errors)
                elif username_errors:
                    messages.error(request, username_errors)
                else:
                    messages.error(request, 'Error de validació en el formulari')
                
                return render(request, 'myapp/dashboard/crear_usuari.html', {'form': form})

        except Exception as e:
            print("Error:", str(e))
            messages.error(request, 'El nom de usuari ya existeix.')
            return render(request, 'myapp/dashboard/crear_usuari.html', {'form': form})

    else:
        form = UserForm()
   
    return render(request, 'myapp/dashboard/crear_usuari.html', {'form': form})
                  