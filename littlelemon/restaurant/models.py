from django.db import models
from django.core.validators import MaxValueValidator
from django.utils import timezone
import datetime

def generate_date_choices(days=7):
    date_choices = []
    now = timezone.now()
    if now.time() > datetime.time(hour=20):
        now = now + datetime.timedelta(days=1)
    for x in range(days):
        y = now.date() + datetime.timedelta(days=x)
        choice = (y, y)
        date_choices.append(choice)
    return date_choices

def generate_time_choices(start=21, end=23, min_interval=5):
    current_datetime = datetime.datetime(year=2024, month=1, day= 1, hour=start)
    end_datetime = datetime.datetime(year=2024, month=1, day=1, hour=end)
    current_time = current_datetime.time()
    time_choices = [(current_time, current_time)]
    while current_datetime < end_datetime:
        current_datetime += datetime.timedelta(minutes=min_interval)
        current_time = current_datetime.time()
        time_choices.append((current_time, current_time))
    return time_choices

class Menu(models.Model):
    title = models.CharField(max_length=255, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    inventory = models.PositiveSmallIntegerField()

    def __str__(self):
        return f'{self.title}'

class Booking(models.Model):

    name = models.CharField(max_length=255, db_index=True)
    no_of_guests = models.PositiveSmallIntegerField(validators=[MaxValueValidator(6)])
    date = models.DateField(db_index=True, choices=generate_date_choices())
    time = models.TimeField(unique_for_date='date', choices=generate_time_choices())

    class Meta:
        ordering = ['-date', '-time']

    def __str__(self):
        return f'{self.name} - {self.date} {self.time}'
