from django.shortcuts import render
from django.http import Http404, HttpResponse

# Create your views here.

# def index(request):
    # return HttpResponse('<h1> this is AnnSystem </h1>')

def index(request):
    context = {'message' : "hello"}
    return render(request, 'AnnounceSystem/index.html', context)

def test_error(request):
    return HttpResponse(status=404)