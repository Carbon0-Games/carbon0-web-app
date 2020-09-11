from django.test import TestCase, Client
from django.urls import reverse_lazy, reverse, resolve
from .views import (
    QuizCreate,
    MissionDetail
)

from .models import (
    Achievement,
    Mission,
    Question,
    Quiz,
)


# Create your tests here.
# TODO Cao: write tests for the views (to be implemented by Zain)

class QuizDetailTest(TestCase):

    questions = [
        Question(question_text="testing quesiton", question_info="nothing much", carbon_value=1.2, category="D", learn_more_link="www.com"),
        Question(question_text="testing quesiton 2", question_info="nothing much", carbon_value=1.2, category="D", learn_more_link="www.com"),
        Question(question_text="testing quesiton 3", question_info="nothing much", carbon_value=1.2, category="D", learn_more_link="www.com")


    ]

    def test_single_quiz(self):
        self.assertEqual(self.questions[1].question_text, "testing quesiton 2")




class MissionDetailTest(TestCase):

    # questions = [
    #     Question(question_text="testing quesiton", question_info="nothing much", carbon_value=1.2, category="D", learn_more_link="www.com"),
    #     Question(question_text="testing quesiton 2", question_info="nothing much", carbon_value=1.2, category="D", learn_more_link="www.com"),
    #     Question(question_text="testing quesiton 3", question_info="nothing much", carbon_value=1.2, category="D", learn_more_link="www.com")


    # ]

    def setUp(self):
        '''Initial work done for each test in this suite.'''
        question1 = Question.objects.create(question_text="testing", question_info="info", carbon_value=1.2, category="D", learn_more_link="ww.ww")
        self.mission = Mission.objects.create(id=1, title="testing", action="compost", clicks_needed=1, learn_more="testing", question=question1)
        self.client = Client()
        # self.url = 'carbon-quiz/mission/<pk:id>/'
        self.url = 'carbon_quiz:mission_detail'

    def test_mission_page(self):
        mission_url = reverse(self.url, kwargs={'pk': self.mission.pk})
        response = self.client.get((mission_url))
        self.assertEqual(response.status_code, 200)

        # resolver = resolve(self.url)
        # self.assertEqual(resolver.func.cls, MissionDetail)

 