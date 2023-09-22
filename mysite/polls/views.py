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
    question = get_object_or_404(Question, pk=question_id)
    user = request.user
    if not user.is_authenticated:
       return redirect('login')
    try:
        selected_choice = question.choice_set.get(pk = request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question, 'error_message': "You didn't select a choice.",
            })
        # selected_choice.votes+=1
        # selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing with POST data.
        # This prevents data from being posted twice if a user hits the Back button
    this_user = request.user
    try:
        vote = Vote.objects.get(user=this_user, choice=selected_choice)
        vote_choice = selected_choice
    except:
        vote = Vote(user=this_user, choice=selected_choice)

    vote.save()
    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
