from django.test import Client, TestCase
from django.test.client import RequestFactory
from django.urls import reverse

from carbon0.views import get_landing


class LandingPageTests(TestCase):
    '''Tests for the landing page view.'''
    def setUp(self):
        '''Initial work done for each test in this suite.'''
        self.client = Client()
        self.url = 'landing_page'

    def test_get_landing(self):
        '''User views the landing page and gets a HTTP 200 response.'''
        # the response is returned successfully 
        response = self.client.get(reverse(self.url))
        self.assertEqual(response.status_code, 200)

        # TODO Henry: uncomment the tests for content on the landing page
        # self.assertContains(response, "Log In")
        # self.assertContains(response, "Sign Up")
