from django.urls import path
from . import views

urlpatterns = [
    path('management/', views.management_page)  # our-domain.com/management
]
