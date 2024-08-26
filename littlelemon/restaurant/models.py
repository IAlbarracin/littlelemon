from django.db import models
from django.core.validators import MaxValueValidator

class Menu(models.Model):
    title = models.CharField(max_length=255, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    inventory = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ['title']

    def __str__(self):
        return f'{self.title}'

class Booking(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    no_of_guests = models.PositiveSmallIntegerField(validators=[MaxValueValidator(6)])
    date = models.DateTimeField()

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f'{self.name} - {self.date}'
