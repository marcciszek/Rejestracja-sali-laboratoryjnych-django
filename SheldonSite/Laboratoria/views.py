from django.shortcuts import render, get_object_or_404
from .models import Room, RegistrationEntry
from django.contrib.auth.decorators import login_required


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
