from django.contrib.auth import views as auth_views
from django.urls import include, path
from django.views.generic import TemplateView

from .views import (
    UserCreate,
    ProfileView,
    LeaderboardView,
    LoginView,
    MissionTrackerComplete,
)

app_name = "accounts"

urlpatterns = [
    # paths to signup
    path("signup/<slug:secret_id>/", UserCreate.as_view(), name="signup"),
    path("signup/", UserCreate.as_view(), name="signup"),
    # paths to login and logout
    path(
        "login/<slug:secret_id>/",
        LoginView.as_view(template_name="accounts/auth/login.html"),
        name="login",
    ),
    path(
        "login/",
        LoginView.as_view(template_name="accounts/auth/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    # User profile page - 'settings' is the required view function name
    path("profile/", ProfileView.as_view(), name="profile"),
    path("leaderboard/", LeaderboardView.as_view(), name="leaderboard"),
    path(
        "profile/<slug:category>/",
        MissionTrackerComplete.as_view(),
        name="mission_tracker_complete",
    ),
]
