import datetime

from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.text import slugify


class Question(models.Model):
    '''Represents a single question on the Carbon calculator quiz.'''
    question_text = models.CharField(max_length=500,
        help_text="Question for the user"
    )
    question_info = models.TextField(
        help_text="Explains any vocabulary relevant to the question."
    )
    carbon_value = models.FloatField(
        help_text="Tons of carbon that may be present in user's footprint."
    )
    # Define the categories a question can fall into
    CATEGORIES = [
        ('D', 'Diet'),
        ('T', 'Transit'),
        ('R', 'Recycling'),
        ('A', 'Airline-Travel'),
        ('U', 'Utilities'),
    ]
    category = models.CharField(max_length=1, choices=CATEGORIES,
        help_text="The area of sustainability to which this question relates."
    )
    learn_more_link = models.CharField(max_length=1000, help_text=
        "Hyperlink where the user can learn more about the question",
        null=True, blank=True
    )

    def __str__(self):
        '''Returns the category of the Question, and it's id.'''
        return f'Question {self.category} {self.id}'


class Quiz(models.Model):
    '''Represents a collection of 5 questions given to the user.'''
    title = models.CharField(max_length=500,
                             unique=True,
                             help_text="Title of the quiz.",
                             null=True)
    slug = models.SlugField(max_length=500,
                            blank=True, editable=False,
                            null=True,
                            help_text=("Unique URL path to access this quiz. "
                                       + "Generated by the system."))
    questions = ArrayField(
        models.IntegerField(), size=5, 
        help_text="Array of ids for the quiz questions.", null=True, blank=True
    )
    active_question = models.IntegerField(
        help_text="Id of the question currently being asked.", 
        default=0, blank=True
    )
    carbon_value_total = models.FloatField(
        blank=True, default=0, 
        help_text='Total metric tons of carbon that the user can eliminate.'
    )

    def __str__(self):
        '''Returns human-readable name of the Quiz.'''
        return f'{self.title}'

    def get_absolute_url(self):
        """
        Returns a fully qualified path for a Quiz.
        The arg for question_answered on first GET after QuizCreate, is 0
        because we want to make sure it can't refer to a real Question model.
        """
        path_components = {
            'slug': self.slug,
            'question_answered': 0  
        }
        return reverse('carbon_quiz:quiz_detail', kwargs=path_components)

    def save(self, *args, **kwargs):
        '''Creates a URL safe slug automatically when a new note is saved.'''
        if not self.pk:
            self.slug = slugify(self.title, allow_unicode=True)

        # call save on the superclass
        return super(Quiz, self).save(*args, **kwargs)

    

class Mission(models.Model):
    '''Represents a possible action the user takes to help the environment.'''
    title = models.CharField(max_length=500,
                             unique=True,
                             help_text="Title of the mission.",
                             null=True)
    action = models.CharField(
        max_length=500, null=True,
        help_text='Describes what the user needs to do.'
    )
    clicks_needed = models.IntegerField(
        default=1, help_text='Number of the links user needs to click.'
    )
    learn_more = models.TextField(
        help_text="Explains why the mission matters.",
        null=True, blank=True
    )
    links = ArrayField(
        models.CharField(max_length=500), size=3,
        help_text="Links that the user can click to complete the mission.",
        null=True, blank=True
    )
    question = models.ForeignKey(
        Question, on_delete=models.PROTECT,
        help_text="The question to which this mission relates.",
    )

    def __str__(self):
        '''Returns human-readable name of the Mission.'''
        return f'{self.title}'


class Achievement(models.Model):
    '''Represents what the user attains for completing a mission.'''
    mission = models.OneToOneField(
        Mission, on_delete=models.PROTECT,
        help_text='The mission that earns this achievement.',
        null=True
    )
    user = models.ForeignKey(
        User, on_delete=models.PROTECT, null=True,
        help_text='The user who completed the mission.'
    )
    completion_date = models.DateTimeField(
        help_text="Date mission was accomplished",
        null=True, blank=True, auto_now=True                          
    )
    zeron_name = models.CharField(max_length=200, default="Zeron prize")
    zeron_image = models.FileField(
        null=True, blank=True, help_text='To be revisited in Feature 2.'
    )
    badge_name = models.CharField(
        max_length=200, null=True, blank=True,
        help_text='The badge that the user earns in this achievement.'
    )

    def __str__(self):
        '''Returns a human-readable name for the Achievement.'''
        mission = Mission.objects.get(id=self.mission.id)
        return f"Achievement for Mission: '{mission.title}'"

    def get_absolute_url(self):
        '''Returns a fully qualified path for a Achievement.'''
        path_components = {'pk': self.pk,}
        return reverse('carbon_quiz:achievement_detail', kwargs=path_components)
