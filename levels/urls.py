from django.conf.urls import url

from levels.views import main_page, start, make_research, response_from_companies, choose_company, recruiter, \
    stay_in_company, choose_gender, drink_coffee

urlpatterns = [
    url(r'^$', main_page, name='main'),
    url(r'^start/$', start, name='start'),
    url(r'^choose-gender/$', choose_gender, name='choose_gender'),
    url(r'^make-research/$', make_research, name='make_research'),
    url(r'^response-from-companies/$', response_from_companies, name='response_from_companies'),
    url(r'^choose-company/$', choose_company, name='choose_company'),
    url(r'^recruiter/$', recruiter, name='recruiter'),
    url(r'^stay-in-company/$', stay_in_company, name='stay_in_company'),
    url(r'^cup-of-coffee/$', drink_coffee, name='drink_coffee'),
]
