from django.db import models

from .mission import Mission


class Link(models.Model):
    '''Represents a link clicked on as part of one of the Missions.'''
    mission = models.ForeignKey(
        Mission, on_delete=models.CASCADE,
        help_text='The related Mission.'
    )
    description = models.CharField(
        max_length=300, blank=True, null=True,
        help_text="The website the user can visit to complete the mission."
    )
    address = models.CharField(
        max_length=300, blank=True, null=True,
        help_text="Links that user can click to complete the mission."
    )

    def __str__(self):
        '''Represents the link in a human-readable way.'''
        return f'Link for {self.address}'
