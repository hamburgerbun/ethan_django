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
    pprint(post_dict)
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
    game_obj = Game(game_id = uuid4().hex, \
                    scores = ','.join(['5'] * ret_dict['player_count']), \
                    turn_number = 1, \
                    win_lose_ind = 0, \
                    last_updated = datetime.now(), \
                    created = datetime.now())
    game_obj.save()
    return game_obj.game_id

def _create_players(ret_dict, game_id):
    for ind in range(ret_dict['player_count']):
        player = Player(game_id = game_id, \
                        player_num = ind, \
                        player_name = '')
        player.save()
    return

def game_page(request):
    '''deals with the game pages after creation'''
    ret_dict = dict()
    if request.method == 'POST':
        # increment turn
        ret_dict = _do_a_turn()
    render_context = _form_render_context(ret_dict)
    return render(request, 'game.html', render_context) 

def _do_a_turn():
    pass

def _form_render_context(ret_dict):
    render_context = dict()
    render_context['game_id'] = 'abcd'
    render_context['ethan_count'] = 5
    render_context['die1'] = 2
    render_context['die2'] = 2
    return render_context
