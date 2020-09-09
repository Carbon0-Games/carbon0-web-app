from django.forms import ModelForm

from .models import Quiz


class QuizForm(ModelForm):
    '''Used to generate/fill out a quiz.'''
    class Meta:
        model = Quiz
        fields = '__all__'