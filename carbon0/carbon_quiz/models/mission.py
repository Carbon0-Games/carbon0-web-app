import random
from django.conf import settings
from django.db import models

from .question import Question


class Mission(models.Model):
    """Represents a possible action the user takes to help the environment."""

    title = models.CharField(
        max_length=500, unique=True, help_text="Title of the mission.", null=True
    )
    action = models.CharField(
        max_length=500, null=True, help_text="Describes what the user needs to do."
    )
    clicks_needed = models.IntegerField(
        default=1, help_text="Number of the links user needs to click."
    )
    learn_more = models.TextField(
        help_text="Explains why the mission matters.", null=True, blank=True
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.PROTECT,
        help_text="The question to which this mission relates.",
    )
    percent_carbon_sequestration = models.FloatField(
        default=0.00,
        help_text=(
            "The percent of the user's carbon footprint that "
            + "completing this mission will offset. Entered in as a float "
            + "e.g. if the value entered here is 0.97, that means 97%."
        ),
    )
    is_stationary = models.BooleanField(
        default=False,
        help_text=(
            "Does the player need to get off the " + "couch to complete the mission?"
        ),
    )
    is_paid = models.BooleanField(
        default=False,
        help_text=("Does it cost anything for the player " + "to complete the mission"),
    )
    requires_answer = models.BooleanField(
        default=False, help_text="Does this mission need a text answer?"
    )
    priority_level = models.IntegerField(
        default=0,
        help_text="The stage at which a player is ready for this mission.",
        choices=settings.PLAYER_LEVELS,
    )
    CATEGORIES = [
        "Diet-Category",
        "Transit-Category",
        "Recycling-Category",
        "Offsets-Category",
        "Utilities-Category",
    ]
    needs_auth = models.BooleanField(
        default=False, help_text="Is the mission available to unauthenticated players."
    )
    needs_scan = models.BooleanField(
        default=False, help_text="Is the mission completed by scanning a QR code."
    )

    def __str__(self):
        """Returns human-readable name of the Mission."""
        return f"{self.title}"

    @classmethod
    def get_related_mission(cls, question_obj):
        """Given a Question instance, return a related Mission randomly."""
        related_missions = Mission.objects.filter(question=question_obj)
        mission_set = random.sample(set(related_missions), 1)
        mission = mission_set.pop()
        return mission

    @classmethod
    def get_corresponding_mission_category(cls, question_category):
        """
        Gives the Mission cateogry to corresponds to one of the
        abbreviations in Question.CATEGORIES.
        """
        # use a mapping between Question and Mission categories
        question_mission_categories = dict(
            zip(Question.get_category_abbreviations(), Mission.CATEGORIES)
        )
        return question_mission_categories[question_category]
