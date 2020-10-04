from django.urls import path

from api.views import QuizUpdate

urlpatterns = [
    path('next-question/<slug:quiz_slug>/<int:response_to_question>/',
         QuizUpdate.as_view(), name="quiz_update"),
]