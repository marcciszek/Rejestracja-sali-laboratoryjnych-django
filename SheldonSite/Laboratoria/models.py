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
        GROUND = 0
        FIRST = 1
        SECOUND = 2
    floor = models.IntegerField(choices=Floor.choices,
                                default=0)

    room_number = models.PositiveIntegerField()
    title = models.CharField(max_length=50)
    description = models.TextField()

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
            self.slug = slugify(str(self.floor) + "-" + str(self.room_number))
        super(Room, self).save(*args, **kwargs)

    class Meta:
        ordering = ('floor', 'room_number')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('laboratoria:room_detail',
                       args=[self.slug])

    # Room.objects.all() for all created rooms
    objects = models.Manager()
    # Room.available.all() for all available rooms
    available = AvailableManager()
