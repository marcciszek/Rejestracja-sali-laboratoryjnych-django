from django.urls import path, register_converter
from . import views, converters

app_name = 'laboratoria'

register_converter(converters.FourDigitYearConverter, 'yyyy')
register_converter(converters.TwoDigitMonthConverter, 'mm')

urlpatterns = [
    path('', views.room_list,
         name='room_list'),
    path('<slug:room>',
         views.room_detail,
         name='room_detail'),
    path('api/order_submit',
         views.order_submit,
         name='order_submit_api'),
    path('api/<slug:room>',
         views.room_detail_api,
         name='room_detail_api'),
    path('reservation/<slug:day>',
         views.day_detail,
         name='day_detail'),
    path('pendings/all',
         views.unprocessed_pendings,
         name='pendings'),
]
