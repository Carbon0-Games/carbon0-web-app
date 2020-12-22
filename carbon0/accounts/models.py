from django.db import models
from carbon0 import settings
from django.urls import reverse
from django.conf import settings

from carbon_quiz.models.mission import Mission
from carbon_quiz.models.question import Question


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    mugshot = models.ImageField(
        upload_to="images/", null=True, blank=True, help_text="User profile image"
    )
    phone = models.CharField(max_length=20, null=True, blank=True)
    users_footprint = models.FloatField(
        default=0,
        help_text="The total carbon footprint of the User across all quizzes.",
    )
    diet_level = models.IntegerField(
        default=0,
        choices=Mission.PRIORITIES,
        help_text=("Which level of Diet Missions to recommend" + " for this player."),
    )
    diet_missions_completed = models.IntegerField(
        default=0, 
        help_text="Used to decide when to increase Player's Diet Level."
    )
    diet_sign_photo = models.ImageField(
        upload_to="images/", null=True, blank=True, 
        help_text="User's sign for their Diet Missions."
    )
    transit_level = models.IntegerField(
        default=0,
        choices=Mission.PRIORITIES,
        help_text=(
            "Which level of Transit Missions to recommend" + " for this player."
        ),
    )
    transit_missions_completed = models.IntegerField(
        default=0, 
        help_text="Used to decide when to increase Player's Transit Level."
    )
    transit_sign_photo = models.ImageField(
        upload_to="images/", null=True, blank=True, 
        help_text="User's sign for their Transit Missions."
    )
    recycling_level = models.IntegerField(
        default=0,
        choices=Mission.PRIORITIES,
        help_text=(
            "Which level of Recycling Missions to recommend" + " for this player."
        ),
    )
    recycling_missions_completed = models.IntegerField(
        default=0, 
        help_text="Used to decide when to increase Player's Recycling Level."
    )
    recycling_sign_photo = models.ImageField(
        upload_to="images/", null=True, blank=True, 
        help_text="User's sign for their Recycling Missions."
    )
    offsets_level = models.IntegerField(
        default=0,
        choices=Mission.PRIORITIES,
        help_text=(
            "Which level of Airlines-Utilities Missions to recommend"
            + " for this player."
        ),
    )
    offset_missions_completed = models.IntegerField(
        default=0, 
        help_text="Used to decide when to increase Player's Offset Level."
    )
    offsets_sign_photo = models.ImageField(
        upload_to="images/", null=True, blank=True, 
        help_text="User's sign for their Airline-Utilities Missions."
    )
    utilities_level = models.IntegerField(
        default=0,
        choices=Mission.PRIORITIES,
        help_text=(
            "Which level of Utilities Missions to recommend" + " for this player."
        ),
    )
    utilities_missions_completed = models.IntegerField(
        default=0, 
        help_text="Used to decide when to increase Player's Utilities Level."
    )
    utilities_sign_photo = models.ImageField(
        upload_to="images/", null=True, blank=True, 
        help_text="User's sign for their Utilities Missions."
    )
    photos_are_accurate = models.BooleanField(
        default=False, help_text=(
            "Whether or not the signs the player has " +
            "are valid."
        )
    )

    def __str__(self):
        """Return the related User's username."""
        return f"{self.user.username}'s Profile"

    def get_absolute_url(self):
        """Returns a fully qualified path for user profile."""
        pass

    def increase_user_footprint(self, quiz):
        """When a Quiz is completed, add the total carbon value
        to the User's profile.

        Parameters:
        quiz(Quiz): the Quiz which the user has just finished

        Returns: None

        """
        # add by the half, because this function is called twice
        self.users_footprint += quiz.carbon_value_total / 2
        self.save()
        return None

    def get_player_level(self, category):
        """
        Return the Profile's current level for a certain Question category.
        """
        # make a dict of all the Question categories and the profile's levels
        levels = [
            self.diet_level,
            self.transit_level,
            self.recycling_level,
            self.offsets_level,
            self.utilities_level,
        ]
        # get a list of the category abbreivations
        categories = [abbreviation for abbreviation, full in Question.CATEGORIES]
        category_level = dict(zip(categories, levels))
        # return the level value for the given category parameter
        return category_level[category]

    def increment_player_level(self, category):
        """
        Increase the Profile's current level for a certain Question category.
        """
        # list the profile's levels, order corresponds to Question categories
        levels = [
            (self.diet_missions_completed, self.diet_level),
            (self.transit_missions_completed, self.transit_level),
            (self.recycling_missions_completed, self.recycling_level),
            (self.offset_missions_completed, self.offsets_level),
            (self.utilities_missions_completed, self.utilities_level),
        ]
        # iterate over the categories until we hit a match
        for index, question_category in enumerate(Question.CATEGORIES):
            # get the no. of Missions and level the Profile currently has
            current_missions_complete, current_level = levels[index]
            if category == question_category:
                # increment number of missions completed for specific category
                levels[index][0] = current_missions_complete + 1
                # increment the category level for every 3 Achievements
                if (current_missions_complete + 1) % 3 == 0:
                    levels[index][1] = current_level + 1
                # save and exit the function
                self.save()
                return None

    @classmethod
    def get_fields_to_track_mission(cls, mission):
        """Return the fields the MissionTracker view (accounts.views) needs
        to include on the form, so it's specific to whatever is the category 
        of the Mission. 

        Parameters:
        mission(Mission): the mission being tracked

        Returns: List: the fields needed on the form

        """
        # map the fields needed in the form, in order by Question categories
        form_fields = [
            'diet_sign_photo',
            'transit_sign_photo',
            'recycling_sign_photo',
            'offsets_sign_photo',
            'utilities_sign_photo',
        ]
        categories = [
            category_abbreviation for category_abbreviation, full_name
            in Question.CATEGORIES
        ]
        category_form_fields = dict(zip(categories, form_fields))
        # use the mission category to figure out which fields go in the form
        fields = [
            'photos_are_accurate',
            category_form_fields[mission.question.category]
        ]
        return fields
