from django.test import TestCase, Client, RequestFactory
from django.urls import reverse_lazy, reverse, resolve
from django.contrib.auth.models import User
import datetime

from .views import (
    QuizCreate,
    QuizDetail,
    MissionDetail,
    AchievementCreate,
    AchievementDetail
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
        question = Question.objects.create(question_text="How often do you recycle?", question_info="Asks the frequency of recycling", carbon_value=3.2, category="R", learn_more_link="www.recycling.com", learn_image="carbon0Home.png")
        self.mission = Mission.objects.create(title="Recycle More", action="Try recycling everyday!", clicks_needed=1, learn_more="www.recycling.com", question=question)
        self.client = Client()
        # self.url = 'carbon-quiz/mission/<pk:id>/'
        self.url = 'carbon_quiz:mission_detail'

    def test_mission_page(self):
        mission_url = reverse(self.url, kwargs={'pk': self.mission.pk})
        response = self.client.get((mission_url))
        self.assertEqual(response.status_code, 200)

        # resolver = resolve(self.url)
        # self.assertEqual(resolver.func.cls, MissionDetail)

 
class QuizCreateViewTest(TestCase):

    def setUp(self):
        self.request_factory = RequestFactory()
        Question.objects.create(question_text="How often do you recycle?", question_info="Asks the frequency of recycling", carbon_value=3.2, category="R", learn_more_link="www.recycling.com"),
        Question.objects.create(question_text="How many miles do you drive a week?", question_info="Asks for the miles driven", carbon_value=2.2, category="T", learn_more_link="www.biking.com"),
        Question.objects.create(question_text="Do you have a composting bin?", question_info="Asks for if user has composting bin", carbon_value=1.2, category="D", learn_more_link="www.compostinginfo.com"),
        Question.objects.create(question_text="How many miles do you drive a week?", question_info="Asks for the miles driven", carbon_value=2.2, category="A", learn_more_link="www.biking.com"),
        Question.objects.create(question_text="Do you have a composting bin?", question_info="Asks for if user has composting bin", carbon_value=1.2, category="U", learn_more_link="www.compostinginfo.com")

    def test_user_gets_template(self):
        get_request = self.request_factory.get('carbon_quiz:quiz_create')
        response = QuizCreate.as_view()(get_request)
        self.assertEqual(response.status_code, 200)

    def test_user_post_action(self):
        quiz_nums = len(Quiz.objects.all())

        post_request = self.request_factory.post('carbon_quiz:quiz_create')
        # when page is submitted
        response = QuizCreate.as_view()(post_request)
        quiz_nums_after = len(Quiz.objects.all())
        self.assertNotEqual(quiz_nums, quiz_nums_after)

class QuizDetailViewTest(TestCase):

    def setUp(self):
        self.request_factory = RequestFactory()
        self.question1 = Question.objects.create(question_text="How often do you recycle?", question_info="Asks the frequency of recycling", carbon_value=3.2, category="R", learn_more_link="www.recycling.com", pk=1, learn_image="Carbon0Home.png"),
        self.question2 = Question.objects.create(question_text="How many miles do you drive a week?", question_info="Asks for the miles driven", carbon_value=2.2, category="T", learn_more_link="www.biking.com", pk=2),
        self.question3 = Question.objects.create(question_text="Do you have a composting bin?", question_info="Asks for if user has composting bin", carbon_value=1.2, category="D", learn_more_link="www.compostinginfo.com", pk=3),
        self.question4 = Question.objects.create(question_text="How many miles do you drive a week?", question_info="Asks for the miles driven", carbon_value=2.2, category="A", learn_more_link="www.biking.com", pk=4),
        self.quesiton5 = Question.objects.create(question_text="Do you have a composting bin?", question_info="Asks for if user has composting bin", carbon_value=1.2, category="U", learn_more_link="www.compostinginfo.com", pk=5)

    def test_get_template(self):
        # q1 = Question.objects.create(question_text="How often do you recycle?", question_info="Asks the frequency of recycling", carbon_value=3.2, category="R", learn_more_link="www.recycling.com", id=1, learn_image="carbon0Home.png")
        quiz = Quiz.objects.create(title="Quiz Your Carbon Footprint",carbon_value_total=2.3, active_question= 1,
                                   questions=[1,1,1,1]

                                #    questions= [self.question1.id]
                                #    questions=[self.question1.id, self.question2.id, self.question3.id, self.question4.id, self.quesiton5.id]
                                    )

        get_request = self.request_factory.get('carbon_quiz/quiz/detail.html')
        response = QuizDetail.as_view()(get_request, slug=quiz.slug, is_question_answered=0)

        self.assertEqual(response.status_code, 200)

class AchievementCreateViewTest(TestCase):
    
    def setUp(self):
        self.request_factory = RequestFactory()

    def test_get_tempalte(self):
        question = Question.objects.create(question_text="How many miles do you drive a week?", 
                                           question_info="Asks for the miles driven", 
                                           carbon_value=2.2, 
                                           category="T", 
                                           learn_more_link="www.biking.com",
                                           learn_image="carbon0Home.png")

        mission = Mission.objects.create(title="Bikecyle more", 
                                         action="Find wasy to bike more",
                                         clicks_needed=3,
                                         learn_more="Biking helps reduce fossil fuel usage",
                                         question=question, id=1)

        template_name = 'carbon_quiz/mission/detail.html'
        get_request = self.request_factory.get(template_name)
        response = AchievementCreate.as_view()(get_request, mission_id=1)
        self.assertEqual(response.status_code, 200)

    def test_post_mission(self):
        question = Question.objects.create(question_text="How many miles do you drive a week?", 
                                           question_info="Asks for the miles driven", 
                                           carbon_value=2.2, 
                                           category="T", 
                                           learn_more_link="www.biking.com",
                                           learn_image="carbon0Home.png")

        mission = Mission.objects.create(title="Bikecyle more", 
                                         action="Find wasy to bike more",
                                         clicks_needed=3,
                                         learn_more="Biking helps reduce fossil fuel usage",
                                         question=question, id=1)

        template_name = 'carbon_quiz/mission/detail.html'
        post_request = self.request_factory.post(template_name)
        AchievementCreate.as_view()(post_request, mission_id=1)

        success_url = 'accounts:signup'
        response = Client().get(reverse_lazy(success_url))
        self.assertEqual(response.status_code, 200)

class AchievementDetailViewTest(TestCase):

    def setUp(self):
        self.request_factory = RequestFactory()

    def test_get_tempate(self):
        user = User.objects.create()
        question = Question.objects.create(question_text="How many miles do you drive a week?", 
                                           question_info="Asks for the miles driven", 
                                           carbon_value=2.2, 
                                           category="T", 
                                           learn_more_link="www.biking.com",
                                           learn_image="carbon0Home.png")

        mission = Mission.objects.create(title="Bikecyle more", 
                                         action="Find wasy to bike more",
                                         clicks_needed=3,
                                         learn_more="Biking helps reduce fossil fuel usage",
                                         question=question, id=1)

        achievement = Achievement.objects.create(mission=mission,
                                                 zeron_name="Bike Master",
                                                 user=user,
                                                 id=1
                                                 )

        template_name = 'carbon_quiz/achievement/detail.html'
        get_request = self.request_factory.get(template_name)
        response = AchievementDetail.as_view()(get_request, pk=1)
        self.assertEqual(response.status_code, 200)