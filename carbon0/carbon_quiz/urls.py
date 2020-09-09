from django.urls import path

from .views import (
    QuizCreate,
)

app_name = 'carbon_quiz'

urlpatterns = [
    path('create-quiz/', QuizCreate.as_view(), name='quiz_create'),
]