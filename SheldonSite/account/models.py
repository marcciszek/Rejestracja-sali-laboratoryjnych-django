from django.db import models
from django.conf import settings
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth.models import User


# make email unique on a database level
User._meta.get_field('email')._unique = True


class Profile(models.Model):
    class Rank(models.IntegerChoices):
        Admin = 0
        Uprzywilejowany = 1
        Zwykly = 2
        Gosc = 3
        Niepotwierdzony = 4

    class Meta:
        verbose_name = 'Uprawnienia dodatkowe'
        verbose_name_plural = 'Uprawnienia dodatkowe'

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, unique=True)

    user_rank = models.IntegerField(choices=Rank.choices,
                                    default=Rank.Niepotwierdzony,
                                    verbose_name="Ranga")

    phone_number = models.CharField(max_length=12,
                                    default='',
                                    blank=True)

    def __str__(self):
        return ''
