from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django import forms
from django.utils.translation import gettext_lazy as _
from django.forms.fields import EmailField


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(label=_('first name').capitalize(),
                                 required=True,
                                 max_length=150,
                                 widget=forms.TextInput())
    last_name = forms.CharField(label=_('last name').capitalize(),
                                required=True,
                                max_length=150,
                                widget=forms.TextInput())
    email = forms.EmailField(label=_('email').capitalize(),
                             required=True,
                             max_length=150,
                             widget=forms.EmailInput())

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

