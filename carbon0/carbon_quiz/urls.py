from django.urls import path

from .views import (
    QuizCreate,
    QuizDetail,
)

app_name = 'carbon_quiz'

urlpatterns = [
    path('create-quiz/', QuizCreate.as_view(), name='quiz_create'),
    path('answer-question/<slug:slug>/<int:question_answered>/', 
         QuizDetail.as_view, name='quiz_detail'),

]