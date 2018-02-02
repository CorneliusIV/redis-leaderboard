import json
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
        rank = rediscon.zrevrank('leaderboard', self.name)
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


def response_to_dict(b):
    d = json.loads(b[0].decode('utf8'))
    d.update({'score': b[1]})
    return d


def get_start_rank(player_value):
    first_rank = rediscon.zrevrank('leaderboard', str(player_value))
    return first_rank + 1


def get_leaderboard(direction, top_score, size):
    rank = 0
    if direction is 'gt':
        byte_leaderboard = rediscon.zrangebyscore(
            'leaderboard', top_score, '+inf', 0, size, withscores=True)
        if len(byte_leaderboard) is 0:
            rank = 1
        else:
            byte_leaderboard = byte_leaderboard[::-1]
            start_rank = byte_leaderboard[0]
            rank = get_start_rank(start_rank[0].decode('utf8'))
    else:
        byte_leaderboard = rediscon.zrevrangebyscore(
            'main_leaderboard', top_score, '-inf', 0, size, withscores=True)
    leaderboard = [response_to_dict(b) for b in byte_leaderboard]
    return leaderboard, rank


def get_leaderboard_top25():
    leaderboard = rediscon.zrevrange(
        'leaderboard', 0, 24, withscores=True)
    return leaderboard
