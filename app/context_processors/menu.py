from django.template.context_processors import request
from app.models import Player, Message

def menu(request):
    if request.user.id == None:
        return {'menu_friends_count': ''}

    user = Player.objects.get(pk=request.user.id)
    messages = Message.objects.filter(recipient=user, is_read=False)
    return {
        "menu_friends_count": '' if messages.count() == 0 else messages.count()
    }