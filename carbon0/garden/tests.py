from io import BytesIO
import os
from pathlib import Path

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.test.client import RequestFactory
from django.urls import reverse

from accounts.models.profile import Profile
from carbon_quiz.models.question import Question
from .models.leaf import Leaf
from .models.ml import MachineLearning
from .models.plant import Plant
from django.conf import settings
from .views import (
    LeafCreate,
    PlantCreate,
    PersonalPlantList,
    PlantDetail,
)


class LeafCreateTests(TestCase):
    def setUp(self) -> None:
        """Initializes attributes used in this suite."""
        self.client = Client()
        self.factory = RequestFactory()
        self.user = get_user_model().objects.create_user(
            "testing_user687",  # username
            "test@email.com",  # email
            "carbon0_ftw153",  # password
        )
        # make a profile for the user
        self.profile = Profile.objects.create(user=self.user)
        self.profile.save()
        # make a plant for the user
        self.plant = Plant.objects.create(
            nickname="Desk Plant", common_name="Rose", profile=self.user.profile
        )
        self.plant.save()  # gives the Plant a slug
        self.url = reverse("garden:leaf_create", args=[self.plant.id])
        self.cnn = MachineLearning.objects.create(purpose="V")
        self.cnn.save()

    def test_get_create_form(self):
        """A user visits the LeafCreate form and gets a response."""
        # user visits the page
        request = self.factory.get(self.url)
        request.user = self.user
        # the response is returned ok
        response = LeafCreate.as_view()(request, plant_id=self.plant.id)
        self.assertEqual(response.status_code, 200)

    def test_user_posts_new_leaf(self):
        """A user submits the form to add a new Leaf to the db.

        NOTE for developers using LOCAL settings: In this is test case
        we use the test client (django.test.client.Client)
        to mock a user uploading a file when they submit the form.

        This was done only so that your file system doesn't need to save a
        new image every time the new Leaf object is inserted into the
        test database.

        However, be warned that this test case DOES NOT actually insert a new
        Leaf model into the db. So please make another test function in case
        you want to test things that depend on the Leaf model actually being
        in the test database (e.g. if it's related to the correct Plant after
        saving).
        """
        # authenticate the request
        self.client.login(username=self.user.username, password=self.user.password)
        # init a test image
        mock_image_path = (
            Path(__file__).resolve().parent / "static/garden/images/AppleCedarRust1.jpg"
        )
        mock_image = SimpleUploadedFile(
            name="test_image.jpg",
            content=open(mock_image_path, "rb").read(),
            content_type="image/jpeg",
        )
        # user submits the form, and is redirected
        form_data = {"image": mock_image}
        response = self.client.post(self.url, form_data)
        self.assertEqual(response.status_code, 302)


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


class PlantCreateTests(TestCase):
    def setUp(self) -> None:
        """Initializes attributes used commonly in this test suite."""
        self.factory = RequestFactory()
        self.url = reverse("garden:plant_create")
        self.user = get_user_model().objects.create_user(
            "testing_user123",  # username
            "test@email.com",  # email
            "carbon0_ftw456",  # password
        )
        # make a profile for the user
        self.profile = Profile.objects.create(user=self.user)
        self.profile.save()
        # Save a question for making an associated Mission for the Plant
        question = Question.objects.create(
            question_text="Do you take care of any garden plants?",
            question_info="A 2016 UC ANR study found that...",
            carbon_value=0,
            category="D",
            is_quiz_question=False
        )
        question.save()

    def test_get_create_form(self):
        """A user visits the PlantCreate form and gets a response."""
        # user visits the page
        request = self.factory.get(self.url)
        request.user = self.user
        # the response is returned ok
        response = PlantCreate.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_user_posts_new_plant(self):
        """A user submits the form to add a new Plant to the db."""
        # user fills out the form
        form_data = {
            "nickname": "Desk Plant",
            "common_name": "Rose",
            "is_edible": True,
            "description": "Doing all right at the moment!",
        }
        # store the number of Plant objects now - use this later
        num_plants_before = len(Plant.objects.all())
        # user submits the form
        request = self.factory.post(self.url, form_data)
        request.user = self.user
        # user is redirected
        response = PlantCreate.as_view()(request)
        self.assertEqual(response.status_code, 302)
        # a new Plant object is in the db
        num_plants_after = len(Plant.objects.all())
        self.assertEqual(num_plants_before + 1, num_plants_after)
