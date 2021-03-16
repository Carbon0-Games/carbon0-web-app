from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from accounts.models.profile import Profile


class Plant(models.Model):
    """A plant that a user keeps in their personal garden at home."""

    nickname = models.CharField(
        max_length=5000, help_text="What do you call this plant?"
    )
    slug = models.CharField(
        max_length=500,
        unique=True,
        null=True,
        blank=True,
        help_text="Unique parameter to specify the Plant in the URL path.",
    )
    common_name = models.CharField(
        max_length=5000,
        help_text="What species is this plant, if you know?",
        null=True,
        blank=True,
    )
    is_edible = models.BooleanField(
        null=True,
        default=False,
        help_text="Are you growing this plant to grow your own food?",
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
        Profile,
        null=True,
        # even if user leaves, we can train the AI on their images to improve
        on_delete=models.SET_NULL,
        help_text="The user who owns this plant.",
    )
    created = models.DateTimeField(auto_now=True)
    amount_harvested_total = models.FloatField(
        default=0,
        help_text="How much produce did you harvest this \
        season from your garden (in pounds)?"
    )


    def __str__(self):
        """Return a string representation, show relation to the Profile."""
        return f"{self.nickname}'s Plant {self.id}"

    def get_absolute_url(self):
        """Returns a fully-qualified path to the PlantDetail view."""
        path_components = {"slug": self.slug}
        return reverse("garden:plant_detail", kwargs=path_components)

    def save(self, *args, **kwargs):
        """Creates a URL safe slug automatically when a new Plant is saved."""
        if not self.pk:
            num_plants = len(Plant.objects.all())
            unique_str = f"{self.nickname}-{num_plants + 1}"
            self.slug = slugify(unique_str, allow_unicode=True)
        # call save on the superclass
        return super().save(*args, **kwargs)
