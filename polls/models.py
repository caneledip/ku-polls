import datetime

from django.db import models
from django.utils import timezone


class Question(models.Model):
    """
        Create a polls question that contain pub_date, end_date, is_published method
        and was_published_recently method.
    """
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    end_date = models.DateTimeField('end date', null=True)

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return timezone.now() - datetime.timedelta(days=3) <= self.pub_date <= timezone.now()

    def is_published(self):
        return timezone.now() >= self.pub_date

    def can_vote(self):
        if self.end_date:
            return self.end_date + datetime.timedelta(seconds=1) >= timezone.now() >= self.pub_date
        return self.is_published()


class Choice(models.Model):
    """
    Create a Choice that contain choice_text and vote tally.
    Every vote belongs to each poll question.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
