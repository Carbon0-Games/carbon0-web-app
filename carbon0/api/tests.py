from django.test import Client, TestCase
from django.test.client import RequestFactory
from django.urls import reverse

from carbon_quiz.tests import AchievementDetailTests
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
    
    def test_get_achievement_data(self):
        '''A request is made to the endpoint and a response is returned.'''
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)


class ProfileDataTests(AchievementDetailTests):
    '''Test suite for the ProfileData view.'''
    def setUp(self):
        '''Adds models to the db needed for testing environment.'''
        super().setUp()
        self.url = reverse('api:profile_data', args=[self.user.profile.id])

    def test_get_profile_data(self):
        '''A request is made to the endpoint and a response is returned.'''
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)


class QuizDataTests(AchievementDetailTests):
    '''Test suite for the QuizData view.'''
    def setUp(self):
        '''Adds models to the db needed for testing environment.'''
        super().setUp()
        self.url = reverse('api:quiz_data', args=[self.quiz.id])

    def test_get_quiz_data(self):
        '''A request is made to the endpoint and a response is returned.'''
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)


class QuizUpdateTests(AchievementDetailTests):
    pass
