from django.db import models


class Plant(models.Model):
    """A plant that a user keeps in their personal garden at home."""
    nickname = models.CharField(
        max_length=5000, help_text="What do you call this plant?"
    )
    common_name = models.CharField(
        max_length=5000, help_text="What species is this plant, if you know?",
        null=True, blank=True
    )
    is_edible = models.BooleanField(
        default=False, 
        help_text="Are you growing this plant to grow your own food?"
    )
    description = models.TextField(
        null=True, blank=True,
        help_text=(
            "Please share anything else you'd like to add about what \
            condition your plant is in (because we care)!"
        )
    )
    # TODO: connect the model with Profile, and the Leaf models
    # TODO: use Trefle API to get image of the species via slug of common name
