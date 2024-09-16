"""Model of Poll application for ku-polls project."""
import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Question(models.Model):
    """Question contain text of the question and it published date."""

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published", default=timezone.now)
    end_date = models.DateTimeField("date poll ended", default=None,
                                    blank=True, null=True)

    def __str__(self) -> str:
        """Return question text of Question object."""
        return str(self.question_text)

    def was_published_recently(self):
        """If question published date was recent, return True."""
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def is_published(self):
        """Give the state of polls question.

        Return True if the current date-time is on
        or after question's publication date.
        """
        return self.pub_date <= timezone.now()

    def can_vote(self):
        """Poll can be vote if it currently in between published and end date."""
        if self.end_date is None:
            return self.pub_date <= timezone.now()
        return self.pub_date <= timezone.now() <= self.end_date


class Choice(models.Model):
    """
    Choice model for database table.

    Contain Question as ForeignKey, choice text
    and the vote count that have been vote on the chioce.
    """

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)

    def __str__(self) -> str:
        """Return choice text of the choice."""
        return str(self.choice_text)

    @property
    def votes(self):
        """Return vote count for this choice."""
        return self.vote_set.count()


class Vote(models.Model):
    """Record a choice for a question made by a user."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    def __str__(self) -> str:
        """Show vote's owner and choice text user vote for in sentence."""
        return f'Vote by {self.user.username} for {self.choice.choice_text}'
