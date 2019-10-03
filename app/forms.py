from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from datetime import datetime
from .models import Player, Court

class PlayerCreationForm(UserCreationForm):
    first_name = forms.CharField(label='Имя', max_length=100, help_text="Ваше полное имя")
    email = forms.EmailField(label='Email', max_length=100)
    phone = forms.CharField(label='Телефон', max_length=100, help_text="Телефон будет скрыт от других пользователей")
    courts = forms.ModelMultipleChoiceField(
        queryset=Court.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Корты",
        help_text="Корты на которых вы играете"
    )
    rank = forms.ChoiceField(
        label="Уровень игры",
        choices=[(x/10, x/10) for x in range(10, 75, 5)],
        help_text="<a href='#' data-toggle='modal' data-target='#rankModal'>Как определить свой уровень?</a>",
    )
    player_since = forms.ChoiceField(
        label='Игровой опыт',
        choices=[(0, '-')] + [(x, f'с {x} года') for x in range(datetime.today().year, datetime.today().year - 10, -1)],
    )

    class Meta:
        model = Player
        fields = ( 'email', 'first_name', 'phone', 'courts', 'rank', 'player_since')

    def clean_username(self):
        print("cleaning username ")
        return self.data.get('email')

    # def clean(self):
    #     super().clean()
    #     self.cleaned_data['username'] = self.cleaned_data.get('email')
    #     print("Cleaned username: " + self.cleaned_data['username'])
    #     print(self.cleaned_data)
    #     return self.cleaned_data

class PlayerChangeForm(UserChangeForm):
    class Meta:
        model = Player
        fields = ('username', 'email',)