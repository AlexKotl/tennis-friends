from datetime import date
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.views import View, generic
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.core.mail import send_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.conf import settings
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from .models import Player, Court, Message, PlayerFilter, Request
from .forms import PlayerCreationForm, PlayerChangeForm, MessageForm, RequestCreationForm

class IndexView(View):
    def get(self, request):
        return render(request, 'homepage.html', {
            'requests': Request.objects.filter(flag=1, date__gte=date.today().strftime("%Y-%m-%d"), user__isnull=False).order_by('date'),
            'players': Player.objects.filter(is_active=1).annotate(courts_count=Count('courts')).order_by('-pk')[:6],
        })

class PlayersView(View):
    def get(self, request):
        players = Player.objects.filter(is_active=1).annotate(courts_count=Count('courts')).order_by('-pk');

        filter = PlayerFilter(request.GET, queryset=players)
        players = filter.qs
        paginator = Paginator(players, 36)
        page = request.GET.get('page')

        try:
            players = paginator.page(page)
        except PageNotAnInteger:
            players = paginator.page(1)
        except EmptyPage:
            players = paginator.page(paginator.num_pages)
        return render(request, 'players.html', {
            'filter': filter,
            'players': players,
        })

class CourtsView(View):
    def get(self, request):
        return render(request, 'courts.html', {
            'courts': Court.objects.filter(flag=1).annotate(players_count=Count('player')).order_by('-players_count'),
        })

class LoginView(generic.CreateView):
    template_name = 'login.html'

class PlayerView(View):
    def get(self, request, id):
        player = Player.objects.get(pk=id)
        messages = None
        show_phone = False
        if request.user.is_authenticated:
            user = Player.objects.get(pk=request.user.id)
            messages = Message.objects.filter(author__in=[user, player], recipient__in=[user, player]).order_by("-pk")
            # by default show only last N messages
            if request.GET.get('all_messages') == None:
                messages = messages[:20]

            # update unread messages count
            try:
                user_messages = Message.objects.filter(recipient=user, author=player, is_read=False).update(is_read=True)
            except Message.DoesNotExist:
                pass

            # if user is a friend - show phone no
            replies_count = Message.objects.filter(author=player, recipient=user).count()
            if replies_count > 0:
                show_phone = True

        return render(request, 'player.html', {
            'player': player,
            'messages': messages,
            'message_form': MessageForm,
            'show_phone': show_phone,
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
            message="Вам пришло новое сообщение от {}. \n\nПрочитать сообщение можно по ссылке: \n{}"
                .format(author.first_name, 'http://' + settings.SITE_URL + reverse('player', args=(author.id,))),
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
            'players': Player.objects.filter(courts=court).order_by('-image', '-pk'),
        })

class FriendsView(LoginRequiredMixin, View):
    def get(self, request):
        user = Player.objects.get(pk=request.user.id)
        messages = Message.objects.filter(Q(author=user) | Q(recipient=user)).order_by("-pk")
        # format new list with only top messages from every user
        player_processed = []
        top_messages = []
        for message in messages:
            # set actually friend to use in template
            if message.author == user:
                message.friend = message.recipient
            else:
                message.friend = message.author

            if message.friend not in player_processed:
                player_processed.append(message.friend)

                top_messages.append(message)

        return render(request, 'friends.html', {
            'messages': top_messages,
        })

class RegisterView(SuccessMessageMixin, generic.CreateView):
    form_class = PlayerCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')
    success_message = "Вы успешно зарегистрировались. Теперь можете войти в систему."

    # def form_valid(self, form):
    #     self.object = form.save()
    #     self.object.save()
    #     messages.success(self.request, self.success_message)
    #     return HttpResponseRedirect(self.get_success_url())

class ProfileView(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = Player
    form_class = PlayerChangeForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('profile')
    success_message = "Профиль сохранен."

    def get_object(self, queryset=None):
        return Player.objects.get(pk=self.request.user.id)

class SitemapView(View):
    def get(self, request):
        return render(request, 'sitemap.xml', {
            'courts': Court.objects.filter(flag=1),
            'players': Player.objects.filter(is_active=1),
            'date': date.today().strftime("%Y-%m-%d")
        })

class RequestsAddView(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    form_class = RequestCreationForm
    template_name = 'add_request.html'
    success_url = reverse_lazy('index')
    success_message = "Ваш запрос успешно добавлен."

    def form_valid(self, form):
        self.object = form.save()
        self.object.user = Player.objects.get(pk=self.request.user.id)
        self.object.save()
        messages.success(self.request, self.success_message) # force add message, mixin will not work in overrided method
        return HttpResponseRedirect(self.get_success_url())

class RequestsEditView(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = Request
    form_class = RequestCreationForm
    template_name = 'add_request.html'
    success_url = reverse_lazy('index')
    success_message = "Ваш запрос отредактирован."

class RequestsDeleteView(LoginRequiredMixin, View):
    def get(self, request, id):
        req = Request.objects.get(pk=id)
        if req.user.id != request.user.id:
            messages.success(self.request, "Недостаточно прав для удаления запроса.")
        else:
            req.flag = 2
            req.save()
            messages.success(self.request, "Ваш запрос удален.")
        return HttpResponseRedirect(reverse_lazy('index'))
