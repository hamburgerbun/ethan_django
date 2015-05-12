from django.shortcuts import render
from django.http import HttpResponseRedirect
from pprint import pprint

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
    # redirect to page
    return HttpResponseRedirect('/game/abcd')

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
