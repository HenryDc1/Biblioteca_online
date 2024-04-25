from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import UserManager



# Modelo base para los elementos del item_catálogo
class ItemCatalogo(models.Model):
    id_catalogo = models.CharField(max_length=200, unique=True)
    titulo = models.CharField(max_length=200)
    ocio = models.TextField()
    autor = models.CharField(max_length=200)
    data_edicion = models.DateField()
    cantidad = models.IntegerField(default=0)  # Campo para la cantidad total
    cantidad_disponible = models.IntegerField(default=0)  # Campo para la cantidad disponible
    
    def __str__(self):
        return str(self.titulo)


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

class Ejemplar(models.Model):
    elemento = models.ForeignKey(ItemCatalogo, on_delete=models.CASCADE)
    codigo = models.CharField(max_length=200)
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.elemento.id_catalogo} - {self.elemento.titulo}"


class User(AbstractUser):
    fecha_nacimiento = models.DateField(null=True)
    centro = models.CharField(max_length=100)
    ciclo = models.CharField(max_length=100)
    roles = models.CharField(max_length=100)
    image = models.ImageField(upload_to='profile_photos', default='default.jpg')
    has_password_changed = models.BooleanField(default=False)  # Nuevo campo para rastrear el cambio de contraseña

    # Definir accesos inversos personalizados para evitar conflictos
    groups = models.ManyToManyField('auth.Group', related_name="biblioteca_user_groups", blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name="biblioteca_user_permissions", blank=True)
    
    email = models.EmailField(("email"), unique=True, db_index=True)    
    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = []

    objects = UserManager()  

class Reserva(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    ejemplar = models.ForeignKey(Ejemplar, on_delete=models.CASCADE)
    fecha_reserva = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.usuario)

class Prestamo(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    ejemplar = models.ForeignKey(Ejemplar, on_delete=models.CASCADE)
    fecha_prestamo = models.DateTimeField(auto_now_add=True)
    fecha_devolucion = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return str(self.usuario)

class Peticion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    elemento = models.ForeignKey(ItemCatalogo, on_delete=models.CASCADE)
    fecha_peticion = models.DateTimeField(auto_now_add=True)
    def __str__(self):
            return str(self.usuario)

    
class Log(models.Model):
    LEVEL_CHOICES = [
        ('INFO', 'INFO'),
        ('WARNING', 'WARNING'),
        ('ERROR', 'ERROR'),
        ('FATAL', 'FATAL'),
    ]

    evento = models.CharField(max_length=200)
    nivel = models.CharField(max_length=20, choices=LEVEL_CHOICES)  
    fecha_registro = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.nivel} ---- {self.evento} ---- {self.usuario}"
