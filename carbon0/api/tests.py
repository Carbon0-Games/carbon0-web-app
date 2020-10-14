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
    pass


class QuizDataTests(AchievementDetailTests):
    pass


class QuizUpdateTests(AchievementDetailTests):
    pass
