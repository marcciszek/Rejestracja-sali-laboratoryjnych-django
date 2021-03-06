from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

from multiselectfield import MultiSelectField


class AvailableManager(models.Manager):
    def get_queryset(self):
        return super(AvailableManager, self).\
            get_queryset()\
            .filter(status='available')

    def get_room_from_slug(self, slug):
        return super(AvailableManager, self).\
            get_queryset()\
            .filter(slug=slug)


class Room(models.Model):
    class Floor(models.IntegerChoices):
        Parter = 0
        Pierwsze = 1
        Drugie = 2
    floor = models.IntegerField(choices=Floor.choices,
                                default=0,
                                verbose_name="Piętro")

    room_number = models.PositiveIntegerField(verbose_name="Numer pokoju",
                                              validators=[MinValueValidator(1),
                                                          MaxValueValidator(100_000)])
    room_station = models.PositiveIntegerField(default=1,
                                               verbose_name="Numer stanowiska",
                                               validators=[MinValueValidator(1),
                                                           MaxValueValidator(100_000)])
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
    def all_entries(self, room):
        return super(CustomManager, self).\
            get_queryset()\
            .filter(roomConnector=room)\
            .order_by('registerDate')

    def day_filter(self, date_iso, room):
        return super(CustomManager, self).\
            get_queryset()\
            .filter(roomConnector=room, registerDate=date_iso)

    def month_filter(self, year, month):
        return super(CustomManager, self).\
            get_queryset()\
            .filter(year_copy=year,
                    month_copy=month)\
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

    registerDate = models.DateField(verbose_name="Data Rejestracji")

    roomConnector = models.ForeignKey(Room,
                                      on_delete=models.CASCADE,
                                      null=True,
                                      verbose_name="Dotyczy")

    # help for queries
    year_copy = models.IntegerField(default=None, null=True)
    month_copy = models.IntegerField(default=None, null=True)

    reserved = MultiSelectField(choices=HoursInDay.choices,
                                blank=True,
                                max_choices=24,
                                max_length=100,
                                verbose_name="Zarezerwowane")


    res_name_0 = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='rn0', verbose_name="00:00 - 01:00")
    res_name_1 = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='rn1', verbose_name="01:00 - 02:00")
    res_name_2 = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='rn2', verbose_name="02:00 - 03:00")
    res_name_3 = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='rn3', verbose_name="03:00 - 04:00")
    res_name_4 = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='rn4', verbose_name="04:00 - 05:00")
    res_name_5 = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='rn5', verbose_name="05:00 - 06:00")
    res_name_6 = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='rn6', verbose_name="06:00 - 07:00")
    res_name_7 = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='rn7', verbose_name="07:00 - 08:00")
    res_name_8 = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='rn8', verbose_name="08:00 - 09:00")
    res_name_9 = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='rn9', verbose_name="09:00 - 10:00")
    res_name_10 = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='rn10', verbose_name="10:00 - 11:00")
    res_name_11 = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='rn11', verbose_name="11:00 - 12:00")
    res_name_12 = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='rn12', verbose_name="12:00 - 13:00")
    res_name_13 = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='rn13', verbose_name="13:00 - 14:00")
    res_name_14 = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='rn14', verbose_name="14:00 - 15:00")
    res_name_15 = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='rn15', verbose_name="15:00 - 16:00")
    res_name_16 = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='rn16', verbose_name="16:00 - 17:00")
    res_name_17 = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='rn17', verbose_name="17:00 - 18:00")
    res_name_18 = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='rn18', verbose_name="18:00 - 19:00")
    res_name_19 = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='rn19', verbose_name="19:00 - 20:00")
    res_name_20 = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='rn20', verbose_name="20:00 - 21:00")
    res_name_21 = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='rn21', verbose_name="21:00 - 22:00")
    res_name_22 = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='rn22', verbose_name="22:00 - 23:00")
    res_name_23 = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='rn23', verbose_name="23:00 - 00:00")

    def get_absolute_url(self):
        return reverse('laboratoria:day_detail',
                       args=[str(self.registerDate)])

    def save(self, *args, **kwargs):
        self.year_copy = self.registerDate.year
        self.month_copy = self.registerDate.month
        super(RegistrationEntry, self).save(*args, **kwargs)

    # dodac pole tekstu dla kazdej godziny (zarezerwowany i oczekujacy)
    # upewnic sie ze jest dodawane/usuwane

    def __str__(self):
        return str(self.registerDate)

    class Meta:
        verbose_name = 'rezerwacja'
        verbose_name_plural = 'rezerwacje'
        unique_together = ['registerDate', 'roomConnector']

    # default manager
    objects = models.Manager()
    # custom manager
    objects_custom = CustomManager()


class CustomPendingManager(models.Manager):

    def pendings_all(self, room):
        return super(CustomPendingManager, self). \
            get_queryset() \
            .filter(room=room) \
            .order_by('date')

    def pendings_unprocessed(self):
        return super(CustomPendingManager, self). \
            get_queryset() \
            .filter(processed=False) \
            .order_by('room', 'date')


class RegistrationPending(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    intervals = MultiSelectField(choices=RegistrationEntry.HoursInDay.choices,
                                 blank=True,
                                 max_choices=24,
                                 max_length=100,
                                 verbose_name="Oczekujące")
    user_mentor = models.ForeignKey(User,
                                    on_delete=models.SET_NULL,
                                    null=True,
                                    blank=True,
                                    related_name="user_m")
    additional_info = models.TextField(blank=True,
                                       max_length = 255)
    processed = models.BooleanField(default=False)

    objects_custom = CustomPendingManager()
