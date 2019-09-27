from django.shortcuts import render, get_object_or_404
from .models import Player, Court

def index(request):
    return render(request, 'index.html', {
        # 'bases': Base.get_all(request),
    })

def players_list(request):
    return render(request, 'players.html', {
        'players': Player.objects.filter(flag=1).order_by('-pk'),
    })

def courts_list(request):
    return render(request, 'courts.html', {
        'courts': Court.objects.filter(flag=1).order_by('-pk'),
    })

def login(request):
    return render(request, 'login.html')

def register(request):
    pass