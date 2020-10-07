from django.db import models
from carbon0 import settings
from django.urls import reverse
from django.conf import settings

# from carbon_quiz.models.achievement import Achievement


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    mugshot = models.ImageField(upload_to='images/',
                                null=True, blank=True,
                                help_text="User profile image")
    phone = models.CharField(max_length=20, null=True, blank=True)
    users_footprint = models.FloatField(
        default=0,
        help_text="The total carbon footprint of the User across all quizzes."
    )

    def __str__(self):
        '''Return the related User's username.'''
        return f"{self.user.username}'s Profile"

    def get_absolute_url(self):
        '''Returns a fully qualified path for user profile.'''
        pass

    def get_related_missions_and_questions(self):
        '''Return all Missions and Question instances related to this user.'''
        # get all the related achievements
        achievements = Achievement.objects.filter(profile=self)
        # make a list of all the related Missions
        missions = [a.mission for a in achievements]
        # make a list of related Questions
        questions = [m.question for m in missions]
        # return missions and questions
        return missions, questions

    def increase_user_footprint(self, quiz):
        """When a Quiz is completed, add the total carbon value
           to the User's profile.

           Parameters:
           quiz(Quiz): the Quiz which the user has just finished

           Returns: None

        """
        self.users_footprint += quiz.carbon_value_total
        self.save()
        return None
