from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Player, Court
from .forms import RegisterForm

class IndexView(View):
    def get(self, request):
        return render(request, 'index.html', {})

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
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {
        'form': form
    })

class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'profile.html', {})