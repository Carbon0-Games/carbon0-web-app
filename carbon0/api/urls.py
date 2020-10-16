from django.urls import path

from api.views import (
    AchievementData,
    ProfileData,
    QuizUpdate,
    QuizData,
    UserFootPrintData,
)

app_name = "api"

urlpatterns = [
    path(
        "next-question/<slug:quiz_slug>/<int:question_response>/",
        QuizUpdate.as_view(),
        name="quiz_update",
    ),
    # Data for the Bar Charts
    path(
        "achievement-data/<int:pk>/", AchievementData.as_view(), name="achievement_data"
    ),
    path("quiz-data/<int:pk>/", QuizData.as_view(), name="quiz_data"),
    path("profile-data/<int:pk>/", ProfileData.as_view(), name="profile_data"),

    path("user-footprint/", UserFootPrintData.as_view(), name="user_footprint_data"),
]
