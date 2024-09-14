"""Module for polls application view"""
import logging

from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from .models import Choice, Question, Vote

logger = logging.getLogger(__name__)


# Getting ip address from user(could be manipulated by request).
def get_client_ip(request):
    """Get the visitor’s IP address using request headers."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class IndexView(generic.ListView):
    """A generic view for index page.

    It show last 5 published polls question order by
    publication date.
    """
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")


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
            logger.warning("Attempted to access a closed poll.")
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

    Args:
        question_id : integre id of polls question
    """

    this_user = request.user
    question = get_object_or_404(Question, pk=question_id)

    user_ip = get_client_ip(request)

    logger.info(f"User {this_user.username} ({this_user.first_name} {this_user.last_name}) voted from IP {user_ip} on question {question_id}")

    if not question.can_vote():
        # prevent voting on end question
        logger.warning(f"User {this_user.username} tried to vote on a closed poll {question_id}")
        return HttpResponseRedirect(reverse("polls:index"))
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except(KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        logger.warning(f"User {this_user.username} failed to select a valid choice for question {question_id}")
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
        # save change to new vote or existing vote.
        vote.save()
        messages.success(request,
                         f'Your Vote for "{question.question_text}" have been updated to "{selected_choice.choice_text}".')
        logger.info(f"User {this_user.username} changed their vote for question {question_id} to '{selected_choice.choice_text}'")
    except Vote.DoesNotExist:
        vote = Vote(user=this_user, choice=selected_choice)
        messages.success(request, f"Vote for '{selected_choice.choice_text}' success.")
        logger.info(f"User have vote for {selected_choice.choice_text}")

    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))


def signup(request):
    """View for users registration page."""

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # get username field from the form data
            username = form.cleaned_data.get('username')
            # get password field from the form data
            raw_passwd = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_passwd)
            login(request, user)
            return redirect('polls:index')
    else:
        # create a user form and display it the signup page
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


@receiver(user_logged_in)
def log_login_event(sender, request, user, **kwargs):
    """
    Logs an info message when user login.

    Args:
        sender: Model class that send the signal.
        request: Http request object.
        user: User object
    """
    user_ip = get_client_ip(request)
    logger.info(f"User {user} logged in from {user_ip}")


@receiver(user_logged_out)
def log_logged_out_event(sender, request, user, **kwargs):
    """
    Logs an info message when a user logs out.

    Args:
        sender: Model class that send the signal.
        request: Http request object.
        user: User object
    """
    user_ip = get_client_ip(request)
    logger.info(f"User {user.username} logged out from {user_ip}")


@receiver(user_login_failed)
def log_login_failed_event(sender, credentials, request, **kwargs):
    """
    Logs a warning message when a login attempt fails.

    Args:
        sender: Model class that send the signal.
        credentials: Credentials given during failed login attempt.
        request: Http request object.
        user: User object
    """
    user_ip = get_client_ip(request)
    username = credentials.get('username', 'unknown')
    logger.warning(f"Failed login attempt for {username} from {user_ip}")
