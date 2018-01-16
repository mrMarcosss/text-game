import json

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse

from text_game.utils import start_required


def main_page(request):
    request.session['coffee'] = 0
    request.session['game_started'] = False
    return render(request, 'levels/main.html')


def start(request):
    request.session['rating'] = 0
    request.session['game_started'] = True
    return render(request, 'levels/start.html')


def choose_gender(request):
    if request.method == 'POST':
        if request.POST.get('gender'):
            request.session['gender'] = int(request.POST.get('gender'))
            return HttpResponseRedirect(reverse('start'))
    return render(request, 'levels/choose_gender.html')


@start_required
def make_research(request):
    if 'rating' in request.session:
        request.session['rating'] = 25
    return render(request, 'levels/make_research.html')


@start_required
def response_from_companies(request):
    if 'rating' in request.session:
        request.session['rating'] = 75
    return render(request, 'levels/response_from_companies.html')


@start_required
def choose_company(request):
    request.session['game_started'] = False
    if request.method == 'POST':
        company = request.POST.get('company')
        try:
            company = int(company)
            if company == 2:
                request.session['rating'] = 100
                context = {'status': 'win'}
            elif company == 1:
                context = {'status': 'not so bad'}
            elif company == 4:
                context = {'status': 'send-cv'}
            else:
                context = {'status': 'lose'}
            if 'rating' in request.session:
                del request.session['rating']
            context['name'] = 'Melisa' if request.session['gender'] else 'Roberto'
            data = {'html': render_to_string('levels/you_win.html', context=context), **context}
            return HttpResponse(json.dumps(data))
        except ValueError:
            return HttpResponse(json.dumps({'error': 'Company value must be a number!'}))


@start_required
def recruiter(request):
    if 'rating' in request.session:
        request.session['rating'] = 20
    return render(request, 'levels/recruiter.html')


@start_required
def stay_in_company(request):
    if 'rating' in request.session:
        request.session['rating'] = 10
    return render(request, 'levels/stay_in_company.html')


def drink_coffee(request):
    coffee = request.session.get('coffee')
    if request.method == 'GET':
        return HttpResponse(json.dumps({'cups': coffee}))
    if request.method == 'POST':
        if 'coffee' in request.session:
            request.session['coffee'] += 1
            return HttpResponse(json.dumps({'cups': request.session['coffee']}))
