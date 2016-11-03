from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.db.models import Count
from django.shortcuts import redirect
from django.views.generic import TemplateView, ListView
from .models import get_leaderboard_top25, Player

from django_redis import get_redis_connection


rediscon = get_redis_connection('leaderboard')

from .forms import GameForm
from .models import Game


class LeaderboardView(ListView):
    model = Game
    template_name = 'leaderboard.html'
    form_class = GameForm

    def get_queryset(self):
        data = []
        queryset = get_leaderboard_top25()
        data = [{'name': cards[0], 'top_score': cards[1]} for cards in queryset]
        return data

    # Keep for comparison
    # def get_queryset(self):
    #     players = Player.objects.order_by('-top_score')[:25]
    #     return players


class PlayerView(TemplateView):
    model = Player
    template_name = 'player.html'
    form_class = GameForm

    def get_context_data(self, **kwargs):
        context = super(PlayerView, self).get_context_data(**kwargs)
        rank = rediscon.zrevrank('leaderboard', 'FEG6MMR6HB')
        context['rank'] = rank + 1
        return context

    # Keep for comparison
    # def get_context_data(self, **kwargs):
    #     context = super(PlayerView, self).get_context_data(**kwargs)
    #     player = Player.objects.get(name='FEG6MMR6HB')
    #     aggregate = Player.objects.filter(
    #         top_score__gt=player.top_score).aggregate(ranking=Count('top_score'))
    #     context['rank'] = aggregate['ranking']
    #     return context
