from django.db import models

from accounts.models.profile import Profile


class Plant(models.Model):
    """A plant that a user keeps in their personal garden at home."""

    nickname = models.CharField(
        max_length=5000, help_text="What do you call this plant?"
    )
    common_name = models.CharField(
        max_length=5000,
        help_text="What species is this plant, if you know?",
        null=True,
        blank=True,
    )
    is_edible = models.BooleanField(
        default=False, help_text="Are you growing this plant to grow your own food?"
    )
    description = models.TextField(
        null=True,
        blank=True,
        help_text=(
            "Please share anything else you'd like to add about what \
            condition your plant is in (because we care)!"
        ),
    )
    profile = models.ForeignKey(
        Profile, null=True,
        # even if user leaves, we can train the AI on their images to improve 
        on_delete=models.SET_NULL,  
        help_text="The user who owns this plant."
    )

    def __str__(self):
        """Return a string representation, show relation to the Profile."""
        return f"{self.profile.username}'s Plant {self.id}"
