from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.test.client import RequestFactory
from django.urls import reverse

from accounts.models.profile import Profile
from .models.plant import Plant
from .views import (
    PersonalPlantList,
    PlantDetail,
)


class PersonalPlantListTests(TestCase):
    def setUp(self) -> None:
        """Initializes attributes used across all tests in this suite."""
        self.client = Client()
        self.factory = RequestFactory()
        self.url = reverse("garden:plant_list")
        self.user = get_user_model().objects.create_user(
            "testing_user456",  # username
            "test@email.com",  # email
            "carbon0_ftw123",  # password
        )

    def test_get_list_page_authenticated(self):
        """A user requests the PersonalPlantList view and gets a valid response."""
        # the authenticated user makes a request
        request = self.factory.get(self.url)
        request.user = self.user
        # user gets a valid response
        response = PersonalPlantList.as_view()(request)
        self.assertEquals(response.status_code, 200)

    def test_get_list_page_unauthenticated(self):
        """A visitor requests the PersonalPlantList view and gets a valid response."""
        # the visitor is not logged in
        response = self.client.get(self.url)
        # so they are redirected to the login page
        self.assertEquals(response.status_code, 302)


class PlantDetailTests(TestCase):
    def setUp(self) -> None:
        """Initializes attributes used across all tests in this suite."""
        self.factory = RequestFactory()
        self.url_path_name = "garden:plant_detail"
        self.user = get_user_model().objects.create_user(
            "testing_user456",  # username
            "test@email.com",  # email
            "carbon0_ftw123",  # password
        )
        # make a profile for the user
        self.profile = Profile.objects.create(user=self.user)
        self.profile.save()
        # make a plant for the user
        self.plant = Plant.objects.create(
            nickname="Desk Plant", common_name="Rose", profile=self.user.profile
        )
        self.plant.save()  # gives the Plant a slug

    def test_get_detail_page_authenticated(self):
        """A user requests their plant details and gets a valid response."""
        # the authenticated user makes a request
        url_full = reverse(self.url_path_name, args=[self.plant.slug])
        request = self.factory.get(url_full)
        request.user = self.user
        # user gets a valid response
        response = PlantDetail.as_view()(request, slug=self.plant.slug)
        self.assertEquals(response.status_code, 200)
