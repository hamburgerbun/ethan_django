from django.shortcuts import render
from django.http import HttpResponseRedirect
from ethan.models import Game, Player, Turn
from pprint import pprint
from uuid import uuid4
from datetime import datetime

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
    game_obj = Game(game_id = uuid4().hex, \
                    scores = ','.join(['5'] * ret_dict['player_count']), \
                    turn_number = 1, \
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
    pass

def _form_render_context(game_id):
    '''forms dict for use in rendering game page'''
    render_context = dict()
    game = Game.objects.filter(game_id = game_id)[0]
    render_context['game_id'] = game_id
    scores = [int(i) for i in game.scores.split(',')]
    render_context['ethan_count'] = 5*len(scores) - sum(scores)
    render_context['die1'] = game.die1
    render_context['die2'] = game.die2
    
    players = Player.objects.filter(game_id = game_id)
    players = sorted(players, key=lambda player: player.player_num)
    player_dict_list = list()
    for player in players:
        player_dict = dict()
        player_dict['name'] = player.player_name
        player_dict['num'] = player.player_num
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

