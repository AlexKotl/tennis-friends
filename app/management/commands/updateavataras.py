from django.core.management.base import BaseCommand, CommandError
from app.models import Player

class Command(BaseCommand):
    help = 'Updates all empty user avataras using API'

    def add_arguments(self, parser):
        parser.add_argument('--update-all',
            help='Force update all avatars that failed.',
            nargs='?',
            default=False)

    def handle(self, *args, **options):
        if options['update_all'] == False:
            players = Player.objects.filter(image_url="")[:10]
        else:
            players = Player.objects.filter(image_url="-")[:100]

        for player in players:
            avatara = player.get_avatar(player.email)
            player.image_url = avatara
            player.save()
            self.stdout.write("Got avatara for {}: {}".format(player.email, avatara))
        self.stdout.write("Done")