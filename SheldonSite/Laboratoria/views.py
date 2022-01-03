from django.shortcuts import render, get_object_or_404
from .models import Room, RegistrationEntry
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse, JsonResponse
from django.core.serializers import serialize
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import requires_csrf_token


@login_required
def room_list(request):
    rooms = Room.available.all()
    return render(request,
                  'laboratoria/room/list.html',
                  {'rooms': rooms})


@requires_csrf_token
@ensure_csrf_cookie
@login_required
def room_detail(request, room):
    room = get_object_or_404(Room, slug=room)
    return render(request,
                  'laboratoria/room/detail.html',
                  {'room': room})

    # if request.method == "GET":
    #     room = get_object_or_404(Room, slug=room)
    #     registers = RegistrationEntry.objects_custom.all_entries(room)
    #     data = serialize("json", registers)
    #     return JsonResponse({'data': data})
    #     return render(request,
    #                   'laboratoria/room/detail.html',
    #                   {'data': data})


@login_required
def room_detail_api(request, room):
    if request.method == "GET":
        room = get_object_or_404(Room, slug=room)
        registers = RegistrationEntry.objects_custom.all_entries(room)
        data = serialize("json", registers)
        return JsonResponse({'data': data})


@login_required
def day_detail(request, day):
    day = get_object_or_404(RegistrationEntry, registerDate=day)
    return render(request,
                  'laboratoria/reservation/day.html',
                  {'day': day})

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


@ensure_csrf_cookie
@requires_csrf_token
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
