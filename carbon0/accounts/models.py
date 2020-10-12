from django.db import models
from carbon0 import settings
from django.urls import reverse
from django.conf import settings


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
