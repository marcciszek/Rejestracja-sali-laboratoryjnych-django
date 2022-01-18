import json, logging, logging.config, sys
from datetime import datetime, date
from .models import Room, RegistrationEntry
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.core.serializers import serialize
from django.views.decorators.csrf import requires_csrf_token, csrf_exempt, ensure_csrf_cookie


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


@login_required
def room_detail_api(request, room):
    if request.method == "GET":
        room = get_object_or_404(Room, slug=room)
        registers = RegistrationEntry.objects_custom.all_entries(room)
        data = serialize("json", registers, use_natural_foreign_keys=True)
        return JsonResponse(data, safe=False)


@login_required
def day_detail(request, day):
    day = get_object_or_404(RegistrationEntry, registerDate=day)
    return render(request,
                  'laboratoria/reservation/day.html',
                  {'day': day})


@ensure_csrf_cookie
@requires_csrf_token
def order_submit(request):
    if request.method == "POST":
        logging.config.dictConfig(LOGGING)

        response_data = {'foo': 'bar'}

        # unpack incoming data
        data = json.loads(request.body)

        username_r = request.user
        message = data['message']
        date_now = date.today()
        date_r = date.fromisoformat(data['list'][0]['date'])
        intervals = data['list'][0]['intervals']
        department = data['department']
        slug = data['slug']

        logging.info("user       --> " + str(username_r))
        logging.info("date now   --> " + str(date_now))
        logging.info("date req   --> " + str(date_r))
        logging.info("intervals  --> " + str(intervals))
        logging.info("message    --> " + str(message))
        logging.info("department --> " + department)
        logging.info("slug       --> " + slug)

        # prevent from register in the current week
        date_diff = (date_r-date_now).days
        if date_diff < 7:
            response_data['error'] = 'minimum 7 days'
            logging.info("Error: no 7 days minimum")
            return JsonResponse(response_data)

        room = Room.available.get_room_from_slug(slug)
        reservation_exist = RegistrationEntry.objects_custom.day_filter(date_r, room[0])

        # updating exist reservation
        if reservation_exist:
            logging.info("obiekt dla tego dnia isntieje, proba aktualizacji")

            # check for reservation colision
            for _ in reservation_exist[0].reserved:
                logging.info(int(_))
                if int(_) in intervals:
                    logging.info("Error: reservation already exists")
                    response_data['error'] = 'reservation already exists'
                    return JsonResponse(response_data)

            logging.info("brak kolizji, tworzenie rezerwacji")
            reserved_new = list(reservation_exist[0].reserved)
            _update_reservation(reserved_new, intervals, reservation_exist, username_r)
        # create new object for new reservation
        else:
            logging.info("brak obiektu dla danej daty, proba utworzenia")
            _new_reservation(date_r, room, intervals, username_r)

        logging.info("Everything seems ok")
        response_data['error'] = 'none'
        return JsonResponse(response_data)

    if request.method == "GET":
        return render(request,
                      'laboratoria/room/stanowisko_export.html',
                      {'rooms': 'aa'})


def _new_reservation(date, room, interv, user):
    logging.config.dictConfig(LOGGING)
    logging.info("_new_reservation")
    logging.info(date)
    logging.info(room)
    logging.info(interv)
    logging.info(user)

    new_register = RegistrationEntry()
    new_register.registerDate = date
    new_register.roomConnector = room[0]

    intervals = interv
    username_r = user

    reserved_new = []
    for _ in intervals:
        reserved_new.append(str(_))
        if _ == 0:
            new_register.res_name_0 = username_r
        if _ == 1:
            new_register.res_name_1 = username_r
        if _ == 2:
            new_register.res_name_2 = username_r
        if _ == 3:
            new_register.res_name_3 = username_r
        if _ == 4:
            new_register.res_name_4 = username_r
        if _ == 5:
            new_register.res_name_5 = username_r
        if _ == 6:
            new_register.res_name_6 = username_r
        if _ == 7:
            new_register.res_name_7 = username_r
        if _ == 8:
            new_register.res_name_8 = username_r
        if _ == 9:
            new_register.res_name_9 = username_r
        if _ == 10:
            new_register.res_name_10 = username_r
        if _ == 11:
            new_register.res_name_11 = username_r
        if _ == 12:
            new_register.res_name_12 = username_r
        if _ == 13:
            new_register.res_name_13 = username_r
        if _ == 14:
            new_register.res_name_14 = username_r
        if _ == 15:
            new_register.res_name_15 = username_r
        if _ == 16:
            new_register.res_name_16 = username_r
        if _ == 17:
            new_register.res_name_17 = username_r
        if _ == 18:
            new_register.res_name_18 = username_r
        if _ == 19:
            new_register.res_name_19 = username_r
        if _ == 20:
            new_register.res_name_20 = username_r
        if _ == 21:
            new_register.res_name_21 = username_r
        if _ == 22:
            new_register.res_name_22 = username_r
        if _ == 23:
            new_register.res_name_23 = username_r
    reserved_new.sort()
    new_register.reserved = reserved_new
    new_register.save()
    logging.info('nowy obiekt utworzony')

def _update_reservation(res_new, interv, reserv, user):
    logging.config.dictConfig(LOGGING)
    logging.info("_update_reservation")
    logging.info(res_new)
    logging.info(interv)
    logging.info(reserv)
    logging.info(user)

    reserved_new = res_new
    intervals = interv
    reservation_exist = reserv
    username_r = user

    for _ in intervals:
        reserved_new.append(str(_))
        if _ == 0:
            reservation_exist.update(res_name_0=username_r)
        if _ == 1:
            reservation_exist.update(res_name_1=username_r)
        if _ == 2:
            reservation_exist.update(res_name_2=username_r)
        if _ == 3:
            reservation_exist.update(res_name_3=username_r)
        if _ == 4:
            reservation_exist.update(res_name_4=username_r)
        if _ == 5:
            reservation_exist.update(res_name_5=username_r)
        if _ == 6:
            reservation_exist.update(res_name_6=username_r)
        if _ == 7:
            reservation_exist.update(res_name_7=username_r)
        if _ == 8:
            reservation_exist.update(res_name_8=username_r)
        if _ == 9:
            reservation_exist.update(res_name_9=username_r)
        if _ == 10:
            reservation_exist.update(res_name_10=username_r)
        if _ == 11:
            reservation_exist.update(res_name_11=username_r)
        if _ == 12:
            reservation_exist.update(res_name_12=username_r)
        if _ == 13:
            reservation_exist.update(res_name_13=username_r)
        if _ == 14:
            reservation_exist.update(res_name_14=username_r)
        if _ == 15:
            reservation_exist.update(res_name_15=username_r)
        if _ == 16:
            reservation_exist.update(res_name_16=username_r)
        if _ == 17:
            reservation_exist.update(res_name_17=username_r)
        if _ == 18:
            reservation_exist.update(res_name_18=username_r)
        if _ == 19:
            reservation_exist.update(res_name_19=username_r)
        if _ == 20:
            reservation_exist.update(res_name_20=username_r)
        if _ == 21:
            reservation_exist.update(res_name_21=username_r)
        if _ == 22:
            reservation_exist.update(res_name_22=username_r)
        if _ == 23:
            reservation_exist.update(res_name_23=username_r)
    reserved_new.sort()
    reservation_exist.update(reserved=reserved_new)
