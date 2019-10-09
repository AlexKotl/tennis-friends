from django.core.management.base import BaseCommand, CommandError
from app.models import Player

class Command(BaseCommand):
    help = 'Updates all empty user avataras using API'

    def handle(self, *args, **options):
        players = Player.objects.filter(image_url="")[:10]
        for player in players:
            avatara = player.get_avatar(player.email)
            self.stdout.write("Got avatara for {}: {}".format(player.email, avatara))
        self.stdout.write("Done")