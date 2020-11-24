from django.forms import ModelForm

from .models.achievement import Achievement
from .models.quiz import Quiz


class AchievementForm(ModelForm):
    """Used to generate new Achievements."""

    class Meta:
        model = Achievement
        fields = [
            'mission_response',
        ]


class QuizForm(ModelForm):
    """Used to generate a quiz."""

    class Meta:
        model = Quiz
        fields = [
            'open_response_answers'
        ]
