import datetime

from django.utils import timezone
from django.db import models

# Create your models here.


class Question(models.Model):
    """
    models of Question object that store question text as CharField and 
    published date as DateTimeField.
    Contain __str__ method for string representation.
    """
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self) -> str:
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now


class Choice(models.Model):
    """
    Model that have 2 fields: choice text(CharField) and vote tally(IntegerField).
    It also use ForeignKey of Question to access the question in database.
    Contain __str__ method for string representation.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.choice_text
