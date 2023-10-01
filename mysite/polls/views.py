from typing import Any
from django.db import models
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import Question, Choice, Vote
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions(not including those set to be published in the future)."""
        return Question.objects.filter(pub_date__lte = timezone.now()).order_by('-pub_date')[:5]
    
class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    
    def get_queryset(self) -> QuerySet[Any]:
        return Question.objects.filter(pub_date__lte = timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

@login_required
def vote(request, question_id):
    """ Get a question and vote for the choice"""
    question = get_object_or_404(Question, pk=question_id)
    user = request.user
    try:
        selected_choice = question.choice_set.get(pk = request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question, 'error_message': "You didn't select a choice.",
            })
    
    vote = Vote.get_vote(question=question, user=user)
    if vote:
        vote.choice = selected_choice
        messages.success(request, 'Vote updated')
    else:
        vote = Vote(user=user, choice=selected_choice)
        messages.success(request, 'Vote success')
    vote.save()
    next_url = request.POST.get('next', reverse('polls:results', args=(question.id,)))
    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
