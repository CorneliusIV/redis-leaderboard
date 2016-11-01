from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.views.generic import CreateView, UpdateView

from .forms import GameForm
from .models import Game


class LeaderboardView(CreateView):
    model = Game
    template_name = 'leaderboard.html'
    form_class = GameForm
