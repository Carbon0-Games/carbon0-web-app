from django.contrib.postgres.fields import ArrayField
from django.db import models

from .question import Question


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
