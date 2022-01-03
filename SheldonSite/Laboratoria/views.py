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
    # room = get_object_or_404(Room, slug=room)
    # registers = RegistrationEntry.objects_custom.all_entries(room)
    # return render(request,
    #               'laboratoria/room/detail.html',
    #               {'room': room})
    if request.method == "GET":
        room = get_object_or_404(Room, slug=room)
        registers = RegistrationEntry.objects_custom.all_entries(room)
        data = serialize("json", registers)
        return JsonResponse({'data': data})
        # return render(request,
        #               'laboratoria/room/detail.html',
        #               {'data': data})


@login_required
def day_detail(request, day):
    day = get_object_or_404(RegistrationEntry, registerDate=day)
    return render(request,
                  'laboratoria/reservation/day.html',
                  {'day': day})
