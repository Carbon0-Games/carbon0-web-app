from django import forms
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
