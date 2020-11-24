from django.core.management import utils
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.urls import reverse, reverse_lazy
from django.utils.text import slugify

from accounts.models import Profile
from django.conf import settings
from .mission import Mission
from .question import Question
from .quiz import Quiz


class Achievement(models.Model):
    """Represents what the user attains for completing a mission."""

    mission = models.ForeignKey(
        Mission,
        on_delete=models.PROTECT,
        help_text="The mission that earns this achievement.",
        null=True,
    )
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        help_text="The profile that owns this achievement.",
        null=True,
    )
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.PROTECT,
        help_text="The Quiz that led the user to this achievement.",
        null=True,
    )
    completion_date = models.DateTimeField(
        help_text="Date mission was accomplished", null=True, blank=True, auto_now=True
    )
    secret_id = models.CharField(
        max_length=50,
        unique=True,
        null=True,
        help_text="Unique id that cannot be guessed easily.",
    )
    # Zerons for Achievements: (img_url_paths: List[str], name_of_zeron: str)
    ZERONS = [
        # 1. Diet category Zeron
        (settings.DIET_ZERON_PATHS, "Nature's Model"),
        # 2. Transit category Zeron
        (settings.TRANSIT_ZERON_PATHS, "Wheel Model"),
        # 3. Recycling category Zeron
        (settings.RECYCLING_ZERON_PATHS, "Bin Model"),
        # 4. Airline-Travel category Zeron
        (settings.AT_ZERON_PATHS, "Coin Model"),
        # 5. Utilities category Zeron
        (settings.UTIL_ZERON_PATHS, "Light Bulb Model"),
    ]
    zeron_image_url = ArrayField(
        models.CharField(
            max_length=100,
            null=True,
            blank=True,
        ),
        null=True,
        blank=True,
        choices=ZERONS,
        help_text="File paths to the 3D model in storage.",
    )
    badge_name = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        help_text="The badge that the user earns in this achievement.",
    )
    mission_response = models.CharField(
        max_length=700,
        null=True,
        blank=True,
        help_text="The text-answer which completed the mission."
    )

    def __str__(self):
        """Returns a human-readable name for the Achievement."""
        mission = Mission.objects.get(id=self.mission.id)
        return f"Achievement for Mission: '{mission.title}'"

    def get_absolute_url(self):
        """Returns a fully qualified path for a Achievement."""
        path_components = {
            "pk": self.pk,
        }
        return reverse("carbon_quiz:achievement_detail", kwargs=path_components)

    def zeron_say_hello(self):
        """Returns a greeting the Zeron says to the User."""
        # find the name of the zeron this model has
        greeting = ""
        for img_url, zeron_name in Achievement.ZERONS:
            if self.zeron_image_url == img_url:
                # set the greeting
                greeting = (
                    f"I'm {zeron_name}. " + "Thanks for helping to save the planet!"
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
        category_to_zerons = dict(zip(category_abbreviations, Achievement.ZERONS))
        # find the right choice of zeron, given the category
        zeron_img_paths, zeron_model_name = category_to_zerons[category]
        return zeron_img_paths

    def reduce_footprint(self, current_footprint):
        """Decrease the current footprint of a user as appropiate."""
        #  compute the new footprint value
        new_footprint = current_footprint - (
            self.mission.percent_carbon_sequestration
            * self.mission.question.carbon_value
        )
        return round(new_footprint, 4)

    def calculate_new_footprint(self, has_user=True):
        """
        Return the new carbon footprint, with the Achievement now won.

        Parameter:
        has_user(bool): tells the method if it's being called for an
                        authenticated user, or not

        Returns: float: new footprint value

        """
        current_footprint = 0
        # calculate the new footprint for the user
        if has_user is True:
            current_footprint = self.profile.users_footprint
        # calculate the overall footprint for a quiz (unauthenticated user)
        else:  # has_user is False
            current_footprint = self.quiz.carbon_value_total
        # return the new footprint value
        return self.reduce_footprint(current_footprint)

    def save(self, user=None, *args, **kwargs):
        """Saves a new instance of the Achievement model.

        Parameters:
        user(User): if this function is called on signup, then
                    we pass this is in order to let the method
                    know that the User's profile has no previous
                    footprint

        Returns: None

        """

        def generate_unique_id():
            """Ensures that a the new secret id is unique."""
            # get a set of all existing ids
            ids = set([a.id for a in Achievement.objects.all()])
            # init a secret id
            new_id = utils.get_random_secret_key()
            # make sure it is unique
            while new_id in ids:
                new_id = utils.get_random_secret_key()
            return new_id

        def update_profile_footprint():
            """
            Whenever an Achievement with a relationship to a Profile is
            saved, we update the total carbon footprint of that user.
            """
            # if this method called on a signup
            if user is not None and self.profile.users_footprint == 0:
                # increase the profile's footprint
                self.profile.users_footprint += self.quiz.carbon_value_total
            # calculate the new footprint
            new_footprint = self.calculate_new_footprint()
            # decrease the profile's footprint
            self.profile.users_footprint = new_footprint
            self.profile.save()
            return None

        # get the unique secret id, make it URL safe
        secret_id = slugify(generate_unique_id())
        # set it on the new model instance
        self.secret_id = secret_id
        # update the impacted user's carbon footprint
        if self.profile is not None:
            update_profile_footprint()
        return super(Achievement, self).save(*args, **kwargs)
