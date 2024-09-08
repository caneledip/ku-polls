"""Module for polls application view"""
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render,redirect
from django.urls import reverse
from django.utils import timezone
from django.views import generic
from django.contrib import messages

from .models import Choice, Question, Vote


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
    
    def get(self, request, *args, **kwargs):
        question = self.get_object()

        # Can you vote on this question?
        if not question.can_vote():
            messages.error(request, "Voting is not allowed for this question.")
            return redirect('polls:index')

        # Check for User vote on this question.
        user_vote = None
        if request.user.is_authenticated:
            user_vote = Vote.objects.filter(user=request.user, choice__question=question).first()

        return render(request, self.template_name, {
            'question': question,
            'previous_vote': user_vote,  # Pass the user's previous vote to the template
        })


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

    this_user = request.user
    print("current user is: ", this_user.id, "login", this_user.username)
    print("Real name: ", this_user.first_name)
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

    try:
        # find a vote of this user for this question.
        vote = Vote.objects.get(user=this_user, choice__question=question)
        vote.choice = selected_choice
        messages.success(request, f'Your Vote for "{question.question_text}" have been updated to "{selected_choice.choice_text}".')
    except Vote.DoesNotExist:
        vote = Vote(user=this_user, choice=selected_choice)
        messages.success(request,f"Vote for '{selected_choice.choice_text}' success.")

    # save change to new vote or existing vote.
    vote.save()
    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
