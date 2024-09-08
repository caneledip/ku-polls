"""Module for polls application view"""
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from .models import Choice, Question


class IndexView(generic.ListView):
    """A generic view for index page.
    
    It show last 5 published polls question order by
    publication date.
    """
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    """A generic view for poll detail page.
    
    Contain method for filtering only published question.
    """
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    """A view of results page."""
    model = Question
    template_name = "polls/results.html"


@login_required
def vote(request, question_id):
    """Method for vote feature of the poll app.
    
    If the question can not be vote, interaction will return
    user to index page. If poll is available, user can vote
    on poll's choice and submit it.
    """
    # comment or delete this part after developped
    user = request.user
    print("current user is: ", user.id, "login", user.username)
    print("Real name: ", user.first_name)
    question = get_object_or_404(Question, pk=question_id)

    if not question.can_vote():
        # prevent voting on end question
        return HttpResponseRedirect(reverse("polls:index"))
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except(KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice."
            },
        )

    selected_choice.votes = F("votes") + 1
    selected_choice.save()
    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
