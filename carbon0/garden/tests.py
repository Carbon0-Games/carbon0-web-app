from django.test import Client, TestCase
from django.urls import reverse
from .views import (
    PlantList
)


class PlantListTests(TestCase):
    def setUp(self) -> None:
        '''Initializes attributes used across all tests in this suite.'''
        self.client = Client()
        self.url = reverse("garden:plant_list")

    def test_get_list_page(self):
        '''A user requests the PlantList view and gets a valid response.'''
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
