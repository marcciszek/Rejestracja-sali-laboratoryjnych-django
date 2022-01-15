"""SheldonSite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.shortcuts import redirect
from . import main_views

urlpatterns = [
    path('', main_views.homepage, name='homepage'),
    path('info',main_views.infopage,name='infopage'),
    path('contact',main_views.contact,name='contact'),
    path('admin/', admin.site.urls),
    path('laboratoria/', include('Laboratoria.urls', namespace='laboratoria')),
    path('account/', include('account.urls', namespace='account')),
    # path('', lambda request: redirect('laboratoria/', permanent=True)),
]
