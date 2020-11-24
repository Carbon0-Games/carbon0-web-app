import random
from django.contrib.postgres.fields import ArrayField
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
            "Does the player need to get off the " +
            "couch to complete the mission?"
            ),
    )
    is_paid = models.BooleanField(
        default=False,
        help_text=(
            "Does it cost anything for the player " +
            "to complete the mission"
        ),
    )
    requires_answer = models.BooleanField(
        default=False, help_text="Does this mission need a text answer?"
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
