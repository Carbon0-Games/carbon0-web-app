from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.test.client import RequestFactory
from django.urls import reverse

from .views import (
    PersonalPlantList
)


class PlantListTests(TestCase):
    def setUp(self) -> None:
        '''Initializes attributes used across all tests in this suite.'''
        self.client = Client()
        self.factory = RequestFactory()
        self.url = reverse("garden:plant_list")
        self.user = get_user_model().objects.create_user(
            "testing_user456",  # username
            "test@email.com",  # email
            "carbon0_ftw123",  # password
        )

    def test_get_list_page_authenticated(self):
        '''A user requests the PersonalPlantList view and gets a valid response.'''
        # the authenticated user makes a request
        request = self.factory.get(self.url)
        request.user = self.user
        # user gets a valid response
        response = PersonalPlantList.as_view()(request)
        self.assertEquals(response.status_code, 200)

    def test_get_list_page_unauthenticated(self):
        '''A visitor requests the PersonalPlantList view and gets a valid response.'''
        # the visitor is not logged in
        response = self.client.get(self.url)
        # so they are redirected to the login page
        self.assertEquals(response.status_code, 302)
