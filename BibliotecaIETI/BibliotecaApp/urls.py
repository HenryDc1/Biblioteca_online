from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('logout', views.logout_user, name='logout'),
    path('canviar_contrasenya', views.canviar_contrasenya, name='canviar_contrasenya'),
    path('cerca_cataleg/', views.cerca_cataleg, name='cerca_cataleg'),

]