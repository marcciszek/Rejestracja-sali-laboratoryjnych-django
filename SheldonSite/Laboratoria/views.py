from django.shortcuts import render, get_object_or_404
from .models import Room, RegistrationEntry
from django.contrib.auth.decorators import login_required

from django.http import JsonResponse



@login_required
def room_list(request):
    rooms = Room.available.all()
    return render(request,
                  'laboratoria/room/list.html',
                  {'rooms': rooms})


@login_required
def room_detail(request, room):
    room = get_object_or_404(Room, slug=room)
    return render(request,
                  'laboratoria/room/detail.html',
                  {'room': room})


@login_required
def days_in_month(request, year, month):
    if month > 12:
        month = 12
    if month < 0:
        month = 0
    if year < 2010:
        year = 2010
    days = RegistrationEntry.objects_custom.month_filter(year, month)
    return render(request,
                  'laboratoria/reservation/month.html',
                  {'year': year,
                   'month': month,
                   'days': days})


@login_required
def days_in_year(request, year):
    if year < 2010:
        year = 2010
    days = RegistrationEntry.objects_custom.year_filter(year)
    return render(request,
                  'laboratoria/reservation/year.html',
                  {'year': year,
                   'days': days})


@login_required
def day_detail(request, day):
    day = get_object_or_404(RegistrationEntry, registerDate=day)
    return render(request,
                  'laboratoria/reservation/day.html',
                  {'day': day})


import logging, logging.config
import sys

LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
        }
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO'
    }
}

from django.http import HttpResponse

def test(request):
    if request.method == "POST":
        logging.config.dictConfig(LOGGING)
        logging.info('Ktoś chce moje dane!')
        logging.info(request.body.decode('utf-8'))
        response = JsonResponse({'foo': 'bar'})
        return response
    if request.method == "GET":
        response = HttpResponse("{'foo':'bar'}", content_type="text/plain")
        response.headers['Age'] = 120
        return render(request,
                      'laboratoria/room/stanowisko_export.html',
                      {'rooms': 'aa'})
