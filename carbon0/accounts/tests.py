from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.contrib.messages.storage.fallback import FallbackStorage
from django.test import Client, TestCase
from django.test.client import RequestFactory
from django.urls import reverse, reverse_lazy

from carbon_quiz.models.achievement import Achievement
from carbon_quiz.tests import AchievementDetailTests
from .views import (
    UserCreate,
    SettingsView
)


class UserCreateTests(AchievementDetailTests):
    '''Test suite for the UserCreate view.'''
    def setUp(self):
        '''Work to execute before each test case in this suite.'''
         # instantiate the db models that would be made before requests
        super().setUp()
        # test clients
        self.client = Client()
        self.factory = RequestFactory()
        # the view path
        self.url = reverse('accounts:signup')
        # a site visitor
        self.visitor = AnonymousUser()
        # add an achievement to the db, that has no User relationship
        self.achievement = Achievement.objects.create(
            mission=self.missions[2],
            quiz=self.quiz,
            zeron_image_url=settings.TRANSIT_ZERON_PATHS
        )
        self.achievement.save()
        return None

    def test_user_gets_signup(self):
        '''A User requests the sign up page and gets an HTML response.'''
        # user makes a request to GET the view
        response = self.client.get(self.url)
        # the response is returned OK
        self.assertEquals(response.status_code, 200)
        # the response has the appropiate content
        self.assertContains(response, "Sign up for more missions")
        return None

    def test_user_signs_up_no_achievement(self):
        """
        User signs up, not after earning an Achievement, 
        and creates a Profile.
        """
        # user sign up data
        form_data = {  
            'email': 'test@email.com',
            'username': 'test_user', 
            'password1': 'test_password123',
            'password2': 'test_password123'
        }
        # user makes the request 
        request = self.factory.post(self.url, form_data)
        request.user = self.visitor
        # supply the message to the request
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        # user gets the response
        response = UserCreate.as_view()(request)
        # user is redirected
        self.assertEquals(response.status_code, 302)
        # User object inserted in the db
        new_user = get_user_model().objects.get(username=form_data['username'])
        self.assertIsNot(new_user, None)
        return None

    def test_user_signs_up_after_achievement(self):
        """
        User signs up after earning an Achievement, 
        and creates a Profile that saves that Achievement.
        """
        # user sign up data
        form_data = {  
            'email': 'test@email.com',
            'username': 'test_user567', 
            'password1': 'test_password123',
            'password2': 'test_password123'
        }
        # user makes the request 
        url_after_achievement = (
            reverse(
                'accounts:signup',
                args=[self.achievement.secret_id])
        )
        request = self.factory.post(url_after_achievement, form_data)
        request.user = self.visitor
        # supply the message to the request
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        # user gets the response
        response = UserCreate.as_view()(
            request, self.achievement.secret_id
        )
        # user is redirected
        self.assertEquals(response.status_code, 302)
        # User object inserted in the db
        new_user = get_user_model().objects.get(username=form_data['username'])
        self.assertIsNot(new_user, None)
        # Achievement is attached to the new User's profile
        achievement = Achievement.objects.get(profile=new_user.profile)
        self.assertIsNot(achievement, None)
        return None


class SettingsViewTests(TestCase):
    '''Test suite for the SettingsView.'''
    pass
