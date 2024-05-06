from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from . import api
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('logout', views.logout_user, name='logout'),
    path('canviar_contrasenya', views.canviar_contrasenya, name='canviar_contrasenya'),

    path('panell', views.dashboard, name='dashboard'),
    path('panell/perfil', views.usuari, name='usuari'),   
    path('panell/usuaris/editar_usuari', views.editUsuaris, name='editUsuaris'),

    # Reset password 
    path('recuperar_contrasenya/', auth_views.PasswordResetView.as_view(), name='recuperar_contrasenya'),
    path('recuperar_contrasenya/ok/',auth_views.PasswordResetDoneView.as_view(template_name='myapp/registration/password_reset_done.html'),name='password_reset_done'),
    path('reestablir_contrasenya/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reestablir_contrasenya/done/', auth_views.PasswordResetCompleteView.as_view(template_name='myapp/registration/password_reset_complete.html'), name='password_reset_complete'),
    
    path('cerca_cataleg/', views.cerca_cataleg, name='cerca_cataleg'),
    path('create_log/', api.create_log, name='create_log'),

    path('guardar-log', views.guardar_log, name='guardar_log'),

    path('panell/importar_arxiu', views.upload_file, name='upload_file'),

    path('panell/prestecs', views.prestamos, name='prestamos'),
    path('panell/prestecs/crear', views.nou_prestec, name='nou_prestec'),

    path('panell/usuaris/', views.usuaris, name='usuaris'),

    path('panell/usuaris/editar_usuari/<str:user_id>/', views.EditUsuarisView, name='EditUsuarisView'),

    path('panell/crear_usuari/', views.crear_usuari, name='crear_usuari'),

    path('dashboard/nou_element/', views.nou_element, name='nou_element'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
