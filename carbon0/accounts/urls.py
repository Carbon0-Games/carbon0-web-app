from django.contrib.auth import views as auth_views
from django.urls import include, path

from .views import UserCreate, SettingsView, password

app_name = 'accounts'

urlpatterns = [
    # paths to signup, login, and logout
    path('signup/', UserCreate.as_view(), name='signup'),
    path('login/',
         auth_views.LoginView.as_view(template_name="accounts/auth/login.html"),
         name='login'),
    path('logout/',
         auth_views.LogoutView.as_view(), name='logout'),

     # User settings page
     path('settings/', SettingsView.as_view(), name='settings'),

     path('settings/password/', password, name='password'),

]
