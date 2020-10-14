from django.test import Client, TestCase
from django.test.client import RequestFactory
from django.urls import reverse

from carbon_quiz.models.quiz import Quiz
from carbon_quiz.tests import (
    AchievementDetailTests,
    DatabaseSetup,
    QuizDetailTests
)
from .views import (
    AchievementData,
    ProfileData,
    QuizData,
    QuizUpdate,
)


class AchievementDataTests(AchievementDetailTests):
    '''Test suite for the AchievementData view.'''
    def setUp(self):
        '''Adds models to the db needed for testing environment.'''
        super().setUp()
        self.url = reverse('api:achievement_data', args=[self.achievement_user.id])
        return None
    
    def test_get_achievement_data(self):
        '''A request is made to the endpoint and a response is returned.'''
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        return None

class ProfileDataTests(AchievementDetailTests):
    '''Test suite for the ProfileData view.'''
    def setUp(self):
        '''Adds models to the db needed for testing environment.'''
        super().setUp()
        self.url = reverse('api:profile_data', args=[self.user.profile.id])
        return None

    def test_get_profile_data(self):
        '''A request is made to the endpoint and a response is returned.'''
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        return None


class QuizDataTests(AchievementDetailTests):
    '''Test suite for the QuizData view.'''
    def setUp(self):
        '''Adds models to the db needed for testing environment.'''
        super().setUp()
        self.url = reverse('api:quiz_data', args=[self.quiz.id])
        return None

    def test_get_quiz_data(self):
        '''A request is made to the endpoint and a response is returned.'''
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        return None


class QuizUpdateTests(QuizDetailTests):
    '''Test suite for the QuizUpdate view.'''
    def setUp(self):
        '''Adds models to the db needed for testing environment.'''
        super().setUp()
        return None

    def test_update_quiz_yes(self):
        '''A user answers yes to a Question on the Quiz.'''
        # form the request url
        yes_url = reverse(
            'api:quiz_update',
            args=[self.quiz.slug, 1]  # 1 = yes
        )
        # store the active_question value before the update
        question_index_before = self.quiz.active_question
        # make the request to the API
        response = self.client.post(yes_url)
        # the user is redirected
        self.assertEquals(response.status_code, 302)
        # the value of active_question has increased
        quiz = Quiz.objects.get(slug=self.quiz.slug)
        self.assertEqual(quiz.active_question, question_index_before + 1)
        # the previous Question id in the array is now ignored
        self.assertEqual(quiz.questions[question_index_before], 0)
        return None

    def test_update_quiz_no(self):
        '''A user answers no to a Question on the Quiz.'''
        # form the request url
        no_url = reverse(
            'api:quiz_update',
            args=[self.quiz.slug, 0]  # 0 = no
        )
        # store the active_question value before the update
        question_index_before = self.quiz.active_question
        # store the value at that index, to check if it remains at the end
        question_id = self.quiz.get_current_question().id
        # make the request to the API
        response = self.client.post(no_url)
        # the user is redirected
        self.assertEquals(response.status_code, 302)
        # the value of active_question has increased
        quiz = Quiz.objects.get(slug=self.quiz.slug)
        self.assertEqual(quiz.active_question, question_index_before + 1)
        # the previous Question id in the array is the same
        self.assertEqual(quiz.questions[question_index_before], question_id)
        return None
