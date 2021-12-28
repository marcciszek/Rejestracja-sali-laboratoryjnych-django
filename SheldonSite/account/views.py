from django.shortcuts import render
from .forms import UserRegistrationForm
from .models import Profile


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password1'])
            new_user.save()
            profile = Profile.objects.create(user=new_user)
            return render(request,
                          'reservation/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'reservation/register.html',
                  {'user_form': user_form})