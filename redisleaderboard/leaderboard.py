import json
from django.conf import settings
from django_redis import get_redis_connection

if settings.APP_STATE not in ('postactivation', 'recap'):
    rediscon = get_redis_connection('leaderboard')


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
            'leaderboard', top_score, '-inf', 0, size, withscores=True)
    leaderboard = [response_to_dict(b) for b in byte_leaderboard]
    return leaderboard, rank


def get_leaderboard_top25():
    byte_leaderboard = rediscon.zrevrange(
        'leaderboard', 0, 24, withscores=True)
    leaderboard = [response_to_dict(b) for b in byte_leaderboard]
    return leaderboard
