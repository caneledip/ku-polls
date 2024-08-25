"""Model of Poll application for ku-polls project."""
import datetime

from django.db import models
from django.utils import timezone


class Question(models.Model):
    """
    Question model. Contain text of the question and it published date.
    """
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    def __str__(self) -> str:
        """Return question text of Question object"""
        return str(self.question_text)

    def was_published_recently(self):
        """If question published date was recent, return True."""
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now


class Choice(models.Model):
    """
    Choice model. Contain Question as ForeignKey, choice text
    and the vote count that have been vote on the chioce.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self) -> str:
        """Return choice text of the choice"""
        return str(self.choice_text)
