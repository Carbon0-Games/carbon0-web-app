from django.urls import path

from .views import (
    QuizCreate,
    QuizDetail,
    MissionDetail,
    AchievementCreate,
    AchievementDetail,
)

app_name = 'carbon_quiz'

urlpatterns = [
     path('', QuizCreate.as_view(), name='quiz_create'),
     path('answer-question/<slug:slug>/', QuizDetail.as_view(), name='quiz_detail'),
     path('mission/<int:pk>/', MissionDetail.as_view(), name='mission_detail'),
     path('achievement/create/<int:mission_id>/<int:chosen_link_index>/',
          AchievementCreate.as_view(), name='achievement_create'),
     path('achievement/details/<int:pk>/', AchievementDetail.as_view(),
         name='achievement_detail'),

]
