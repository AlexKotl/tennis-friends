from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.views import View, generic
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.core.mail import send_mail
from django.conf import settings
from .models import Player, Court, Message
from .forms import PlayerCreationForm, PlayerChangeForm, MessageForm

class IndexView(View):
    def get(self, request):
        return render(request, 'homepage.html', {
            'courts': Court.objects.filter(flag=1).annotate(players_count=Count('player')).order_by('-pk')[:6],
            'players': Player.objects.filter(is_active=1).annotate(courts_count=Count('courts')).order_by('-pk')[:6],
        })

class PlayersView(View):
    def get(self, request):
        return render(request, 'players.html', {
            'players': Player.objects.filter(is_active=1).annotate(courts_count=Count('courts')).order_by('-pk'),
        })

class CourtsView(View):
    def get(self, request):
        return render(request, 'courts.html', {
            'courts': Court.objects.filter(flag=1).annotate(players_count=Count('player')).order_by('-pk'),
        })

class LoginView(generic.CreateView):
    template_name = 'login.html'

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

        send_mail(subject="{} - новое сообщение".format(settings.SITE_NAME),
            message="Вам пришло новое сообщение от {}: \n\n{}\n\n{}"
                .format(author.first_name, request.POST.get('text', ''), settings.SITE_URL),
            from_email=settings.SITE_EMAIL,
            recipient_list=[recipient.email],
            fail_silently=not settings.DEBUG)

        result = 'sent'
        return HttpResponseRedirect("{}?r={}".format(reverse('player', args=(id,)), result))

class CourtView(View):
    def get(self, request, id):
        court = Court.objects.annotate(players_count=Count('player')).get(pk=id)
        return render(request, 'court.html', {
            'court': court,
            'players': Player.objects.filter(courts=court),
        })

class FriendsView(LoginRequiredMixin, View):
    def get(self, request):
        user = Player.objects.get(pk=request.user.id)
        messages = Message.objects.filter(Q(author=user) | Q(recipient=user)).order_by("-pk")
        # format new list with only top messages from every user
        player_processed = [user]
        top_messages = []
        for message in messages:
            if message.author not in player_processed or message.recipient not in player_processed:
                if message.author not in player_processed:
                    player_processed.append(message.author)
                if message.recipient not in player_processed:
                    player_processed.append(message.recipient)
                top_messages.append(message)

        return render(request, 'friends.html', {
            'messages': top_messages,
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