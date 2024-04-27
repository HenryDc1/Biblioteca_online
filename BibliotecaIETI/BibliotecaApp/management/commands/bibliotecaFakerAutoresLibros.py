from django.core.management.base import BaseCommand
import random
from faker import Faker
from datetime import datetime
from BibliotecaApp.models import Libro

fake_author = Faker(['es_ES']) 
fake_title = Faker('es_ES')


word_categories = {
    "adjetivos": ["El", "La", "Los", "Las", "Un", "Una", "Unos", "Unas", "Este", "Esta", "Estos", "Estas"],
    "sustantivos": ["señor", "señora", "anillos", "aventura", "misterio", "fantasía", "romance", "historia", 
                    "ciencia", "ficción", "intriga", "suspenso", "viaje", "descubrimiento", "amor", "poder", 
                    "destino", "guerra", "tesoro", "espada", "rey", "reina", "príncipe", "princesa", "héroe", 
                    "heroína", "mundo", "universo", "ciudad", "paisaje", "sueño", "pesadilla"],
    "verbos": ["en busca de", "en el reino de", "la búsqueda de", "la conquista de", "la venganza de", 
                "el regreso de", "el secreto de", "el destino de", "la leyenda de", "el poder de"],
    "adverbios": ["oscuro", "legendario", "mágico", "olvidado", "perdido", "eterno", "prohibido", "inmortal",
                    "desconocido", "oculto", "fatal", "infinito", "solitario", "temible", "legendario"]
}

class Command(BaseCommand):
    help = 'Generate libros with random data'

    def add_arguments(self, parser):
        parser.add_argument('num_authors', type=int, help='Indicate the number of authors')
        parser.add_argument('books_per_author', type=int, help='Indicate the number of books per author')

    def handle(self, *args, **kwargs):
        num_authors = kwargs['num_authors']
        books_per_author = kwargs['books_per_author']
        self.stdout.write(self.style.SUCCESS(f'Generating libros for {num_authors} authors...'))
        self.generate_books(num_authors, books_per_author)
        self.stdout.write(self.style.SUCCESS(f'Successfully generated libros for {num_authors} authors'))

    def generate_books(self, num_authors, books_per_author):
        for i in range(num_authors):
            author_name = fake_author.name()
            self.stdout.write(f'Generating libros for author: {author_name}')
            for j in range(books_per_author):
                id_catalogo = f"LB{i*books_per_author + j + 100}"
                # Genera el título del libro utilizando palabras de las categorías del diccionario
                titulo_parts = [
                    random.choice(word_categories["adjetivos"]), 
                    random.choice(word_categories["sustantivos"]), 
                    random.choice(word_categories["verbos"]), 
                    random.choice(word_categories["adverbios"])
                ]
                titulo = ' '.join(titulo_parts)
                ocio = "Novel·la"
                autor = author_name
                data_edicion = fake_author.date_between(start_date='-50y', end_date='today')
                cantidad = random.randint(1, 10)  # Cantidad total de libros
                cantidad_disponible = cantidad  # Se asume que todos están disponibles al principio
                CDU = fake_author.random_int(min=800, max=899) + random.choice([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9])
                ISBN = fake_author.isbn13(separator="-")
                editorial = fake_author.company()
                coleccion = "Biblioteca Breu"
                paginas = fake_author.random_int(min=100, max=500)
                
                libro = Libro.objects.create(
                    id_catalogo=id_catalogo,
                    titulo=titulo,
                    ocio=ocio,
                    autor=autor,
                    data_edicion=data_edicion,
                    cantidad=cantidad,
                    cantidad_disponible=cantidad_disponible,
                    CDU=CDU,
                    ISBN=ISBN,
                    editorial=editorial,
                    coleccion=coleccion,
                    paginas=paginas
                )
                libro.save()
