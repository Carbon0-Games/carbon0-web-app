from django.test import Client, TestCase
from django.test.client import RequestFactory
from django.urls import reverse


# Create your tests here.
# TODO Cao: write tests for the views (to be implemented by Zain)
class QuizCreateTests(TestCase):
    '''Tests for the landing page view.'''
    def setUp(self):
        '''Initial work done for each test in this suite.'''
        self.client = Client()
        self.view_pattern = 'carbon_quiz:quiz_create'

    def test_get_landing(self):
        '''User views the landing page and gets a HTTP 200 response.'''
        # the response is returned successfully 
        response = self.client.get(reverse(self.view_pattern))
        self.assertEqual(response.status_code, 200)

        # TODO Henry: uncomment the tests for content on the landing page
        # self.assertContains(response, "Log In")
        # self.assertContains(response, "Sign Up")