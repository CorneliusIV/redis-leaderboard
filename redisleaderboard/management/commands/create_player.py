import logging
import string
import random

from django.core.management.base import BaseCommand

from redisleaderboard.models import Game, Player


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Sets up all active pipelines to run in an rq worker'

    def handle(self, *args, **options):
        for x in range(100000):
            ran_name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
            player = Player.objects.create(name=ran_name)
            score = random.uniform(1, 30)
            Game.objects.create(player=player, score=score)
