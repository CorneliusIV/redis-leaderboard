
from django.db import models
from django_redis import get_redis_connection


rediscon = get_redis_connection('leaderboard')


class Player(models.Model):

    name = models.CharField(
        max_length=10, unique=True,
        error_messages={'unique': 'Name not available.'})
    top_score = models.FloatField(db_index=True, default=0.0, blank=True)

    def __str__(self):
        return self.name

    def rank(self):
        player_value = self.redis_key_value()
        rank = rediscon.zrevrank('leaderboard', player_value)
        if rank is None:
            rank = 0
        return rank + 1

    def save(self, *args, **kwargs):
        super(Player, self).save(*args, **kwargs)
        rediscon.zadd('leaderboard', self.top_score, self.name)


class Game(models.Model):

    player = models.ForeignKey(
        Player,
        on_delete=models.CASCADE)
    score = models.FloatField(db_index=True)

    class Meta:
        verbose_name = 'Game'
        verbose_name_plural = 'Games'

    def __str__(self):
        return '{} {}'.format(self.player, self.score)

    def set_player_top_score(self):
        player = self.player
        player_top_score = player.top_score
        if self.score > player_top_score:
            player.top_score = self.score
            player.save()

    def save(self, *args, **kwargs):
        super(Game, self).save(*args, **kwargs)
        self.set_player_top_score()
