import random

from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView)

from .models import (
    Achievement,
    Mission,
    Question,
    Quiz,
)


class QuizCreate(CreateView):
    '''View to create new Quiz instance from randomly picked questions.'''
    model = Quiz
    fields = []

    def generate_random_question(self, category):
        '''Gets a Question model in a specific category randomly.'''
        category_questions = Question.objects.filter(category=category)
        return random.sample(category_questions, 1)

    def form_valid(self, form):
        '''Initializes the Questions the user will answer on the Quiz.'''
        # get random questions
        quiz_questions = list()
        for category in Question.CATEGORIES:
            # get the value stored for the category field on the model
            category_value, category_full_name = category
            # get a Question instance in that category
            next_question = self.generate_random_question(category_value)
            # add it to the list
            quiz_questions.append(next_question)
        # set the questions list on the model
        form.instance.questions = quiz_questions
        return super().form_valid(form)
