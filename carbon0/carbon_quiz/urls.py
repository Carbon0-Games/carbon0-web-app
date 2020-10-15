from django.urls import path

from .views import (
    QuizCreate,
    QuizDetail,
    MissionDetail,
    AchievementCreate,
    AchievementDetail,
)

app_name = "carbon_quiz"

# save a variable to abbreviate one of the longer paths
achievement_create_path = (
    "achievement/create/<int:mission_id>/" + "<int:chosen_link_index>/<slug:quiz_slug>/"
)

# define the URL paths for the views in this module
urlpatterns = [
    path("", QuizCreate.as_view(), name="quiz_create"),
    path(
        "<slug:slug>/answer-question/<int:question_number>/",
        QuizDetail.as_view(),
        name="quiz_detail",
    ),
    path(
        "mission/<int:pk>/<slug:quiz_slug>/",
        MissionDetail.as_view(),
        name="mission_detail",
    ),
    path("mission/<int:pk>/", MissionDetail.as_view(), name="mission_detail"),
    path(
        achievement_create_path, AchievementCreate.as_view(), name="achievement_create"
    ),
    path(
        "achievement/create/<int:mission_id>/<int:chosen_link_index>/",
        AchievementCreate.as_view(),
        name="achievement_create",
    ),
    path(
        "achievement/details/<int:pk>/",
        AchievementDetail.as_view(),
        name="achievement_detail",
    ),
]
