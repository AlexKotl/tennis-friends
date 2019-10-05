from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db import models
from datetime import datetime

class Court(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=255,default="")
    url = models.CharField(max_length=255,default="")
    image = models.CharField(max_length=255,default="")
    map_lat = models.FloatField(default=0)
    map_lng = models.FloatField(default=0)
    flag = models.IntegerField(default=1)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"

class Player(AbstractUser):
    username = models.CharField(max_length=180, unique=False)
    email = models.CharField(max_length=180, unique=True)
    phone = models.CharField(max_length=180)
    courts = models.ManyToManyField(Court)
    is_looking = models.IntegerField(default=0)
    rank = models.FloatField(default=0)
    player_since = models.IntegerField(default=0)
    about = models.TextField(default="")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

class Message(models.Model):
    author = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="authors")
    recipient = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="recipients")
    text = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.text}"