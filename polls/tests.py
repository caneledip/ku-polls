import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question


def create_question(question_text, days):
    """
    Create a question with the given 'question_text' and published the given number of 'days'
    offset to now (negative for question published in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

def create_choice(Question, vote=0):
    """
    Create a choice for question with given choice_text
    """
    choice = Question.choice_set.create(choice_text="Choice 1", votes=vote)
    return choice


class QuestionModelTests(TestCase):
    """
    Model testing class for Question.
    Test on was_published_recently method.
    """
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for question whose pub_date is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date = time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question_after_1_day(self):
        """
        was_published_recently() returns False for questions whose pub_date is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question_within_q_day(self):
        """
        was_published_recently() returns True for questions whose pub_date is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


class QuestionIndexViewTests(TestCase):
    """
    Test on Index page displaying the correct polls.
    """
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question2, question1],
        )


class QuestionDetailViewTests(TestCase):
    """
    Test on detail page showing correct poll question detail, and not showing future poll.
    """
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future returns a 404 not found.
        """
        future_question = create_question(question_text="Future question.", days=5)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past displays the question's text.
        """
        past_question = create_question(question_text="Past question.", days=-5)
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)


class QuestionResultsTest(TestCase):
    """
    Test result page show correct vote result and can vote again.
    """
    def test_result_from_voted_question(self):
        """
        The results view of a question that have been voted on is display
        """
        question = create_question("Question", days=0)
        choice1 = create_choice(question, 2)
        choice2 = create_choice(question, 4)

        response = self.client.get(reverse("polls:results", args=(question.id,)))
        self.assertContains(response, f"{choice1.choice_text}")
        self.assertContains(response, f"{choice1.votes}")
        self.assertEqual(choice1.votes, 2)
        self.assertContains(response, f"{choice2.choice_text}")
        self.assertContains(response, f"{choice2.votes}")
        self.assertEqual(choice2.votes, 4)


class VoteTests(TestCase):
    """
    Test of vote feature. Vote increase after being vote, vote redirect to result page after voting,
    vote without selected choice don't go through.
    """
    def test_vote_choice(self):
        """
        Test if the votes increase after user vote for that choice.
        """
        question = create_question("Question", days=0)
        choice1 = create_choice(question)
        
        # Simulate voting on the choice1
        response = self.client.post(
            reverse("polls:vote", args=(question.id,)),
            {"choice": choice1.id}
        )

        # Check if the vote was incremented
        choice1.refresh_from_db()
        self.assertEqual(choice1.votes, 1)

    def test_vote_redirect(self):
        """
        Ensure that you are redirect to results page after voting.
        """
        question = create_question("Question", days=0)
        choice1 = create_choice(question)

        # Simulate voting on the choice1
        response = self.client.post(
            reverse("polls:vote", args=(question.id,)),
            {"choice": choice1.id}
        )

        # Check if it redirects to the results page
        self.assertRedirects(response, reverse("polls:results", args=(question.id,)))

    def test_vote_without_selecting_choice(self):
        """
        Ensure that submitting the vote form without selecting a choice
        redisplays the question form with an appropriate error message.
        """
        # Create a sample question and choices
        question = create_question("Sample Question", days=0)
        choice1 = create_choice(question)
        choice2 = create_choice(question)

        # Simulate submitting an empty choice
        response = self.client.post(
            reverse("polls:vote", args=(question.id,)),  # Use the correct URL for voting
            {}  # No choice selected
        )

        # Check that the form is redisplayed with an error message
        self.assertEqual(response.status_code, 200)  # Ensure status code is 200 OK
        # check contain from &#x27; (html encoding of "'")
        self.assertContains(response, "You didn&#x27;t select a choice.")
        self.assertTemplateUsed(response, "polls/detail.html")


class QuestionIsPublished(TestCase):
    """
    Test is_published method in Question Model.
    
    is_published should return True if question was published on or before
    current time, and should return False if question pub_date is in the
    future.
    """
    def test_is_published_on_published_question(self):
        """Test is_published method on published question."""
        question = create_question("Published Question", days=-1)
        self.assertTrue(question.is_published())

    def test_is_published_on_unpublished_question(self):
        """Test is_published method on unpublished question."""
        question = create_question("Unpublished Question", days=10)
        self.assertFalse(question.is_published())

    def test_is_published_on_recently_published_question(self):
        """Test is_published method on unpublished question."""
        question = create_question("Unpublished Question", days=0)
        self.assertTrue(question.is_published())


class TestCanVote(TestCase):
    """Test can_vote to check polls availability.
    
    can_vote return True when the poll is published and it is
    not end, and should return False if it is not in voting
    period."""
    def test_can_vote_on_available_poll(self):
        """Test can_vote on poll that is available for vote."""
        question = create_question("Available question", days=-2)
        self.assertTrue(question.can_vote())

    def test_can_vote_on_unavailable_poll(self):
        """Test can_vote on poll that is not available for vote."""
        question = create_question("Unavailable question", days=2)
        self.assertFalse(question.can_vote())

    def test_can_vote_on_ending_poll(self):
        """Test can_vote on poll that is already over."""
        question = create_question("End question", days=-5)
        question.end_date = timezone.now()-datetime.timedelta(days=1)
        self.assertFalse(question.can_vote())
