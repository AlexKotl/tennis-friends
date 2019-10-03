from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.views import View, generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from .models import Player, Court
from .forms import PlayerCreationForm, PlayerChangeForm

class IndexView(View):
    def get(self, request):
        return render(request, 'index.html', {})

def players_list(request):
    return render(request, 'players.html', {
        'players': Player.objects.filter(is_active=1).annotate(courts_count=Count('courts')).order_by('-pk'),
    })

def courts_list(request):
    return render(request, 'courts.html', {
        'courts': Court.objects.filter(flag=1).order_by('-pk'),
    })

def login(request):
    return render(request, 'login.html')

class PlayerView(View):
    def get(self, request, id):
        return render(request, 'player.html', {
            'player': Player.objects.get(pk=id)
        })

class RegisterView(generic.CreateView):
    form_class = PlayerCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'

class ProfileView(LoginRequiredMixin, generic.UpdateView):
    model = Player
    form_class = PlayerChangeForm
    template_name = 'profile.html'
    success_url = reverse_lazy('profile')
    #fields = ['first_name', 'last_name']

    def get_object(self, queryset=None):
        return Player.objects.get(pk=self.request.user.id)