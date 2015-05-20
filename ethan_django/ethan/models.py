from django.db import models

# Create your models here.
class Game(models.Model):
    game_id = models.CharField(max_length=32)
    scores = models.CommaSeparatedIntegerField(max_length=30*4)  # array of scores integers
    turn_number = models.IntegerField() # number of turn that'll happen next
    player_turn = models.IntegerField()
    ethan_eyes = models.IntegerField()
    win_lose_ind = models.IntegerField() #0 nothing, -1 ethan wins, else player num win
    last_updated = models.DateTimeField() #date of last access
    die1 = models.IntegerField()
    die2 = models.IntegerField()
    created = models.DateTimeField() #date created

class Player(models.Model):
    game_id = models.CharField(max_length=32)
    player_num = models.IntegerField()
    player_name = models.CharField(max_length=40)

class Turn(models.Model):
    game_id = models.CharField(max_length=32)
    turn_num = models.IntegerField()
    turn_str = models.CharField(max_length=50)
