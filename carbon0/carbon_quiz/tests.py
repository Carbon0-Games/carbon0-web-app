from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse_lazy, reverse, resolve

from .models.question import Question
from .models.mission import Mission
from .models.quiz import Quiz
from .models.achievement import Achievement
from .views import (
    MissionDetail,
    QuizCreate,
    QuizDetail,
)


class QuestionTests(TestCase):
    '''Test suite for the Question model in the database.'''
    def setUp(self):
        '''Create new instances of the Question model.'''
        # store the Questions in an array
        self.questions = [
            Question.objects.create(question_text="How often do you recycle?",
                question_info="Asks the frequency of recycling", 
                carbon_value=3.2, 
                category="R", 
                learn_more_link="www.recycling.com"),
            Question.objects.create(
                question_text="How many miles do you drive a week?",
                question_info="Asks for the miles driven", 
                carbon_value=2.2, 
                category="T", 
                learn_more_link="www.biking.com"),
            Question.objects.create(
                question_text="Do you have a composting bin?", 
                question_info="Asks for if user has composting bin", 
                carbon_value=1.2, 
                category="R", 
                learn_more_link="www.compostinginfo.com")
        ]
        # save the Questions 
        for q in self.questions:
            q.save()
        return None

    def test_question_db_query(self):
        '''Question objects can be looked up in the databse correctly.'''
        # test the Question object being retrieved
        question = Question.objects.get(
            question_text=self.questions[1].question_text
        )
        self.assertIsNot(question, None)
        return None

    def test_question_db_property(self):
        '''Question objects in the database have the correct field values.'''
        question = Question.objects.get(
            question_text=self.questions[0].question_text
        )
        self.assertEqual(question.category, self.questions[0].category)
        return None


class QuizTests(TestCase):
    '''Test suite for the Quiz model.'''
    def setUp(self):
        '''Create the necessary db instances before the tests run.'''
        # store 5 Questions in an array
        self.questions = [
            Question.objects.create(
                question_text="Do you recycle at least daily?",
                question_info="Reycling is important", 
                carbon_value=3.2, 
                category="R", 
                learn_more_link="www.recycling.com"),
            Question.objects.create(
                question_text="Do you carpool at least once a week?",
                question_info="Driving less helps the environment", 
                carbon_value=2.2, 
                category="T", 
                learn_more_link="www.biking.com"),
            Question.objects.create(question_text="Do you have LEDs?", 
                question_info="LEDs are more energy efficient!", 
                carbon_value=4.2, 
                category="U", 
                learn_more_link="www.LEDsFTW.com"),
            Question.objects.create(
                question_text="Do you fly on places more than annually?",
                question_info="Flying contributes a lot of emissions", 
                carbon_value=1.2, 
                category="A", 
                learn_more_link="www.flyinggreen.com"),
            Question.objects.create(question_text="Do you eat vegan?", 
                question_info="Research shows it can be more sustainable", 
                carbon_value=5.2, 
                category="D", 
                learn_more_link="www.vegan-diet.com")
        ]
        # save the Questions 
        for q in self.questions:
            q.save()
        # save a new Quiz
        quiz = Quiz.objects.create()
        quiz.save()
        self.quiz = quiz
        return None

    def test_quiz_attributes(self):
        '''A Quiz instance is saved in the database with the correct fields.'''
        # retrieve the Quiz
        quiz = Quiz.objects.first()
        # test that it has the correct identifiers
        self.assertEqual(quiz.id, self.quiz.id)
        self.assertEqual(quiz.title, self.quiz.title)
        self.assertEqual(quiz.slug, self.quiz.slug)
        # test that it has the correct default values
        self.assertEqual(quiz.active_question, 0)
        self.assertEqual(quiz.carbon_value_total, 0)
        # test that is has the right questions array
        self.assertEqual(quiz.questions, self.quiz.questions)
        return None


class MissionModelTest(TestCase):
    '''Test suite for the Mission model.'''
    pass

class AchievementModelTest(TestCase):
    '''Test suite for the Achievement model.'''
    pass


class QuizCreateTests(TestCase):
    '''Test suite for the QuizCreate view controller.'''
    def setUp(self):
        '''Create the necessary db instances before the tests run.'''
        # store the URL pattern of the view
        self.url = reverse("carbon_quiz:quiz_create")
        # store 5 Questions in an array
        self.questions = [
            Question.objects.create(
                question_text="Do you recycle at least daily?",
                question_info="Reycling is important", 
                carbon_value=3.2, 
                category="R", 
                learn_more_link="www.recycling.com"),
            Question.objects.create(
                question_text="Do you carpool at least once a week?",
                question_info="Driving less helps the environment", 
                carbon_value=2.2, 
                category="T", 
                learn_more_link="www.biking.com"),
            Question.objects.create(question_text="Do you have LEDs?", 
                question_info="LEDs are more energy efficient!", 
                carbon_value=4.2, 
                category="U", 
                learn_more_link="www.LEDsFTW.com"),
            Question.objects.create(
                question_text="Do you fly on places more than annually?",
                question_info="Flying contributes a lot of emissions", 
                carbon_value=1.2, 
                category="A", 
                learn_more_link="www.flyinggreen.com"),
            Question.objects.create(question_text="Do you eat vegan?", 
                question_info="Research shows it can be more sustainable", 
                carbon_value=5.2, 
                category="D", 
                learn_more_link="www.vegan-diet.com")
        ]
        # save the Questions 
        for q in self.questions:
            q.save()
        return None
    
    def test_get_quiz_create(self):
        '''User is able to get a page with instructions of the quiz.'''
        # client makes a request to GET the view
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        # test the content on the instructions page
        self.assertContains(response, "Welcome to the Carbon Quiz!")
        return None

    def test_user_starts_new_quiz(self):
        '''User starts the quiz and a new Quiz instance is created.'''
        # store the number of quiz objects before the request
        num_quizzes_before = len(Quiz.objects.all())
        # user makes a request to POST a new Quiz, and is redirected
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        # the number of quizzes has increased by one
        num_quizzes_after = len(Quiz.objects.all())
        self.assertEqual(num_quizzes_after, num_quizzes_before + 1)
        return None

    def test_user_starts_new_quiz(self):
        '''User starts the quiz and a new Quiz instance is created.'''
        # store the number of quiz objects before the request
        num_quizzes_before = len(Quiz.objects.all())
        # user makes a request to POST a new Quiz, and is redirected
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        # the number of quizzes has increased by one
        num_quizzes_after = len(Quiz.objects.all())
        self.assertEqual(num_quizzes_after, num_quizzes_before + 1)
        return None


class QuizDetail(TestCase):
    '''Test suite for the QuizDetail view.'''
    def setUp(self):
        '''Create the necessary db instances before the tests run.'''
        # instantiate the testing client
        self.client = Client()
        # store 5 Questions in an array
        self.questions = [
            # Recycling question
            Question.objects.create(
                question_text="Do you recycle at least daily?",
                question_info="Reycling is important", 
                carbon_value=3.2, 
                category="R", 
                learn_more_link="www.recycling.com"),
            # Transit question
            Question.objects.create(
                question_text="Do you carpool at least once a week?",
                question_info="Driving less helps the environment", 
                carbon_value=2.2, 
                category="T", 
                learn_more_link="www.biking.com"),
            # Utilities question
            Question.objects.create(question_text="Do you have LEDs?", 
                question_info="LEDs are more energy efficient!", 
                carbon_value=4.2, 
                category="U", 
                learn_more_link="www.LEDsFTW.com"),
            # Airline-Transit question
            Question.objects.create(
                question_text="Do you fly on places more than annually?",
                question_info="Flying contributes a lot of emissions", 
                carbon_value=1.2, 
                category="A", 
                learn_more_link="www.flyinggreen.com"),
            # Diet question
            Question.objects.create(question_text="Do you eat vegan?", 
                question_info="Research shows it can be more sustainable", 
                carbon_value=5.2, 
                category="D", 
                learn_more_link="www.vegan-diet.com")
        ]
        # save the Questions 
        for q in self.questions:
            q.save()
        # save a new Quiz
        quiz = Quiz.objects.create(
            questions=[q.id for q in self.questions]
        )
        quiz.save()
        self.quiz = quiz
        # create Missions related to the Questions
        self.missions = [
            # Diet mission
            Mission.objects.create(
                title="Beginner Diet Mission",
                action='learn about the vegan diet',
                learn_more="find out 20 delicious, nutritious vegan recipes!",
                link_descriptions=["List of the Top 20 Vegan Recipes"],
                link_addresses=["recipes.com/diets/vegan"],
                question=self.questions[4]
            ),
            # Recycling mission
            Mission.objects.create(
                title="Beginner Recycling Mission",
                action='learn about recycling',
                learn_more="find out what's recyclable!",
                link_descriptions=["List of the Top 20 Recyclables"],
                link_addresses=["recipes.com/diets/vegan"],
                question=self.questions[0]
            ),
            # Transit mission
            Mission.objects.create(
                title="Beginner Transit Mission",
                action='learn about transit',
                learn_more="find out what's being emitted when you drive!",
                link_descriptions=["Tips for Car-Pooling"],
                link_addresses=["carpools.com"],
                question=self.questions[1]
            ),
            # Utilities mission
            Mission.objects.create(
                title="Beginner Utilities Mission",
                action='buy LEDs',
                learn_more="compare LEDs to CFLs!",
                link_descriptions=["Buy LEDs at the Hardware Store"],
                link_addresses=["hardwarestore.com"],
                question=self.questions[2]
            ),
            # Airline-Transit mission
            Mission.objects.create(
                title="Beginner Airline-Transit Mission",
                action='offset your carbon footprint',
                learn_more="see how much planes emit each year!",
                link_descriptions=["Science of Plane Emissions"],
                link_addresses=["plane-emissions.com"],
                question=self.questions[3]
            )
        ]
        # save the Missions
        for m in self.missions:
            m.save()
        return None

    def test_get_question_page(self):
        """
        A User gets a view of the Quiz, with one of the Questions displayed.
        """
        # user makes a request to GET the QuizDetail view
        url = reverse(
            "carbon_quiz:quiz_detail", args=[
                self.quiz.slug, # arg for slug (URL param)
                self.quiz.active_question  # arg for question_number
            ]
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
            "carbon_quiz:quiz_detail", args=[
                self.quiz.slug, # arg for slug (URL param)
                self.quiz.active_question  # arg for question_number
            ]
        )
        response = self.client.get(url)
        # the response is returned OK
        self.assertEqual(response.status_code, 200)
        # now pick one of the Questions whose id is not 0 
        question = self.quiz.questions[4]
        # test that the related mission is shown on the response HTML
        mission = Mission.objects.get(question=question)
        self.assertContains(response, mission.title)
        return None


class MissionDetailTest(TestCase):
    '''Test suite for the MissionDetail view.'''
    def setUp(self):
        '''Initial work executed before each test in this suite.'''
        # save a Question
        self.question = Question.objects.create(
            question_text="How often do you recycle?",
            question_info="Recycling = Tried and Trusted Way to Live Green",
            carbon_value=3.2,
            category="R",
            learn_more_link="www.recycling.com",
            learn_image=None
        )
        self.question.save()
        # save a mission
        self.mission = Mission.objects.create(
            title="Recycle More", 
            action="Try recycling everyday!",
            learn_more="www.recycling.com",
            question=self.question
        )
        self.mission.save()
        # set up the testing client
        self.client = Client()
        # store a property - the URL related to the view function
        self.url = 'carbon_quiz:mission_detail'
        return None

    def test_mission_page(self):
        '''User makes a request to see a Mission, and views its details.'''
        # user makes the request to GET the view
        mission_url = reverse(self.url, kwargs={'pk': self.mission.pk})
        response = self.client.get((mission_url))
        # the response is returned OK
        self.assertEqual(response.status_code, 200)
        # the response HTML has the appropiate content
        mission = Mission.objects.get(id=self.mission.id)
        self.assertContains(response, mission.title)
        return None
