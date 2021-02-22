from django import forms
from .models.plant import Plant


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
