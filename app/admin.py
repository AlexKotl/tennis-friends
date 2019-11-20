from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import *

from .models import *

class PlayerAdmin(UserAdmin):
    add_form = PlayerCreationForm
    form = PlayerChangeForm
    model = Player
    list_display = ['email', 'phone', 'rank']

class CourtAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'phone',]

admin.site.register(Player)
admin.site.register(Court, CourtAdmin)
admin.site.register(Message)
admin.site.register(Request)