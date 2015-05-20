from django.shortcuts import render
from django.http import HttpResponseRedirect
from ethan.models import Game, Player, Turn
from pprint import pprint
from uuid import uuid4
from datetime import datetime
from random import randint

def home_page(request):
    '''deals with the main page'''
    render_context = dict()
    if request.method == 'POST':
        ret_dict = _validate_options(request.POST)
        if ret_dict['player_count']:
            return _start_ethan(ret_dict)
        else:
            render_context['error_string'] = ret_dict['error_string']
    return render(request, 'home.html', render_context)

def _validate_options(post_dict):
    '''validates options for game creation'''
    ret_dict = dict()
    if 'ethan_eyes_chk' in post_dict:
        ret_dict['ethan_eyes'] = 1
    try:
        ret_dict['player_count'] = int(post_dict['num_players'])
    except:
        ret_dict['player_count'] = 99999999
    if ret_dict['player_count'] < 2 or ret_dict['player_count'] > 30:
        ret_dict['player_count'] = 0
        ret_dict['error_string'] = 'Please enter a number in the range 2-30'
    return ret_dict

def _start_ethan(ret_dict):
    '''initializes the game internals before redirecting to game page'''
    # make use of model and create game internals
    game_uuid = _create_game(ret_dict)
    _create_players(ret_dict, game_uuid) 
    # redirect to page
    return HttpResponseRedirect('/game/%s' % (game_uuid))

def _create_game(ret_dict):
    '''creates game object'''
    ethan_eyes = 0
    if 'ethan_eyes' in ret_dict:
        ethan_eyes = 1
    game_obj = Game(game_id = uuid4().hex, \
                    scores = ','.join(['5'] * ret_dict['player_count']), \
                    turn_number = 1, \
                    player_turn = 0, \
                    ethan_eyes = ethan_eyes, \
                    win_lose_ind = 0, \
                    last_updated = datetime.now(), \
                    die1 = 2, \
                    die2 = 2, \
                    created = datetime.now())
    game_obj.save()
    return game_obj.game_id

def _create_players(ret_dict, game_id):
    '''creates player objects'''
    for ind in range(ret_dict['player_count']):
        player = Player(game_id = game_id, \
                        player_num = ind, \
                        player_name = '')
        player.save()
    return

def game_page(request):
    '''deals with the game pages after creation'''
    game_id = request.path_info.split('/')[-1]
    if request.method == 'POST':
        _do_a_turn(game_id, request)
    render_context = _form_render_context(game_id)
    return render(request, 'game.html', render_context) 

def _do_a_turn(game_id, request):
    game = Game.objects.filter(game_id = game_id)[0]
    players = Player.objects.filter(game_id = game_id)
    for player in players:
        player.player_name = request.POST['player%d' % getattr(player,'player_num')]
        player.save()
        if player.player_num == game.player_turn:
            player_name = player.player_name
            if player_name.isspace():
                player_name = 'player%d' % player.player_num
    game.die1 = randint(1,6)
    game.die2 = randint(1,6)
    total = game.die1 + game.die2
    new_turn = Turn(game_id = game_id, \
                    turn_num = game.turn_number, \
                    turn_str = '')
    turn_str = '%s rolled a %d ,' % (player_name, total)
    scores = [int(i) for i in game.scores.split(',')]
    if total == 4:
        ethan = 5*len(players) - sum(scores)
        scores[game.player_turn] = scores[game.player_turn] + ethan
        turn_str = '%s robs Ethan of %d chips.' % (turn_str, ethan)
    elif total == 2 and game.ethan_eyes:
        scores[game.player_turn] = 0
        turn_str = '%s gets Ethan Eyes and loses all chips.' % (turn_str)
    else:
        scores[game.player_turn] = scores[game.player_turn] - 1
        turn_str = '%s loses 1 chip.' % (turn_str)
    ethan = 5*len(players) - sum(scores)
    if sum(scores) == 0:
        game.win_lose_ind = -1
    elif scores[game.player_turn] > ethan and scores[game.player_turn] == sum(scores):
        game.win_lose_ind = game.player_turn
    else:
        while(True):
            game.player_turn = (game.player_turn + 1) % len(players)
            if scores[game.player_turn]:
                break
    game.scores = ','.join([str(i) for i in scores])
    game.turn_number = game.turn_number + 1
    game.save()
    new_turn.turn_str = turn_str
    new_turn.save()
    return

def _form_render_context(game_id):
    '''forms dict for use in rendering game page'''
    render_context = dict()
    game = Game.objects.filter(game_id = game_id)[0]
    render_context['game_id'] = game_id
    scores = [int(i) for i in game.scores.split(',')]
    render_context['ethan_count'] = 5*len(scores) - sum(scores)
    render_context['die1'] = game.die1
    render_context['die2'] = game.die2
    render_context['player_turn'] = game.player_turn    
    players = Player.objects.filter(game_id = game_id)
    players = sorted(players, key=lambda player: player.player_num)
    player_dict_list = list()
    for player in players:
        player_dict = dict()
        player_dict['name'] = player.player_name
        player_dict['num'] = player.player_num
        player_dict['score'] = scores[player.player_num]
        player_dict_list.append(player_dict)
    render_context['players'] = player_dict_list
    
    turns = Turn.objects.filter(game_id = game_id)
    turns = sorted(turns, key=lambda turn: turn.turn_num, reverse=True)
    render_context['turns'] = [i.turn_str for i in turns]

    if game.win_lose_ind < 0:
        render_context['end_msg'] = 'EVERYBODY LOSES. AE2015.'
    elif game.win_lose_ind > 0:
        winner_name = players[game.win_lose_ind].player_name
        render_context['end_msg'] = 'HOORAY %s WON, ETHAN LOSES.' % (winner_name)
    return render_context

