import os

from django.conf import settings
from django.db import models

from .plant import Plant


class Leaf(models.Model):
    date_uploaded = models.DateTimeField(
        auto_now_add=True, help_text="When the leaf image was uploaded."
    )
    # save static files related to this model in app subdirectory
    UPLOAD_LOCATION = os.path.join("garden", "images")
    image = models.ImageField(
        upload_to=UPLOAD_LOCATION, null=True, blank=True, help_text="Image of the leaf."
    )
    STATUSES = [
        ("M", "Moderate"),  # can also set this option when the model is unsure
        ("H", "Heathy"),
        ("U", "Unhealthy"),
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
        Plant,
        on_delete=models.CASCADE,
        null=True,
        help_text="The plant that this leaf came from.",
    )

    def __str__(self):
        """Return a string representation, show relation to the Profile."""
        return f"Leaf {self.id} \
            for {self.plant.profile.user.username}'s Plant {self.id}"

    @classmethod
    def get_status_mapping(cls):
        """Maps each health abbreviation to the full name of the status."""
        abbreviations, full_names = list(), list()
        for abbreviation, full_name in cls.STATUSES:
            abbreviations.append(abbreviation)
            full_names.append(full_name)
        return dict(zip(abbreviations, full_names))

    @classmethod
    def get_status_abbreviations(cls):
        """Return a list of the abbreivated health statuses."""
        return [abbreviation for abbreviation, full in cls.STATUSES]

    def get_confidence(self):
        """Returns the confidence of the health check as a percentage."""
        if self.confidence is not None:
            rounded = round(self.confidence, 3) * 100
            return f"{rounded}%"
