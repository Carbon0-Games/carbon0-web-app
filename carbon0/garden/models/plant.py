from django.db import models

from .leaf import Leaf


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
    leaf = models.ForeignKey(
        Leaf,
        null=True,
        blank=True,
        help_text="Leaves of this plant.",
        on_delete=models.PROTECT,
    )

    def __str__(self):
        """Return a string representation, show relation to the Profile."""
        return f"{self.profile.username}'s Plant {self.id}"
