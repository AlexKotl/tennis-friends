from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('players/', views.players_list, name='players'),
    path('courts/', views.courts_list, name='courts'),
    path('admin/', admin.site.urls),
]
