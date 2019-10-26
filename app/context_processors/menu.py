from django.template.context_processors import request

def menu(request):
    return {
        "menu_friends_count": 0
    }