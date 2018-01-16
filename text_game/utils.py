from django.http import HttpResponseRedirect
from django.urls import reverse


def start_required(original_function):
    def new_function(request):
        if not request.session.get('game_started'):
            return HttpResponseRedirect(reverse('main'))
        return original_function(request)
    return new_function
