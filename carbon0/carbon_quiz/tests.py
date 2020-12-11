from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from django.test.client import RequestFactory
from django.test import Client, TestCase
from django.urls import reverse_lazy, reverse, resolve
from django.contrib.auth.models import User
import datetime

from .views import QuizCreate, MissionDetail
from accounts.models import Profile
from .models.link import Link
from .models.question import Question
from .models.mission import Mission
from .models.quiz import Quiz
from .models.achievement import Achievement
from .views import (
    AchievementCreate,
    AchievementDetail,
    MissionDetail,
    QuizCreate,
    QuizDetail,
)


class DatabaseSetup(TestCase):
    """Parent class to handle the instantiation of models for testing."""

    def setUp(self):
        """Create 5 Questions and 1 Quiz."""
        # store 5 Questions in an array
        self.questions = [
            Question.objects.create(
                question_text="Do you recycle at least daily?",
                question_info="Reycling is important",
                carbon_value=3.2,
                category="R",
                learn_more_link="www.recycling.com",
            ),
            Question.objects.create(
                question_text="Do you carpool at least once a week?",
                question_info="Driving less helps the environment",
                carbon_value=2.2,
                category="T",
                learn_more_link="www.biking.com",
            ),
            Question.objects.create(
                question_text="Do you have LEDs?",
                question_info="LEDs are more energy efficient!",
                carbon_value=4.2,
                category="U",
                learn_more_link="www.LEDsFTW.com",
            ),
            Question.objects.create(
                question_text="Do you fly on places more than annually?",
                question_info="Flying contributes a lot of emissions",
                carbon_value=1.2,
                category="A",
                learn_more_link="www.flyinggreen.com",
            ),
            Question.objects.create(
                question_text="Do you eat vegan?",
                question_info="Research shows it can be more sustainable",
                carbon_value=5.2,
                category="D",
                learn_more_link="www.vegan-diet.com",
            ),
        ]
        # save the Questions
        for q in self.questions:
            q.save()
        # save a new Quiz
        quiz = Quiz.objects.create(title="New Quiz 1")
        quiz.save()
        self.quiz = quiz
        return None


class QuestionTests(TestCase):
    """Test suite for the Question model in the database."""


class QuestionModelTest(TestCase):
    def setUp(self):
        """Create new instances of the Question model."""
        # store the Questions in an array
        self.questions = [
            Question.objects.create(
                question_text="How often do you recycle?",
                question_info="Asks the frequency of recycling",
                carbon_value=3.2,
                category="R",
                learn_more_link="www.recycling.com",
            ),
            Question.objects.create(
                question_text="How many miles do you drive a week?",
                question_info="Asks for the miles driven",
                carbon_value=2.2,
                category="T",
                learn_more_link="www.biking.com",
            ),
            Question.objects.create(
                question_text="Do you have a composting bin?",
                question_info="Asks for if user has composting bin",
                carbon_value=1.2,
                category="R",
                learn_more_link="www.compostinginfo.com",
            ),
        ]
        # save the Questions
        for q in self.questions:
            q.save()
        return None

    def test_question_db_query(self):
        """Question objects can be looked up in the databse correctly."""
        # test the Question object being retrieved
        question = Question.objects.get(question_text=self.questions[1].question_text)
        self.assertIsNot(question, None)
        return None

    def test_question_db_property(self):
        """Question objects in the database have the correct field values."""
        question = Question.objects.get(question_text=self.questions[0].question_text)
        self.assertEqual(question.category, self.questions[0].category)
        return None


class QuizTests(DatabaseSetup):
    """Test suite for the Quiz model."""

    def setUp(self):
        """Create the necessary db instances before the tests run."""
        super().setUp()

    def test_quiz_attributes(self):
        """A Quiz instance is saved in the database with the correct fields."""
        # retrieve the Quiz
        quiz = Quiz.objects.first()
        # test that it has the correct identifiers
        self.assertEqual(quiz.id, self.quiz.id)
        self.assertEqual(quiz.title, self.quiz.title)
        self.assertEqual(quiz.slug, self.quiz.slug)
        # test that it has the correct default values
        self.assertEqual(quiz.active_question, 0)
        self.assertEqual(quiz.carbon_value_total, 1000.0)
        # test that is has the right questions array
        self.assertEqual(quiz.questions, self.quiz.questions)
        return None


class MissionModelTest(TestCase):
    """Test suite for the Mission model."""

    pass


class AchievementModelTest(TestCase):
    """Test suite for the Achievement model."""

    pass


class QuizCreateTests(DatabaseSetup):
    """Test suite for the QuizCreate view controller."""

    def setUp(self):
        """Create the necessary db instances before the tests run."""
        # add Quiz and Question instances to the db
        super().setUp()
        # store the URL pattern of the view
        self.url = reverse("carbon_quiz:quiz_create")
        return None

    def test_get_quiz_create(self):
        """User is able to get a page with instructions of the quiz."""
        # client makes a request to GET the view
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        # test the content on the instructions page
        self.assertContains(response, "Welcome to the Carbon Quiz!")
        return None

    def test_user_starts_new_quiz(self):
        """User starts the quiz and a new Quiz instance is created."""
        # store the number of quiz objects before the request
        num_quizzes_before = len(Quiz.objects.all())
        # user makes a request to POST a new Quiz, and is redirected
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        # the number of quizzes has increased by one
        num_quizzes_after = len(Quiz.objects.all())
        self.assertEqual(num_quizzes_after, num_quizzes_before + 1)
        return None


class QuizDetailTests(DatabaseSetup):
    """Test suite for the QuizDetail view."""

    def setUp(self):
        """Create the necessary db instances before the tests run."""
        # instantiate the testing client
        self.client = Client()
        # add Question and Quiz instances to the db
        super().setUp()
        # populate the Questions array
        self.quiz.questions = [q.id for q in self.questions]
        self.quiz.save()
        # create Missions related to the Questions
        self.missions = [
            # Diet mission
            Mission.objects.create(
                title="Beginner Diet Mission",
                action="learn about the vegan diet",
                learn_more="find out 20 delicious, nutritious vegan recipes!",
                question=self.questions[4],
            ),
            # Recycling mission
            Mission.objects.create(
                title="Beginner Recycling Mission",
                action="learn about recycling",
                learn_more="find out what's recyclable!",
                question=self.questions[0],
            ),
            # Transit mission
            Mission.objects.create(
                title="Beginner Transit Mission",
                action="learn about transit",
                learn_more="find out what's being emitted when you drive!",
                question=self.questions[1],
            ),
            # Utilities mission
            Mission.objects.create(
                title="Beginner Utilities Mission",
                action="buy LEDs",
                learn_more="compare LEDs to CFLs!",
                question=self.questions[2],
            ),
            # Airline-Transit mission
            Mission.objects.create(
                title="Beginner Airline-Transit Mission",
                action="offset your carbon footprint",
                learn_more="see how much planes emit each year!",
                question=self.questions[3],
            ),
        ]
        # save the Missions
        for m in self.missions:
            m.save()
        # make links for the Missions
        self.links = [
            Link.objects.create(
                mission=Mission.objects.get(id=self.missions[0].id),
                description="List of the Top 20 Vegan Recipes",
                address="recipes.com/diets/vegan",
            ),
            Link.objects.create(
                mission=Mission.objects.get(id=self.missions[1].id),
                description="List of the Top 20 Recyclables",
                address="recipes.com/diets/vegan",
            ),
            Link.objects.create(
                mission=Mission.objects.get(id=self.missions[2].id),
                description="Tips for Car-Pooling",
                address="carpools.com",
            ),
            Link.objects.create(
                mission=Mission.objects.get(id=self.missions[3].id),
                description="Buy LEDs at the Hardware Store",
                address="hardwarestore.com",
            ),
            Link.objects.create(
                mission=Mission.objects.get(id=self.missions[4].id),
                description="Science of Plane Emissions",
                address="plane-emissions.com",
            ),
        ]
        # save the links
        for l in self.links:
            l.save()
        return None

    def test_get_question_page(self):
        """
        A User gets a view of the Quiz, with one of the Questions displayed.
        """
        # user makes a request to GET the QuizDetail view
        url = reverse(
            "carbon_quiz:quiz_detail",
            args=[
                self.quiz.slug,  # arg for slug (URL param)
                self.quiz.active_question,  # arg for question_number
            ],
        )
        response = self.client.get(url)
        # the response is returned OK
        self.assertEqual(response.status_code, 200)
        # user gets the correct Question
        question = self.quiz.get_current_question()
        self.assertContains(response, question.question_text)
        return None

    def test_get_missions(self):
        """
        After reaching the end of the quiz, user sees suggested missions.
        """
        # user finishes answering all the questions
        self.quiz.active_question = 5
        self.quiz.save()
        # user makes answer request to get the view
        url = reverse(
            "carbon_quiz:quiz_detail",
            args=[
                self.quiz.slug,  # arg for slug (URL param)
                self.quiz.active_question,  # arg for question_number
            ],
        )
        response = self.client.get(url)
        # the response is returned OK
        self.assertEqual(response.status_code, 200)
        # user is suggested missions randomly, because they're not logged in
        self.assertContains(response, "we randomly generated 3 missions")
        return None


class MissionDetailTest(TestCase):
    """Test suite for the MissionDetail view."""

    def setUp(self):
        """Initial work executed before each test in this suite."""
        # save a Question
        self.question = Question.objects.create(
            question_text="How often do you recycle?",
            question_info="Recycling = Tried and Trusted Way to Live Green",
            carbon_value=3.2,
            category="R",
            learn_more_link="www.recycling.com",
        )
        self.question.save()
        # save a mission
        self.mission = Mission.objects.create(
            title="Recycle More",
            action="Try recycling everyday!",
            learn_more="www.recycling.com",
            question=self.question,
        )
        self.mission.save()
        # set up the testing client
        self.client = Client()
        # store a property - the URL related to the view function
        self.url = "carbon_quiz:mission_detail"
        return None

    def test_mission_page(self):
        """User makes a request to see a Mission, and views its details."""
        # user makes the request to GET the view
        mission_url = reverse(self.url, kwargs={"pk": self.mission.pk})
        response = self.client.get((mission_url))
        # the response is returned OK
        self.assertEqual(response.status_code, 200)
        # the response HTML has the appropiate content
        mission = Mission.objects.get(id=self.mission.id)
        self.assertContains(response, mission.title)
        return None


class AchievementCreateTests(QuizDetailTests):
    """Test suite for the AchievementCreate view."""

    def setUp(self):
        """Create the models needed before each test int this suite."""
        # add 5 questions to the db
        # add a quiz to the db
        # add a mission to the db
        super().setUp()
        # add a User and their Profile to the db
        self.user = get_user_model().objects.create_user(
            "testing_user456",  # username
            "test@email.com",  # email
            "carbon0_ftw123",  # password
        )
        # instantiate a RequestFactory to mock authenticated requests
        self.factory = RequestFactory()
        self.profile = Profile.objects.create(user=self.user)
        self.profile.save()
        return None

    def test_user_gets_achievement_create_with_quiz_unauthenticated(self):
        """
        After a quiz, user visits the view and is
        returned a valid response.
        """
        # user makes the request
        request_url = reverse(
            "carbon_quiz:achievement_create",
            kwargs={
                "mission_id": self.missions[0].id,
                # "chosen_link_id": self.links[0].id,  # right now the Mission only has 1
                "quiz_slug": self.quiz.slug,
            },
        )
        # user gets a response
        response = self.client.get(request_url)
        # response is returned ok
        self.assertEquals(response.status_code, 200)
        # response has appropiate content
        self.assertContains(response, self.missions[0].title)
        return None

    def test_user_gets_achievement_create_without_quiz_unauthenticated(self):
        """
        After a quiz, user visits the view and is returned
        a valid response.
        """
        # user makes a request
        request_url = reverse(
            "carbon_quiz:achievement_create",
            kwargs={
                "mission_id": self.missions[0].id,
                # "chosen_link_id": self.links[0].id,  # right now the Mission only has 1
            },
        )
        # user gets a response
        response = self.client.get(request_url)
        # response is returned ok
        self.assertEquals(response.status_code, 200)
        # response has appropiate content
        self.assertContains(response, self.missions[0].title)
        return None

    def test_user_posts_achievement_with_quiz_authenticated(self):
        """
        A site visitor completes a Mission and their Zeron is saved on
        their profile.
        """
        # record the current number of Achievements before the request
        num_achievements_before = len(Achievement.objects.all())
        # user makes a request
        request = self.factory.post(
            reverse(
                "carbon_quiz:achievement_create",
                kwargs={
                    "mission_id": self.missions[0].id,
                    "quiz_slug": self.quiz.slug,
                },
            )
        )
        request.user = self.user
        # user gets a response
        response = AchievementCreate.as_view()(
            request, self.missions[0].id, self.quiz.slug
        )
        # user is redirected
        self.assertEquals(response.status_code, 302)
        # test that Achievement is made after the request
        num_achievements_after = len(Achievement.objects.all())
        self.assertEquals(num_achievements_after, num_achievements_before + 1)
        # test that the Achievement has the right Profile recorded
        achievement = Achievement.objects.get(mission=self.missions[0])
        self.assertEquals(achievement.profile, self.user.profile)
        return None

    def test_user_posts_achievement_without_quiz_authenticated(self):
        """
        A site visitor completes a Mission and their Zeron is saved on
        their profile.
        """
        # record the current number of Achievements before the request
        num_achievements_before = len(Achievement.objects.all())
        # user makes a request
        request = self.factory.post(
            reverse(
                "carbon_quiz:achievement_create",
                kwargs={"mission_id": self.missions[0].id},
            )
        )
        request.user = self.user
        # user gets a response
        response = AchievementCreate.as_view()(
            request, self.missions[0].id, self.quiz.slug
        )
        # user is redirected
        self.assertEquals(response.status_code, 302)
        # test that Achievement is made after the request
        num_achievements_after = len(Achievement.objects.all())
        self.assertEquals(num_achievements_after, num_achievements_before + 1)
        # test that the Achievement has the right Profile recorded
        achievement = Achievement.objects.get(mission=self.missions[0])
        self.assertEquals(achievement.profile, self.user.profile)
        return None


class AchievementDetailTests(AchievementCreateTests):
    """Test suite for the AcheivementDetail view."""

    def setUp(self):
        """Create the models needed before each test int this suite."""
        # add 5 questions to the db
        # add a quiz to the db
        # add a mission to the db
        # add a User and their Profile to the db
        super().setUp()
        # add an achievement to the db, that has a User relationship
        self.achievement_user = Achievement.objects.create(
            mission=self.missions[1],
            profile=self.profile,
            quiz=self.quiz,
            zeron_image_url=settings.RECYCLING_ZERON_PATHS,
        )
        self.achievement_user.save()
        # add an achievement to the db, that has no User relationship
        self.achievement_no_user = Achievement.objects.create(
            mission=self.missions[2],
            quiz=self.quiz,
            zeron_image_url=settings.TRANSIT_ZERON_PATHS,
        )
        self.achievement_no_user.save()
        # attach an attribute for an unauthenticated user
        self.visitor = AnonymousUser()
        return None

    def test_user_gets_achievement_details_unauthenticated(self):
        """
        A site vistor requests the AchievementDetail view
        and is informed about the Achievement they have earned.
        """
        # unauthenticated user makes a request to GET the view
        request = self.factory.get(
            reverse(
                "carbon_quiz:achievement_detail", args=[self.achievement_no_user.id]
            )
        )
        # attach session and user to request
        request.session = dict()
        request.session["achievement_pk"] = self.achievement_no_user.id
        request.user = self.visitor
        # user gets a response
        response = AchievementDetail.as_view()(request, self.achievement_no_user.id)
        # response is returned OK
        self.assertEqual(response.status_code, 200)
        # response has the appropiate content
        self.assertContains(response, "NEW Carbon Footprint")
        return None

    def test_user_gets_achievement_details_authenticated(self):
        """
        An authenticated requests the AchievementDetail view
        and is informed about the Achievement they have earned.
        """
        # user makes a request to GET the view
        request = self.factory.get(
            reverse("carbon_quiz:achievement_detail", args=[self.achievement_user.id])
        )
        # attach session and user to request
        request.session = dict()
        request.session["achievement_pk"] = self.achievement_user.id
        request.user = self.user
        # user gets a response
        response = AchievementDetail.as_view()(request, self.achievement_user.id)
        # response is returned OK
        self.assertEqual(response.status_code, 200)
        # response has the appropiate content
        self.assertContains(response, "Updated Carbon Footprint")
        return None
