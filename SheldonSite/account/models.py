from django.db import models
from django.conf import settings

from django.utils.translation import gettext, gettext_lazy as _


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

    def __str__(self):
        return ''
