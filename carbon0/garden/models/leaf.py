from django.conf import settings
from django.db import models

from .plant import Plant


class Leaf(models.Model):
    date_uploaded = models.DateTimeField(
        auto_now_add=True, help_text="When the leaf image was uploaded."
    )
    image = models.ImageField(
        upload_to="images/", null=True, blank=True, help_text="Image of the leaf."
    )
    STATUSES = [
        ("H", "Heathy"),
        ("U", "Unhealthy"),
        ("M", "Moderate"),  # can also set this option when the model is unsure
    ]
    status = models.CharField(
        max_length=1,
        choices=STATUSES,
        default="M",
        help_text="The healthiness of this leaf.",
    )
    condition = models.CharField(
        max_length=100, null=True, help_text="What the AI identified on the leaf."
    )
    confidence = models.FloatField(
        default=(1 / settings.NUM_PREDICTION_LABELS),
        help_text="How confident the AI was in its prediction.",
    )
    plant = models.ForeignKey(
        Plant, on_delete=models.CASCADE,
        null=True,
        help_text="The plant that this leaf came from."
    )

    def __str__(self):
        """Return a string representation, show relation to the Profile."""
        return f"Leaf {self.id} for {self.profile.username}'s Plant {self.id}"
