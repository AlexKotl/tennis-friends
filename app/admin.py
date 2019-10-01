from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import *

from .models import *

class PlayerAdmin(UserAdmin):
    add_form = PlayerCreationForm
    form = PlayerChangeForm
    model = Player
    list_display = ['email', 'username',]

admin.site.register(Player, PlayerAdmin)
admin.site.register(Court)