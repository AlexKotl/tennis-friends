from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from .models import Player

class PlayerCreationForm(UserCreationForm):
    first_name = forms.CharField(label='Имя', max_length=100, help_text="Имя")
    email = forms.EmailField(label='Email', max_length=100)
    phone = forms.CharField(label='Телефон', max_length=100)
    courts = forms.CharField(label='Корты на которых вы играете', max_length=100)
    rank = forms.CharField(label='Ваш уровень', max_length=100)
    player_since = forms.CharField(label='Когда вы начали играть?', max_length=100)

    class Meta:
        model = Player
        fields = ('username', "first_name", 'email')

class PlayerChangeForm(UserChangeForm):
    class Meta:
        model = Player
        fields = ('username', 'email')