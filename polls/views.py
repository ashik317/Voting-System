from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from .models import Question, Choice
from django.template import loader

#Get question and display them.
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    return render(
        request,
        'polls/index.html',
        {
            'latest_question_list': latest_question_list
        }
    )

#Show specific question and answer
def detail(request, question_id):
    try:
        question = get_object_or_404(Question, pk=question_id)

    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(
        request,
        'polls/detail.html',
        {
            'question': question
        }
    )

#Get Question and specific result.
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(
        request,
        'polls/result.html',
        {
            'question': question
        }
    )
#Vote for question choice.
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        return render(
            request,
            'polls/detail.html',
            {
                'question': question,
            }
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


