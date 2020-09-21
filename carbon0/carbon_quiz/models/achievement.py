from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse, reverse_lazy

from .mission import Mission
from .question import Question


class Achievement(models.Model):
    '''Represents what the user attains for completing a mission.'''
    mission = models.ForeignKey(
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
    # Define the types of Zerons an Achievement can have
    ZERONS = [
        # the tuples below follow the format: `(img_url_path, name_of_zeron)`
        ('assets/cartoon_carrot.gltf', 'Carrot Model'),  # goes with Diet
        ('assets/Wheel.gltf', 'Wheel Model'),  # goes with Transit 
        ('assets/Bin.gltf', 'Bin Model'),  # goes with Recycling 
        ('assets/coin.gltf', 'Coin Model'),  # goes with Airline-Travel 
        ('assets/Light bulb 1.gltf', 'Light Bulb Model'),  # # goes with Utilities
    ]
    zeron_image_url = models.CharField(
        choices=ZERONS,
        max_length=100, null=True, 
        blank=True, help_text='Path to the 3D model in storage.'
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

    def zeron_say_hello(self):
        '''Returns a greeting the Zeron says to the User.'''
        # find the name of the zeron this model has
        greeting = ''
        for img_url, zeron_name in Achievement.ZERONS:
            if self.zeron_image_url == img_url:
                # set the greeting
                greeting = (
                    f"I'm {zeron_name}. " +
                     "Thanks for helping to save the planet!"
                )
        # return the greeting
        return greeting

    @classmethod
    def set_zeron_image_url(cls, mission):
        """
        Returns the appropiate Zeron, given a Mission model instance.

        Parameters:
        mission(Mission): the Mission model that has been completed

        Returns:
        Tuple(str, str): the value in Achievement.ZERONS that 
                         corresponds to the category this Mission 
                         falls under (must refer back to related Question)

        """
        # get the category of the question related to the mission
        category = mission.question.category
        # store a list of the categories Questions may be in
        category_abbreviations = [
            category_abbrev for category_abbrev, category in Question.CATEGORIES
        ]
        # map each category to a Zeron name 
        category_to_zerons = dict(
            zip(category_abbreviations, Achievement.ZERONS)
        )
        # find the right choice of zeron, given the category
        zeron_img_path, zeron_model_name = category_to_zerons[category]
        return zeron_img_path
         