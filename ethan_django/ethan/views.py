from django.shortcuts import render

def home_page(request):
    '''deals with the main page'''
    render_context = dict()
    if request.method == 'POST':
        ret_dict = _validate_options(request)
        if ret_dict['its_good']:
            return _start_ethan(ret_dict)
        else:
            render_context['error_string'] = ret_dict['error_string']
    return render(request, 'home.html', render_context)

def _validate_options(request):
    '''validates options for game creation'''
    ret_dict = dict()
    ret_dict['its_good'] = 0
    ret_dict['error_string'] = 'i broke it on purpose to test it'
    return ret_dict

def game_page(request):
    '''deals with the game pages after creation'''
    pass
