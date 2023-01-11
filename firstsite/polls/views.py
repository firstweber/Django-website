from django.shortcuts import render
from django.http import Http404, HttpResponse, HttpResponseBadRequest
from django.template import loader

from .models import Question
# Create your views here.

#def index(request):
#    latest_question_list = Question.objects.order_by('-pub_date')[:5]
#    output = ', '.join([q.question_text for q in latest_question_list])
#    #return HttpResponse("Hello World, THIS IS MY PROJECT !!")
#    return HttpResponse(output)

# Using HttpResponse
#def index(request):
#    latest_question_list = Question.objects.order_by('-pub_date')[:5]
#    template = loader.get_template('polls/index.html')
#    context = {
#        'latest_question_list': latest_question_list,
#    }
#    return HttpResponse(template.render(context, request))

# Using shortcuts.render
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)


def officaltutor(request):
    return HttpResponse('<h1>這是Django官網的教學 !</h1>')

def test_error(anything):
    return HttpResponse(status=404)

def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)

def results(request, question_id):
    response = "You're looking at question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)