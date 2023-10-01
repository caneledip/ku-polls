import datetime
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Question(models.Model):
    """
    models of Question object that store question text as CharField and 
    published date as DateTimeField.
    Contain __str__ method for string representation.
    """
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', default=timezone.now)
    end_date = models.DateTimeField('date ended', default=None, blank=True, null=True)

    def __str__(self) -> str:
        return self.question_text

    def was_published_recently(self):
        """Method return boolean, either the question published within a day or not"""
        now = timezone.now()
        return now - datetime.timedelta(hours=23, minutes=59, seconds=59) <= self.pub_date <= now
    
    def can_vote(self):
        """Method return true if you can vote on poll question."""
        now = timezone.now()
        if self.is_published():
            if self.end_date is None:
                return True
            else:
                return now <= self.end_date
        else:
            return False

    def is_published(self):
        """Method return true if question was published on or after current date and time."""
        now = timezone.now()
        return now >= self.pub_date


class Choice(models.Model):
    """
    Model that have 2 fields: choice text(CharField) and vote tally(IntegerField).
    It also use ForeignKey of Question to access the question in database.
    Contain __str__ method for string representation.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)

    @property
    def votes(self):
        """ Count the vote of this choice and return the number."""
        return self.vote_set.count()

    def __str__(self) -> str:
        return self.choice_text

class Vote(models.Model):
    """ Records a Vote of a Choice by a User. """
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
        
    def __str__(self):
        return f'Vote by {self.user.username} for {self.choice.choice_text}'
        