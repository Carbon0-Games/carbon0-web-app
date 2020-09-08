import datetime

from django.db import models
from django.utils import timezone


class Question(models.Model):
    '''Represents a single question on the Carbon calculator quiz.'''
    question_text = models.CharField(max_length=200,
        help_text="Question for the user"
    )
    question_info = models.CharField(max_length=200,
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


class Quiz(models.Model):
    pass


class Mission(models.Model):
    completion_date = models.DateTimeField("date mission was accomplished")




class Achievement(models.Model):
    pass
