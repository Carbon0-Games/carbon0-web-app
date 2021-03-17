from django import forms
from django.conf import settings

from .models.leaf import Leaf
from .models.plant import Plant


class LeafForm(forms.ModelForm):
    """A form for uploading leaf images."""

    class Meta:
        model = Leaf
        fields = ["image"]


class PlantForm(forms.ModelForm):
    """A form for adding new Plant models."""

    class Meta:
        model = Plant
        fields = [
            "nickname",
            "common_name",
            "is_edible",
            "description",
        ]


class HarvestForm(forms.Form):
    """A form for the user to record the amount of produce they grew."""

    UNITS = [("kg", "Kilograms"), ("lbs", "English Pounds")]
    measuring_unit = forms.ChoiceField(
        choices=UNITS, help_text="The unit the gardener measures produce in."
    )
    amount_harvested = forms.FloatField(
        help_text="How much produce did you harvest this \
        season from your garden (in pounds)?"
    )

    def get_harvest(self):
        """Returns amount harvested in kg, taking care of any conversions."""
        amount = self.cleaned_data.get("amount_harvested")
        if self.cleaned_data.get("measuring_unit") == "lbs":
            amount = amount * settings.POUNDS_TO_KILOGRAMS
        return amount
