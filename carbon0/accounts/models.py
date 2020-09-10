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
    phone = models.CharField(max_length=20, null=True)

    def __str__(self):
        '''Return the related User's username.'''
        return f"{self.user.username}'s Profile"

    def get_absolute_url(self):
        '''Returns a fully qualified path for user profile.'''
        pass
