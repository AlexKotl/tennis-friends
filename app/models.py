from django.db import models
from datetime import datetime

class Court(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    map_lat = models.FloatField(default=0)
    map_lng = models.FloatField(default=0)

    def __str__(self):
        return f"{self.name}"

class Player(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    courts = models.ManyToManyField(Court)
    is_looking = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"