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

    path('dashboard', views.dashboard, name='dashboard'),
    path('dashboard/usuari', views.usuari, name='usuari'),   
    path('dashboard/usuaris/EditUsuaris', views.editUsuaris, name='editUsuaris'),

    # Reset password 
    path('recuperar_contrasenya/', auth_views.PasswordResetView.as_view(), name='recuperar_contrasenya'),
    path('recuperar_contrasenya/ok/',auth_views.PasswordResetDoneView.as_view(template_name='myapp/registration/password_reset_done.html'),name='password_reset_done'),
    path('reestablir_contrasenya/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reestablir_contrasenya/done/', auth_views.PasswordResetCompleteView.as_view(template_name='myapp/registration/password_reset_complete.html'), name='password_reset_complete'),
    
    path('cerca_cataleg/', views.cerca_cataleg, name='cerca_cataleg'),
    path('create_log/', api.create_log, name='create_log'),

    path('guardar-log', views.guardar_log, name='guardar_log'),

    path('crear_usuari/', views.crear_usuari, name='crear_usuari'),

    
    path('dashboard/upload_file', views.upload_file, name='upload_file'),

    path('dashboard/prestecs', views.prestamos, name='prestamos'),

    path('dashboard/usuaris/', views.usuaris, name='usuaris'),

    path('dashboard/usuaris/EditUsuaris/<str:user_id>/', views.EditUsuaris, name='EditUsuaris'),


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
