from django.db import models
from django.core.validators import MaxValueValidator
from django.utils import timezone
import datetime

TODAY = timezone.now().date()

class Menu(models.Model):
    title = models.CharField(max_length=255, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    inventory = models.PositiveSmallIntegerField()

    def __str__(self):
        return f'{self.title}'

class Booking(models.Model):
    TIME_CHOICES = [
        ('21:00:00', '9 PM'), ('21:05:00', '9:05 PM'), ('21:10:00', '9:10 PM'), ('21:15:00', '9:15 PM'),
        ('21:20:00', '9:20 PM'), ('21:25:00', '9:25 PM'), ('21:30:00', '9:30 PM'), ('21:35:00', '9:35 PM'),
        ('21:40:00', '9:40 PM'), ('21:45:00', '9:45 PM'), ('21:50:00', '9:50 PM'), ('21:55:00', '9:55 PM'),
        ('22:00:00', '10 PM'), ('22:05:00', '10:05 PM'), ('22:10:00', '10:10 PM'), ('22:15:00', '10:15 PM'),
        ('22:20:00', '10:20 PM'), ('22:25:00', '10:25 PM'), ('22:30:00', '10:30 PM'), ('22:35:00', '10:35 PM'),
        ('22:45:00', '10:45 PM'), ('22:50:00', '10:50 PM'), ('22:55:00', '10:55 PM'), ('23:00:00', '11 PM'),
    ]
    DATE_CHOICES = [(TODAY + datetime.timedelta(days=n), TODAY + datetime.timedelta(days=n)) for n in range(7)]

    name = models.CharField(max_length=255, db_index=True)
    no_of_guests = models.PositiveSmallIntegerField(validators=[MaxValueValidator(6)])
    date = models.DateField(db_index=True, choices=DATE_CHOICES)
    time = models.TimeField(unique_for_date='date', choices=TIME_CHOICES)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f'{self.name} - {self.date}'
