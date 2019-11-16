import json
import requests
import os
import django_filters
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db import models
from datetime import datetime
from PIL import Image, ExifTags

class Court(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=255, default="", blank=True)
    url = models.CharField(max_length=255, default="", blank=True)
    image = models.ImageField(upload_to='courts/')
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
    phone = models.CharField(max_length=180, blank=True)
    courts = models.ManyToManyField(Court, blank=True)
    image_url = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='users/',blank=True)
    is_looking = models.BooleanField(default=False)
    is_looking_date = models.DateTimeField(auto_now=True)
    rank = models.FloatField(default=0)
    player_since = models.IntegerField(default=0)
    about = models.TextField(default="",blank=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

    def get_nickname(self):
        return self.email.split("@")[0]

    nickname = property(get_nickname)

    def save(self, *args, **kwargs):
        if self.image:
            try:
                super().save() # first save image

                im = Image.open(self.image.path)

                # detect image rotation
                for orientation in ExifTags.TAGS.keys():
                    if ExifTags.TAGS[orientation] == 'Orientation':
                        break

                exif = dict(im._getexif().items())

                if exif[orientation] == 3:
                    im = im.rotate(180, expand=True)
                elif exif[orientation] == 6:
                    im = im.rotate(270, expand=True)
                elif exif[orientation] == 8:
                    im = im.rotate(90, expand=True)

                im.thumbnail((1000, 1000))
                im.save(self.image.path, im.format)
            except IOError:
                print("cannot create thumbnail for", self.image)
            except (AttributeError, KeyError, IndexError):
                print("Getting exif error")

        super(Player, self).save(*args, **kwargs)

    def get_avatar(self, email):
        '''
        This function as currently not available due to dead API
        '''
        try:
            response = requests.get("https://api.devidentify.com/{}".format(email))
        except Exception as err:
            self.stdout.write("Some error raised while getting API: {}".format(err))
            return

        try:
            data = json.loads(response.content)
        except:
            self.stdout.write("Failed to parse JSON")
            return

        if data['success'] == False or data['profile_picture'] == '':
            data['profile_picture'] = '-'

        return data['profile_picture']

class PlayerFilter(django_filters.FilterSet):
    ranks = [(x/10, x/10) for x in range(10, 75, 5)];
    rank__gt = django_filters.ChoiceFilter(
        choices=ranks,
        empty_label="Мин. уровень",
        field_name='rank',
        lookup_expr='gte')
    rank__lt = django_filters.ChoiceFilter(
        choices=ranks,
        empty_label="Макс. уровень",
        field_name='rank',
        lookup_expr='lte')

    first_name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Player
        fields = []

class Message(models.Model):
    author = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="authors")
    recipient = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="recipients")
    text = models.TextField()
    is_read = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.text} (from: {self.author.first_name} -> {self.recipient.first_name})"