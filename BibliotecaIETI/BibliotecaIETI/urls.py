"""
URL configuration for BibliotecaIETI project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
import BibliotecaApp
from BibliotecaApp import api, views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('BibliotecaApp/', include('django.contrib.auth.urls')),
    path('BibliotecaApp/', include('BibliotecaApp.urls')),
    path('', BibliotecaApp.views.index),
    path('get_ItemCatalogo', api.get_ItemCatalogo, name='get_ItemCatalogo'),

    path('guardar-log/', views.guardar_log, name='guardar_log'),

    path('accounts/', include('allauth.urls')),


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
