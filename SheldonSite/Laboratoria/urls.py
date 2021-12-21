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
    path('reservation/<slug:day>',
         views.day_detail,
         name='day_detail'),
    path('reservation/<yyyy:year>/all',
         views.days_in_year,
         name='days_in_year'),
    path('reservation/<yyyy:year>/<mm:month>',
         views.days_in_month,
         name='days_in_month'),
]
