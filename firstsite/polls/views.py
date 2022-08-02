from django.shortcuts import render
from django.http import Http404, HttpResponse, HttpResponseBadRequest
# Create your views here.

def index(request):
    return HttpResponse("Hello World, THIS IS MY PROJECT !!")

def officaltutor(request):
    return HttpResponse('<h1>這是Django官網的教學 !</h1>')

def test_error(anything):
    return HttpResponse(status=404)
