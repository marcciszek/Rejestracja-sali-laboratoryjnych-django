from django.db import models
from django.utils.text import slugify
from django.urls import reverse

from multiselectfield import MultiSelectField


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
            self.slug = slugify(str(self.floor) + "-"
                                + str(self.room_number) + "-"
                                + str(self.room_station))
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


class CustomManager(models.Manager):
    def month_filter(self, year, month):
        return super(CustomManager, self).\
            get_queryset()\
            .filter(year_copy=year, month_copy=month)\
            .order_by('registerDate')

    def year_filter(self, year):
        return super(CustomManager, self). \
            get_queryset() \
            .filter(year_copy=year) \
            .order_by('registerDate')


class RegistrationEntry(models.Model):

    class HoursInDay(models.IntegerChoices):
        Hour0 = 0, "00:00 - 01:00"
        Hour1 = 1, "01:00 - 02:00"
        Hour2 = 2, "02:00 - 03:00"
        Hour3 = 3, "03:00 - 04:00"
        Hour4 = 4, "04:00 - 05:00"
        Hour5 = 5, "05:00 - 06:00"
        Hour6 = 6, "06:00 - 07:00"
        Hour7 = 7, "07:00 - 08:00"
        Hour8 = 8, "08:00 - 09:00"
        Hour9 = 9, "09:00 - 10:00"
        Hour10 = 10, "10:00 - 11:00"
        Hour11 = 11, "11:00 - 12:00"
        Hour12 = 12, "12:00 - 13:00"
        Hour13 = 13, "13:00 - 14:00"
        Hour14 = 14, "14:00 - 15:00"
        Hour15 = 15, "15:00 - 16:00"
        Hour16 = 16, "16:00 - 17:00"
        Hour17 = 17, "17:00 - 18:00"
        Hour18 = 18, "18:00 - 19:00"
        Hour19 = 19, "19:00 - 20:00"
        Hour20 = 20, "20:00 - 21:00"
        Hour21 = 21, "21:00 - 22:00"
        Hour22 = 22, "22:00 - 23:00"
        Hour23 = 23, "23:00 - 00:00"

    registerDate = models.DateField(unique_for_date='registerDate',
                                    verbose_name="Data Rejestracji")

    # help for queries
    year_copy = models.IntegerField(default=None, null=True)
    month_copy = models.IntegerField(default=None, null=True)

    reserved = MultiSelectField(choices=HoursInDay.choices,
                                blank=True,
                                max_choices=24,
                                max_length=100,
                                verbose_name="Zarezerwowane")

    pending = MultiSelectField(choices=HoursInDay.choices,
                               blank=True,
                               max_choices=24,
                               max_length=100,
                               verbose_name="Oczekujące")

    def get_absolute_url(self):
        return reverse('laboratoria:day_detail',
                       args=[str(self.registerDate)])

    def save(self, *args, **kwargs):
        self.year_copy = self.registerDate.year
        self.month_copy = self.registerDate.month
        super(RegistrationEntry, self).save(*args, **kwargs)

    # dodac pole tekstu dla kazdej godziny (zarezerwowany i oczekujacy)
    # upewnic sie ze jest dodawane/usuwane
    # dodac polaczenie z konkretna sala

    def __str__(self):
        return str(self.registerDate)

    class Meta:
        verbose_name = 'rezerwacja'
        verbose_name_plural = 'rezerwacje'

    # default manager
    objects = models.Manager()
    # custom manager
    objects_custom = CustomManager()
