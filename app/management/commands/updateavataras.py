from django.core.management.base import BaseCommand, CommandError
from app.models import Player

class Command(BaseCommand):
    help = 'Updates all empty user avataras using API'

    def handle(self, *args, **options):
        self.stdout.write("Done")