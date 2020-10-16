import datetime as dt

from django.conf import settings
import django.contrib.auth.views as auth_views
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView
from mixpanel import Mixpanel, MixpanelException

from carbon_quiz.models.achievement import Achievement
from .forms import UserSignUpForm
from .models import Profile


# Social Auth
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.views import LoginView
from social_django.models import UserSocialAuth


def track_successful_signup(user, secret_id):
    """Logs whenever a User successfully signs up on Mixpanel.

       Parameter:
       user(User): a newly saved User model
       secret_id(str): used to determine if user
                       earned an Achievement first

       Returns: None

    """
    # instaniate the Mixpanel tracker
    mp = Mixpanel(settings.MP_PROJECT_TOKEN)
    # determine if user completed a quiz first
    earned_achievement = (secret_id is not None)
    # Tracks the event and its properties
    try:
        mp.track(user.username, 'signUp', {
            'achievementEarned': earned_achievement,
        })
        # make a User profile for this person on Mixpanel
        mp.people_set(
            user.username, {
            '$email': user.email,
            '$phone': '',
            'logins': []
            }, 
            # ignore geolocation data
            meta = {'$ignore_time' : 'true', '$ip' : 0}
        )
    # TODO: figure out why Mixpanel throws an exception on some environments
    except MixpanelException:
        # log the error happened on the Terminal
        print('MixpanelException occurred!')
    return None


def track_login_event(user):
    """Appends the time of the user's login, to their
       Mixpanel profile.

       Parameter: user(User) - person who's logging in

       Returns: None

    """
    # instaniate the Mixpanel tracker
    mp = Mixpanel(settings.MP_PROJECT_TOKEN)
    # add the date of the login, in the User's Mixpanel profile
    try:
        mp.people_append(user.username, {
            'logins' : dt.datetime.now()
        })
    # TODO: figure out why Mixpanel throws an exception on some environments
    except MixpanelException:
        # log the error happened on the Terminal
        print('MixpanelException occurred!')
    return None


class UserCreate(SuccessMessageMixin, CreateView):
    """Display form where user can create a new account."""

    form_class = UserSignUpForm
    success_url = reverse_lazy("accounts:login")
    template_name = "accounts/auth/signup.html"
    success_message = "Welcome to Carbon0! You may now log in."

    def form_valid(self, form, secret_id, request):
        '''Save the new User, and a new Profile for them, in the database.'''
        # save a new user from the form data
        self.object = form.save()
        # track the signup in Mixpanel
        track_successful_signup(self.object, secret_id)
        # save a new profile for the user
        profile = Profile.objects.create(user=self.object)
        profile.save()
        # connect this profile to the achievement, if applicable
        if secret_id is not None:
            achievement = Achievement.objects.get(secret_id=secret_id)
            achievement.profile = profile
            achievement.save(user=request.user)
        return super().form_valid(form)

    def post(self, request, secret_id=None):
        """
        Passes the id of the Achievement the profile should include, if any.

        Parameters:
        request(HttpRequest): the POST request sent to the server
        secret_id(str): unique value on one of the Achievement instances

        Returns:
        HttpResponseRedirect: the view of the Login template
        """
        # init the object property
        self.object = None
        # get form needed for Achievement model instantiation
        form = self.get_form()
        # validate, then create
        if form.is_valid():
            return self.form_valid(form, secret_id, request)
        # or redirect back to the form
        else:
            return super().form_invalid(form)



class LoginView(auth_views.LoginView):
    '''Subclass of LoginView.'''
    def form_valid(self, form):
        '''Tracks login events in Mixpanel, after security checks.'''
        # get the user
        user = form.get_user()
        # track the login in Mixpanel
        track_login_event(user)
        return super().form_valid(form)

class SettingsView(LoginRequiredMixin, TemplateView):
    """
    Currently shows the user info from social signup or login
    """

    def get(self, request, *args, **kwargs):
        user = request.user

        try:
            facebook_login = user.social_auth.get(provider="facebook")
        except UserSocialAuth.DoesNotExist:
            facebook_login = None

        try:
            google_login = user.social_auth.get(provider="google-oauth2")
        except UserSocialAuth.DoesNotExist:
            google_login = None

        # track the login in Mixpanel
        track_login_event(user)
        
        return render(request, 'accounts/auth/settings.html', {
            'facebook_login': facebook_login,
            'google_login': google_login,
        })
      

def create_social_user_with_achievement(request, user, response, *args, **kwargs):
    """
    Attach achievement to user if they sign up with their social media account

    Parameters:
        request(HttpRequest): passes the request into this function
        user: the social auth user
        response: the response from authenticating on social media
        **kwargs: returned dictionary of content when user completes social auth

    """

    # checks to see if the user is new then create a profile else just log them in
    if kwargs["is_new"]:
        profile = Profile.objects.create(user=user)
        profile.save()

        # checking to make sure there's a achievement_pk in request.session
        if "achievement_pk" in request.session:
            pk = request.session["achievement_pk"]
            achievement = Achievement.objects.get(id=pk)
            achievement.profile = profile
            achievement.save(user=request.user)
            # track the signup in Mixpanel
            track_successful_signup(user, 'achievement earned!')
        else:  # user signed up with social, but not after earning Achievement
            # track the signup in Mixpanel
            track_successful_signup(user, None)
            print("woops")
