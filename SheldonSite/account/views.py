from .forms import UserRegistrationForm
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from.models import Profile


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password1'])
            new_user.save()
            profile = Profile.objects.create(user=new_user)
            return render(request,
                          'registration/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'registration/register.html',
                  {'user_form': user_form})

def usertest(request):
    return render(request,'userpage.html',{'foo':'bar'})

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

@login_required
def userprofile(request, username):
    user = get_object_or_404(User, username=username)

    # logging.config.dictConfig(LOGGING)

    name = user.username
    first_name = user.first_name
    last_name = user.last_name
    email = user.email
    last_login = user.last_login
    date_joined = user.date_joined
    rank = Profile.Rank(user.profile.user_rank).name
    phone_number = user.profile.phone_number
    return render(request,
                  'userpage.html',
                  {'name':name,
                   'first_name':first_name,
                   'last_name':last_name,
                   'email':email,
                   'last_login':last_login,
                   'date_joined':date_joined,
                   'rank':rank,
                   'phone_number':phone_number})