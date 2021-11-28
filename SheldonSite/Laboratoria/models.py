from django.db import models
from django.utils.text import slugify
from django.urls import reverse


class AvailableManager(models.Manager):
    def get_queryset(self):
        return super(AvailableManager, self).\
            get_queryset()\
            .filter(status='available')


class Room(models.Model):
    class Floor(models.IntegerChoices):
        Parter = 0
        Pierwsze = 1
        Drugie = 2
    floor = models.IntegerField(choices=Floor.choices,
                                default=0,
                                verbose_name="Piętro")

    room_number = models.PositiveIntegerField(verbose_name="Numer pokoju")
    room_station = models.PositiveIntegerField(default=1,
                                               verbose_name="Numer stanowiska")
    title = models.CharField(max_length=50,
                             verbose_name="Nazwa pokoju")
    description = models.TextField(verbose_name="Opis")

    slug = models.SlugField(unique=True)

    STATUS_CHOICES = (
        ('available', 'Dostępna'),
        ('disabled', 'Wyłączona'),
    )
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='disabled')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(str(self.floor) + "-" + str(self.room_number) + "-" + str(self.room_station))
        super(Room, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Laboratorium'
        verbose_name_plural = 'Laboratoria'
        ordering = ('floor', 'room_number', 'room_station')
        unique_together = ['floor', 'room_number', 'room_station']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('laboratoria:room_detail',
                       args=[self.slug])

    # Room.objects.all() for all created rooms
    objects = models.Manager()
    # Room.available.all() for all available rooms
    available = AvailableManager()
