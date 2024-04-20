from django.contrib.auth.models import AbstractUser
from django.db import models


# Modelo base para los elementos del item_catálogo
class ItemCatalogo(models.Model):
    id_catalogo = models.CharField(max_length=200, unique=True)
    titulo = models.CharField(max_length=200)
    ocio = models.TextField()
    autor = models.CharField(max_length=200)
    data_edicion = models.DateField()

# Modelo para los libros
class Libro(ItemCatalogo):
    CDU = models.CharField(max_length=100)
    ISBN = models.CharField(max_length=30)
    editorial = models.CharField(max_length=100)
    coleccion = models.CharField(max_length=100, null=True)
    paginas = models.IntegerField(default=0)  # Establecer un valor predeterminado


# Modelo para los CD
class CD(ItemCatalogo):
    discografica = models.CharField(max_length=100)
    estilo = models.CharField(max_length=100)
    duracion = models.TimeField()

# Modelo para los DVD
class DVD(ItemCatalogo):
    director = models.CharField(max_length=100)
    duracion = models.DurationField()
    subtitulos = models.BooleanField(default=True)
    idiomas_audio = models.CharField(max_length=100)
    formato_video = models.CharField(max_length=50)

# Modelo para los Blu-ray
class BR(ItemCatalogo):
    estudio = models.CharField(max_length=100)
    formato_video = models.CharField(max_length=50)
    extras = models.TextField()

# Modelo para los dispositivos
class Dispositivo(ItemCatalogo):
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    tipo_conexion = models.CharField(max_length=100)
    sistema_operativo = models.CharField(max_length=100)
    almacenamiento = models.CharField(max_length=100)

# Modelo para los ejemplares
class Ejemplar(models.Model):
    elemento = models.ForeignKey(ItemCatalogo, on_delete=models.CASCADE)
    codigo = models.CharField(max_length=200)
    disponible = models.BooleanField(default=True)

class User(AbstractUser):
    fecha_nacimiento = models.DateField(null=True)
    centro = models.CharField(max_length=100)
    ciclo = models.CharField(max_length=100)
    roles = models.CharField(max_length=100)
    image = models.ImageField(upload_to='profile_photos', default='default.jpg')

    # Definir accesos inversos personalizados para evitar conflictos
    groups = models.ManyToManyField('auth.Group', related_name="biblioteca_user_groups", blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name="biblioteca_user_permissions", blank=True)

class Reserva(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    ejemplar = models.ForeignKey(Ejemplar, on_delete=models.CASCADE)
    fecha_reserva = models.DateTimeField(auto_now_add=True)

class Prestamo(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    ejemplar = models.ForeignKey(Ejemplar, on_delete=models.CASCADE)
    fecha_prestamo = models.DateTimeField(auto_now_add=True)
    fecha_devolucion = models.DateTimeField(null=True, blank=True)

class Peticion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    elemento = models.ForeignKey(ItemCatalogo, on_delete=models.CASCADE)
    fecha_peticion = models.DateTimeField(auto_now_add=True)

class Log(models.Model):
    evento = models.CharField(max_length=200)
    nivel = models.CharField(max_length=20)  
    fecha_registro = models.DateTimeField(auto_now_add=True)
