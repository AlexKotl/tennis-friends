from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.views import View, generic
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from .models import Player, Court, Message
from .forms import PlayerCreationForm, PlayerChangeForm, MessageForm

class IndexView(View):
    def get(self, request):
        return render(request, 'homepage.html', {})

def players_list(request):
    return render(request, 'players.html', {
        'players': Player.objects.filter(is_active=1).annotate(courts_count=Count('courts')).order_by('-pk'),
    })

def courts_list(request):
    return render(request, 'courts.html', {
        'courts': Court.objects.filter(flag=1).annotate(players_count=Count('player')).order_by('-pk'),
    })

def login(request):
    return render(request, 'login.html')

class PlayerView(View):
    def get(self, request, id):
        player = Player.objects.get(pk=id)
        messages = None
        if request.user.is_authenticated:
            user = Player.objects.get(pk=request.user.id)
            messages = Message.objects.filter(author__in=[user, player], recipient__in=[user, player]).order_by("-pk")

        return render(request, 'player.html', {
            'player': player,
            'messages': messages,
            'message_form': MessageForm
        })

class MessageView(LoginRequiredMixin, View):
    def post(self, request, id):
        try:
            author = Player.objects.get(pk=request.user.id)
            recipient = Player.objects.get(pk=id)
        except:
            raise Exception("Cant find author or recipient user")
        message = Message(author=author, recipient=recipient, text=request.POST.get('text', ''))
        message.save()
        result = 'sent'
        return HttpResponseRedirect("{}?r={}".format(reverse('player', args=(id,)), result))

class CourtView(View):
    def get(self, request, id):
        return render(request, 'court.html', {
            'court': Court.objects.get(pk=id)
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