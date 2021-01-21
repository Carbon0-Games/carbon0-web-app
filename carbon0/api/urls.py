from django.urls import path

from api.views import (
    AchievementCreateLink,
    AchievementData,
    CategoryTrackerData,
    MissionTrackingAchievement,
    ProfileData,
    FootprintOverTime,
    QuizUpdate,
    QuizData,
    UserFootPrintData,
)

app_name = "api"

urlpatterns = [
    # Move the Quiz to the Next Question
    path(
        "next-question/<slug:quiz_slug>/<int:question_response>/",
        QuizUpdate.as_view(),
        name="quiz_update",
    ),
    # Generate Links for AchievementCreate
    path(
        "achievement-create-link/<int:mission_id>/<slug:quiz_slug>/",
        AchievementCreateLink.as_view(),
        name="achievement_create_link",
    ),
    path(
        "achievement-create-link/<int:mission_id>/",
        AchievementCreateLink.as_view(),
        name="achievement_create_link",
    ),
    path(
        "tracking-category-image/<slug:category>/",
        CategoryTrackerData.as_view(),
        name="category_tracker_data"
    ),
    # Data for the Bar Charts
    path(
        "achievement-data/<int:pk>/", AchievementData.as_view(), name="achievement_data"
    ),
    path("quiz-data/<int:pk>/", QuizData.as_view(), name="quiz_data"),
    path("profile-data/<int:pk>/", ProfileData.as_view(), name="profile_data"),
    path(
        "footprint-leaderboard/",
        UserFootPrintData.as_view(),
        name="footprint_leaderboard",
    ),
    # Data for the Footprint Over Time
    path(
        "footprint-change/<int:pk>/",
        FootprintOverTime.as_view(),
        name="footprint_change",
    ),
    # URLs for Mission Tracking
    path(
        "track-achievement/<int:mission_id>/",
        MissionTrackingAchievement.as_view(),
        name="mission_tracking_achievement",
    ),
    path(
        "track-achievement/<int:mission_id>/<int:pk>/",
        MissionTrackingAchievement.as_view(),
        name="mission_tracking_achievement",
    ),
]
