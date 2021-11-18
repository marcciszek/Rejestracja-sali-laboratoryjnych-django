from django.shortcuts import render, get_object_or_404
from .models import Room


def room_list(request):
    rooms = Room.available.all()
    return render(request,
                  'laboratoria/room/list.html',
                  {'rooms': rooms})


def room_detail(request, room):
    room = get_object_or_404(Room, slug=room)
    return render(request,
                  'laboratoria/room/detail.html',
                  {'room': room})
