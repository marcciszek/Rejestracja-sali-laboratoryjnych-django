from django.urls import path
from . import views

app_name = 'laboratoria'

urlpatterns = [
    path('', views.room_list,
         name='room_list'),
    path('<slug:room>',
         views.room_detail,
         name='room_detail')
]
