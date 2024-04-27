import json
from datetime import datetime
from django.core.management.base import BaseCommand
from BibliotecaApp.models import Libro, CD, DVD, BR, Dispositivo, Ejemplar, User, Reserva, Prestamo
from datetime import timedelta
from django.contrib.auth.hashers import make_password


class Command(BaseCommand):
    help = 'Inserta datos ficticios en la base de datos'

    def handle(self, *args, **kwargs):
        # self.eliminar_datos_antiguos()
        with open(r'D:\Usuarios\M E H D I\Desktop\Proyecto-Biblioteca\BibliotecaMariCarmen\BibliotecaIETI\BibliotecaApp\management\commands\datosfake.json', 'r',encoding='utf-8') as f:
            data = json.load(f)
            self.insertar_datos_ficticios(data)
        self.stdout.write(self.style.SUCCESS("¡Datos insertados exitosamente!"))

    # def eliminar_datos_antiguos(self):
    #     models_to_clear = [Libro, CD, DVD, BR, Dispositivo, Ejemplar, User, Reserva, Prestamo]
    #     for model in models_to_clear:
    #         model.objects.all().delete()

    def insertar_datos_ficticios(self, data):
        self.insertar_usuarios(data['Usuarios'])  # Primero inserta los usuarios
        self.insertar_libros(data['Libros'])
        self.insertar_cds(data['CDs'])
        self.insertar_dvds(data['DVDs'])
        self.insertar_blurays(data['Blu-rays'])
        self.insertar_dispositivos(data['Dispositivos'])
        self.insertar_ejemplares(data['Ejemplares'])
        self.insertar_reservas(data['Reservas'])
        self.insertar_prestamos(data['Prestamos'])


    def insertar_libros(self, libros):
        for libro_data in libros:
            Libro.objects.create(
                id_catalogo=libro_data['id_catalogo'],
                titulo=libro_data['titulo'],
                ocio=libro_data['ocio'],
                autor=libro_data['autor'],
                data_edicion=datetime.strptime(libro_data['data_edicion'], "%Y-%m-%d").date(),
                CDU=libro_data['CDU'],
                ISBN=libro_data['ISBN'],
                editorial=libro_data['editorial'],
                coleccion=libro_data['coleccion'],
                paginas=libro_data['paginas'],
                cantidad=libro_data.get('cantidad', 0),
                cantidad_disponible=libro_data.get('cantidad_disponible', 0)
            )

    def insertar_cds(self, cds):
        for cd_data in cds:
            CD.objects.create(
                id_catalogo=cd_data['id_catalogo'],
                titulo=cd_data['titulo'],
                ocio=cd_data['ocio'],
                autor=cd_data['autor'],
                data_edicion=datetime.strptime(cd_data['data_edicion'], "%Y-%m-%d").date(),
                discografica=cd_data['discografica'],
                estilo=cd_data['estilo'],
                duracion=cd_data['duracion'],
                cantidad=cd_data.get('cantidad', 0),
                cantidad_disponible=cd_data.get('cantidad_disponible', 0)
            )

    def insertar_dvds(self, dvds):
        for dvd_data in dvds:
            try:
                duracion = timedelta(hours=int(dvd_data['duracion_hours']), minutes=int(dvd_data['duracion_minutes']), seconds=int(dvd_data['duracion_seconds']))
            except KeyError:
                # Manejar el caso donde no se encuentran las claves de duración
                duracion = timedelta(hours=0, minutes=0, seconds=0)
            DVD.objects.create(
                id_catalogo=dvd_data['id_catalogo'],
                titulo=dvd_data['titulo'],
                ocio=dvd_data['ocio'],
                autor=dvd_data['autor'],
                data_edicion=datetime.strptime(dvd_data['data_edicion'], "%Y-%m-%d").date(),
                director=dvd_data['director'],
                duracion=duracion,
                subtitulos=dvd_data['subtitulos'],
                idiomas_audio=dvd_data['idiomas_audio'],
                formato_video=dvd_data['formato_video'],
                cantidad=dvd_data.get('cantidad', 0),
                cantidad_disponible=dvd_data.get('cantidad_disponible', 0)
            )

    def insertar_blurays(self, blurays):
        for br_data in blurays:
            duracion = timedelta(hours=int(br_data['duracion_hours']), minutes=int(br_data['duracion_minutes']), seconds=int(br_data['duracion_seconds']))
            BR.objects.create(
                id_catalogo=br_data['id_catalogo'],
                titulo=br_data['titulo'],
                ocio=br_data['ocio'],
                autor=br_data['autor'],
                data_edicion=datetime.strptime(br_data['data_edicion'], "%Y-%m-%d").date(),
                estudio=br_data['estudio'],
                formato_video=br_data['formato_video'],
                extras=br_data['extras'],
                cantidad=br_data.get('cantidad', 0),
                cantidad_disponible=br_data.get('cantidad_disponible', 0)
            )

    def insertar_dispositivos(self, dispositivos):
        for dispositivo_data in dispositivos:
            Dispositivo.objects.create(
                id_catalogo=dispositivo_data['id_catalogo'],
                titulo=dispositivo_data['titulo'],
                ocio=dispositivo_data['ocio'],
                autor=dispositivo_data['autor'],
                data_edicion=datetime.strptime(dispositivo_data['data_edicion'], "%Y-%m-%d").date(),
                marca=dispositivo_data['marca'],
                modelo=dispositivo_data['modelo'],
                tipo_conexion=dispositivo_data['tipo_conexion'],
                sistema_operativo=dispositivo_data['sistema_operativo'],
                almacenamiento=dispositivo_data['almacenamiento'],
                cantidad=dispositivo_data.get('cantidad', 0),
                cantidad_disponible=dispositivo_data.get('cantidad_disponible', 0)
            )

    def insertar_ejemplares(self, ejemplares):
        ejemplar_objs = []
        for ejemplar_data in ejemplares:
            elemento = None
            if ejemplar_data['elemento'].startswith('LB'):
                elemento = Libro.objects.get(id_catalogo=ejemplar_data['elemento'])
            elif ejemplar_data['elemento'].startswith('CD'):
                elemento = CD.objects.get(id_catalogo=ejemplar_data['elemento'])
            elif ejemplar_data['elemento'].startswith('DVD'):
                elemento = DVD.objects.get(id_catalogo=ejemplar_data['elemento'])
            elif ejemplar_data['elemento'].startswith('BR'):
                elemento = BR.objects.get(id_catalogo=ejemplar_data['elemento'])
            elif ejemplar_data['elemento'].startswith('DIS'):
                elemento = Dispositivo.objects.get(id_catalogo=ejemplar_data['elemento'])
            ejemplar_objs.append(Ejemplar(
                elemento=elemento,
                codigo=ejemplar_data['codigo'],
                disponible=ejemplar_data['disponible']
            ))
        Ejemplar.objects.bulk_create(ejemplar_objs)

    def insertar_usuarios(self, usuarios):
        for usuario_data in usuarios:
            # Utiliza make_password para crear la contraseña en el formato correcto
            hashed_password = make_password(usuario_data['password'])
            
            User.objects.create(
                username=usuario_data['username'],
                password=hashed_password,  # Guarda la contraseña hasheada
                first_name=usuario_data['first_name'],
                last_name=usuario_data['last_name'],
                email=usuario_data['email'],
                fecha_nacimiento=datetime.strptime(usuario_data['fecha_nacimiento'], "%Y-%m-%d").date(),
                centro=usuario_data['centro'],
                ciclo=usuario_data['ciclo'],
                roles=usuario_data['roles'],
                telefono=usuario_data.get('telefono')  # Obtener el teléfono del diccionario o None si no está presente
            )

    def insertar_reservas(self, reservas):
        for reserva_data in reservas:
            usuario = User.objects.get(pk=reserva_data['usuario'])
            ejemplar = Ejemplar.objects.get(codigo=reserva_data['ejemplar'])
            Reserva.objects.create(
                usuario=usuario,
                ejemplar=ejemplar,
                fecha_reserva=datetime.strptime(reserva_data['fecha_reserva'], "%Y-%m-%dT%H:%M:%S")
            )
            ejemplar.disponible = False
            ejemplar.save()

    def insertar_prestamos(self, prestamos):
        for prestamo_data in prestamos:
            usuario = User.objects.get(pk=prestamo_data['usuario'])
            ejemplar = Ejemplar.objects.get(codigo=prestamo_data['ejemplar'])
            fecha_devolucion = None
            if prestamo_data['fecha_devolucion']:
                fecha_devolucion = datetime.strptime(prestamo_data['fecha_devolucion'], "%Y-%m-%dT%H:%M:%S")
            Prestamo.objects.create(
                usuario=usuario,
                ejemplar=ejemplar,
                fecha_prestamo=datetime.strptime(prestamo_data['fecha_prestamo'], "%Y-%m-%dT%H:%M:%S"),
                fecha_devolucion=fecha_devolucion
            )
            ejemplar.disponible = False
            ejemplar.save()
