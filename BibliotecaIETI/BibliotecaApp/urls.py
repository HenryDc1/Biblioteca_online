from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('logout', views.logout_user, name='logout'),
    path('canviar_contrasenya', views.canviar_contrasenya, name='canviar_contrasenya'),

    # Reset password
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='myapp/registration/password_reset_form.html'), name='recuperar_contrasenya'),
    path('recuperar_contrasenya/ok/',auth_views.PasswordResetDoneView.as_view(),name='recuperar_contrasenya_ok'),
    path('reestablir_contrasenya/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='reestablir_contrasenya'),
    path('reestablir_contrasenya/done/',auth_views.PasswordResetCompleteView.as_view(),name='reestablir_contrasenya_ok'),
]