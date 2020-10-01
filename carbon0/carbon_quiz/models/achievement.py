from django.core.management import utils
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.urls import reverse, reverse_lazy
from django.utils.text import slugify

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
    secret_id = models.CharField(
        max_length=50, unique=True, null=True,
        help_text="Unique id that cannot be guessed easily."
    )
    # Zerons for Achievements: (img_url_paths: List[str], name_of_zeron: str)
    ZERONS = [
        # 1. Diet category Zeron
        (['assets/glb-files/cartoon_carrot.glb', 
          'assets/usdz-files/tree.usdz'], 
            "Nature's Model"), 
        # 2. Transit category Zeron
        (['assets/glb-files/Wheel.glb',
          'assets/usdz-files/wheel.usdz'],
            'Wheel Model'), 
        # 3. Recycling category Zeron 
        (['assets/glb-files/Bin.glb',
          'assets/usdz-files/bin.usdz'],
            'Bin Model'), 
        # 4. Airline-Travel category Zeron
        (['assets/glb-files/coin.glb',
          'assets/usdz-files/coin.usdz'],
            'Coin Model'), 
        # 5. Utilities category Zeron
        (['assets/glb-files/Light bulb 1.glb',
          'assets/usdz-files/Lightbulb.usdz'],
            'Light Bulb Model'),  
    ]
    zeron_image_url = ArrayField(
        models.CharField(
        max_length=100, null=True, 
        blank=True,
        ),
        null=True, blank=True, choices=ZERONS,
        help_text='File paths to the 3D model in storage.'
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
        zeron_img_paths, zeron_model_name = category_to_zerons[category]
        return zeron_img_paths

    def save(self, *args, **kwargs):
        '''Init the secret_id field on the new instance.'''
        def generate_unique_id():
            '''Ensures that the id is unique.'''
            # get a set of all existing ids
            ids = set([a.id for a in Achievement.objects.all()])
            # init a secret id
            new_id = utils.get_random_secret_key()
            # make sure it is unique
            while new_id in ids:
                new_id = utils.get_random_secret_key()
            return new_id
        # get the unique secret id, make it URL safe
        secret_id = slugify(generate_unique_id())
        # set it on the new model instance 
        self.secret_id = secret_id
        return super(Achievement, self).save(*args, **kwargs)   
