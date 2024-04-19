import random
from faker import Faker
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from BibliotecaApp.models import Libro, Ejemplar, User, Reserva, Prestamo, Peticion, ItemCatalogo

# Crear una instancia de Faker
fake = Faker()

class Command(BaseCommand):
    help = 'Genera datos ficticios para la biblioteca'

    # Crear instancias de libros ficticios
    def crear_libros(self, numero_libros):
        for _ in range(numero_libros):
            isbn = fake.isbn13()[:13]  # Truncar el ISBN si es demasiado largo
            libro = Libro.objects.create(
                id_catalogo=fake.uuid4(),  # Generar un ID único para el catálogo
                titulo=fake.catch_phrase(),
                ocio=fake.paragraph(),
                autor=fake.name(),
                data_edicion=fake.date_between(start_date='-50y', end_date='today'),
                CDU=fake.isbn13(),  # Generar un CDU aleatorio
                ISBN=isbn,
                editorial=fake.company(),
                coleccion=fake.word(),
                paginas=random.randint(50, 500)
            )
            # Crear ejemplares para cada libro
            self.crear_ejemplares(libro, random.randint(1, 5))

    # Crear instancias de ejemplares ficticios para cada libro
    def crear_ejemplares(self, libro, cantidad):
        for _ in range(cantidad):
            Ejemplar.objects.create(
                elemento=libro,
                codigo=fake.uuid4(),  # Generar un código único para el ejemplar
                disponible=random.choice([True, False])
            )

    # Crear instancias de usuarios ficticios
    def crear_usuarios(self, numero_usuarios):
        for _ in range(numero_usuarios):
            usuario = User.objects.create_user(
                username=fake.user_name(),
                password=fake.password(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.email(),
                fecha_nacimiento=fake.date_of_birth(minimum_age=18, maximum_age=90),
                centro=fake.company(),
                ciclo=fake.job(),
                roles=fake.random_element(elements=('Estudiante', 'Profesor', 'Personal administrativo')),
                is_active=True
            )
            # Asignar usuarios a grupos aleatorios
            self.asignar_grupo_usuario(usuario)

    # Asignar usuarios a grupos aleatorios
    def asignar_grupo_usuario(self, usuario):
        grupos = Group.objects.all()
        usuario.groups.add(random.choice(grupos))

    # Generar reservas ficticias
    def generar_reservas(self, numero_reservas):
        ejemplares = Ejemplar.objects.filter(disponible=True)
        usuarios = User.objects.all()
        for _ in range(numero_reservas):
            reserva = Reserva.objects.create(
                usuario=random.choice(usuarios),
                ejemplar=random.choice(ejemplares)
            )
            # Marcar el ejemplar como no disponible después de reservar
            reserva.ejemplar.disponible = False
            reserva.ejemplar.save()

    # Generar préstamos ficticios
    def generar_prestamos(self, numero_prestamos):
        ejemplares = Ejemplar.objects.filter(disponible=True)
        usuarios = User.objects.all()
        for _ in range(numero_prestamos):
            prestamo = Prestamo.objects.create(
                usuario=random.choice(usuarios),
                ejemplar=random.choice(ejemplares)
            )
            # Marcar el ejemplar como no disponible después del préstamo
            prestamo.ejemplar.disponible = False
            prestamo.ejemplar.save()

    # Generar peticiones ficticias
    def generar_peticiones(self, numero_peticiones):
        elementos = ItemCatalogo.objects.all()
        usuarios = User.objects.all()
        for _ in range(numero_peticiones):
            Peticion.objects.create(
                usuario=random.choice(usuarios),
                elemento=random.choice(elementos)
            )

    def handle(self, *args, **kwargs):
        self.crear_libros(50)
        self.crear_usuarios(20)
        self.generar_reservas(30)
        self.generar_prestamos(20)
        self.generar_peticiones(10)
