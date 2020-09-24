from django.test import TestCase, Client
from django.urls import reverse_lazy, reverse, resolve
from django.contrib.auth.models import User
import datetime


from .views import (
    QuizCreate,
    MissionDetail
)

from .models.question import Question
from .models.mission import Mission
from .models.quiz import Quiz
from .models.achievement import Achievement


# Create your tests here.
# TODO Cao: write tests for the views (to be implemented by Zain)

class QuestionModelTest(TestCase):

    def setUp(self):
        self.questions = [
        Question(question_text="How often do you recycle?", question_info="Asks the frequency of recycling", carbon_value=3.2, category="R", learn_more_link="www.recycling.com"),
        Question(question_text="How many miles do you drive a week?", question_info="Asks for the miles driven", carbon_value=2.2, category="T", learn_more_link="www.biking.com"),
        Question(question_text="Do you have a composting bin?", question_info="Asks for if user has composting bin", carbon_value=1.2, category="R", learn_more_link="www.compostinginfo.com")
        ]


    def test_question_model(self):
        self.assertEqual(self.questions[1].question_text, "How many miles do you drive a week?")
        self.assertEqual(self.questions[0].carbon_value, 3.2)
        self.assertEqual(self.questions[0].category, "R")



class QuizModelTest(TestCase):

    def test_quiz_model(self):
        quiz = Quiz.objects.create(title="Quiz for new user", active_question=1, carbon_value_total=23.2)
        absolute_url = quiz.get_absolute_url()
        # print(absolute_url)
        self.assertEqual(absolute_url, "/answer-question/quiz-for-new-user/0/")
        self.assertEqual(quiz.title, "Quiz for new user")
        self.assertEqual(quiz.carbon_value_total, 23.2)


class MissionModelTest(TestCase):

    def test_mission_model(self):
        question = Question.objects.create(question_text="How often do you recycle?", question_info="Asks the frequency of recycling", carbon_value=3.2, category="R", learn_more_link="www.recycling.com")
        mission = Mission(title="Recyle More Often", action="This mission will encourage users to recyle more often", clicks_needed=2, learn_more="Recycling helps the planet become more sustainable", question=question, links=["www.recycle.com", "www.plasticwaste.com"])
        self.assertEqual(mission.title, "Recyle More Often")
        self.assertEqual(mission.clicks_needed, 2)
        self.assertEqual(mission.question, question)

class AchievementModelTest(TestCase):

    def test_achievement_model(self):
        user = User.objects.create()
        question = Question.objects.create(question_text="How often do you recycle?", question_info="Asks the frequency of recycling", carbon_value=3.2, category="R", learn_more_link="www.recycling.com")
        mission = Mission.objects.create(title="Recyle More Often", action="This mission will encourage users to recyle more often", clicks_needed=2, learn_more="Recycling helps the planet become more sustainable", question=question, links=["www.recycle.com", "www.plasticwaste.com"])
        achievement = Achievement.objects.create(mission=mission, user=user, completion_date=datetime.datetime.now(), zeron_name="Recycle Zeron", badge_name="Recyle Master")

        self.assertEqual(achievement.zeron_name, "Recycle Zeron")

class MissionDetailTest(TestCase):

    def setUp(self):
        '''Initial work done for each test in this suite.'''
        question = Question.objects.create(question_text="How often do you recycle?", question_info="Asks the frequency of recycling", carbon_value=3.2, category="R", learn_more_link="www.recycling.com")
        self.mission = Mission.objects.create(id=1, title="Recycle More", action="Try recycling everyday!", clicks_needed=1, learn_more="www.recycling.com", question=question)
        self.client = Client()
        # self.url = 'carbon-quiz/mission/<pk:id>/'
        self.url = 'carbon_quiz:mission_detail'

    def test_mission_page(self):
        mission_url = reverse(self.url, kwargs={'pk': self.mission.pk})
        response = self.client.get((mission_url))
        self.assertEqual(response.status_code, 200)

        # resolver = resolve(self.url)
        # self.assertEqual(resolver.func.cls, MissionDetail)

 
