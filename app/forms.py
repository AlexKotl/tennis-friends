from django import forms

class RegisterForm(forms.Form):
    first_name = forms.CharField(label='Имя', max_length=100)
    email = forms.EmailField(label='Email', max_length=100)
    phone = forms.CharField(label='Телефон', max_length=100)
    courts = forms.CharField(label='Корты на которых вы играете', max_length=100)
    rank = forms.CharField(label='Ваш уровень', max_length=100)
    player_since = forms.CharField(label='Когда вы начали играть?', max_length=100)
