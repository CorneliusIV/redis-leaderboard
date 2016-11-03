from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.views.generic import DetailView, ListView
from .models import get_leaderboard_top25, Player

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
