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
    link_descriptions = ArrayField(
        models.CharField(max_length=300, blank=True, null=True),
        null=True, blank=True,
        help_text=(
            "What websites the user can click to complete the mission."
        ),
    )
    link_addresses = ArrayField(
        models.CharField(max_length=300, blank=True, null=True),
        null=True, blank=True,
        help_text=(
            "Links that user can click to complete the mission." 
        )
    )
    question = models.ForeignKey(
        Question, on_delete=models.PROTECT,
        help_text="The question to which this mission relates.",
    )

    def __str__(self):
        '''Returns human-readable name of the Mission.'''
        return f'{self.title}'

    """
    def split_links(self):
        '''Return one list of just website links, and of the site names.'''
        is_link = True
        links, site_names = list(), list()
        for element in self.links:
            if is_link is True:
                links.append(element)
                is_link = False
            else:  # is_link is False
                site_names.append(element)
                is_link = True
        return links, site_names
    """
