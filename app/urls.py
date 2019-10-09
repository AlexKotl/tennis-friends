from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('', include('django.contrib.auth.urls')),
    path('players/', views.PlayersView.as_view(), name='players'),
    path('players/<id>', views.PlayerView.as_view(), name='player'),
    path('players/<id>/message', views.MessageView.as_view(), name='message_player'),
    path('courts/', views.CourtsView.as_view(), name='courts'),
    path('courts/<id>', views.CourtView.as_view(), name='court'),
    path('friends/', views.FriendsView.as_view(), name='friends'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('admin/', admin.site.urls),
]
