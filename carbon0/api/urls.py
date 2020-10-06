from django.urls import path

from api.views import (
    QuizUpdate,
    QuizDetailData,
)

urlpatterns = [
    path('next-question/<slug:quiz_slug>/<int:question_response>/',
         QuizUpdate.as_view(), name="quiz_update"),
    path('quiz-data/<int:pk>/', QuizDetailData.as_view(), name='quiz_data'),
]