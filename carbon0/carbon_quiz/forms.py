from django.forms import ModelForm

from .models.quiz import Quiz


class QuizForm(ModelForm):
    """Used to generate a quiz."""

    class Meta:
        model = Quiz
        fields = [
            'open_response_answers'
        ]
