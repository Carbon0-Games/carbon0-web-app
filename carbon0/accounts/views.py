import datetime as dt
import random

from django.conf import settings
import django.contrib.auth.views as auth_views
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView
from mixpanel import Mixpanel, MixpanelException

from carbon_quiz.models.achievement import Achievement
from carbon_quiz.models.mission import Mission
import carbon_quiz.views as cqv
from .models import Profile
from .forms import UserSignUpForm


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
    earned_achievement = secret_id is not None
    # Tracks the event and its properties
    try:
        mp.track(
            user.username,
            "signUp",
            {
                "achievementEarned": earned_achievement,
            },
        )
        # make a User profile for this person on Mixpanel
        mp.people_set(
            user.username,
            {"$email": user.email, "$phone": "", "logins": []},
            # ignore geolocation data
            meta={"$ignore_time": "true", "$ip": 0},
        )
    # let Mixpanel fail silently in the dev environment
    except MixpanelException:
        pass
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
        mp.people_append(user.username, {"logins": dt.datetime.now()})
    # let Mixpanel fail silently in the dev environment
    except MixpanelException:
        pass
    return None


class UserCreate(SuccessMessageMixin, CreateView):
    """Display form where user can create a new account."""

    form_class = UserSignUpForm
    success_url = reverse_lazy("accounts:login")
    template_name = "accounts/auth/signup.html"
    success_message = "Welcome to Carbon0! You may now log in."

    def form_valid(self, form, secret_id, request):
        """Save the new User, and a new Profile for them, in the database."""
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
    """Subclass of LoginView."""

    def form_valid(self, form):
        """Tracks login events in Mixpanel, after security checks."""
        # get the user
        user = form.get_user()
        # track the login in Mixpanel
        track_login_event(user)
        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, TemplateView):
    """
    Currently shows the user info from social signup or login
    """

    template_name = "accounts/auth/profile.html"

    def _suggest_missions(self, user):
        """Return uncompleted missions the User will most likely enjoy, 
        based on the following order:

        1. Missions in areas they need to improve on
        2. Missions in areas they have not said they need improvement in
        3. If no missions are available for 1 or 2, 
           then display 3 random missions.

        Parameter:
        user(User): the user making the request to the view
        
        Returns: 
        is_random(bool): a flag to tell us if the missions were selected 
                         randomly or not. Helps in deciding which partial 
                         templates to use on the view
        QuerySet<Mission>: the missions suggested for the user

        """

        def get_improvement_missions(achievement):
            """
            Get missions for the questions in areas
            that the user needs to improve in.
            """
            missions = list()
            if achievement is not None and achievement.quiz is not None:
                missions = achievement.quiz.get_related_missions()
            return missions

        def get_non_improvement_missions(achievement):
            """
            Get missions for the questions in areas in which the user 
            may already be strong.
            """
            missions = list()
            if achievement is not None and achievement.quiz is not None:
                missions = achievement.quiz.get_unrelated_missions()
            return missions

        # grab the most recent Achievement
        user_achievements = Achievement.objects.filter(profile=user.profile)
        latest_achievement = user_achievements.order_by("id").last()
        # grab missions for improvement questions 
        missions = get_improvement_missions(latest_achievement)
        # set a flag to track if the Missions are selectec randomly
        is_random = False
        # if failure, try to grab missions for non improvement questions
        if len(missions) == 0:
            missions = get_non_improvement_missions(latest_achievement)
        # if failure, try to grab missions randomly
        if len(missions) == 0:
            missions = random.sample(set(Mission.objects.all()), 3)
            is_random = True
        # return the missions
        return is_random, missions

    def get(self, request):
        """Display the profile page for the user."""
        # get info about the user
        user = request.user
        # track the login in Mixpanel
        track_login_event(user)
        # decide how to color the user's footprint
        is_footprint_green = False
        if user.profile.users_footprint <= 1000:
            is_footprint_green = True  # green means "Good"
        # grab missions for the context
        is_random, missions = self._suggest_missions(user)
        # define the template context
        context = {
            "is_footprint_green": is_footprint_green,
            "footprint": user.profile.users_footprint,
            "profile": user.profile,
            "is_random": is_random,
            "missions": missions
        }
        return render(request, self.template_name, context)


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

        # checks to make sure there's an achievement_pk in request.session
        if "achievement_pk" in request.session:
            pk = request.session["achievement_pk"]
            achievement = Achievement.objects.get(id=pk)
            achievement.profile = profile
            achievement.save(user=request.user)
            # track the signup in Mixpanel
            track_successful_signup(user, "achievement earned!")
        else:  # user signed up with social, but not after earning Achievement
            # track the signup in Mixpanel
            track_successful_signup(user, None)
