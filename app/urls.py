from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('', include('django.contrib.auth.urls')),
    path('players/', views.players_list, name='players'),
    path('players/<id>', views.PlayerView.as_view(), name='player'),
    path('courts/', views.courts_list, name='courts'),
    path('courts/<id>', views.CourtView.as_view(), name='court'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('admin/', admin.site.urls),
]
