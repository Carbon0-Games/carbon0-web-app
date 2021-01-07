import datetime as dt
import random
from typing import Any, Dict

from django.conf import settings
import django.contrib.auth.views as auth_views
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView
from mixpanel import Mixpanel, MixpanelException

from carbon_quiz.models.achievement import Achievement
from carbon_quiz.models.mission import Mission
import carbon_quiz.views as cqv
from .forms import UserSignUpForm
from .models import Profile


# Social Auth
from django.views.generic import TemplateView, View
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


def connect_profile_achievement(secret_id, profile, request=None):
    """Finds an Achievement by using the secret_id (passed to the URL),
    then connects the model with the appropiate Profile instance.

    Parameters:
    secret_id(str): an identifier for a unique Achievement instance
    profile(Profile): connect with one of the players in the database
    request(HttpRequest): in sign ups we also pass in the user of the 
                          request, as per the args needed by the scoring
                          algorithm (see Achievement.save more details).

    Returns: None

    """
    if secret_id is not None:
        achievement = Achievement.objects.get(secret_id=secret_id)
        achievement.profile = profile
        # when request is passed in, let the save algorithm know it's a signup
        if request is not None:
            achievement.save(user=request.user)
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
        connect_profile_achievement(secret_id, profile, request=request)
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

    def get_redirect_view(self, request, secret_id=None) -> HttpResponseRedirect:
        '''Sends the user to AchievementDetail, or to the dashboard.'''
        if secret_id is not None:
            # sending user to AchievementDetail
            achievement = Achievement.objects.get(secret_id=secret_id)
            url = achievement.get_absolute_url()
            # add a message as well
            messages.add_message(
                request, messages.SUCCESS, 
                "Congratulations - you've earned a new Zeron!"
            )
            return HttpResponseRedirect(url)
        else:  # send to the dashboard
            return HttpResponseRedirect(self.get_success_url())


    def form_valid(self, request, form, secret_id):
        """Tracks login events in Mixpanel, after security checks."""
        # A: get the user
        user = form.get_user()
        # B: track the login in Mixpanel
        track_login_event(user)
        # C: get the profile, and connect it with the Achievement
        profile = Profile.objects.get(user=user)
        connect_profile_achievement(secret_id, profile)
        # D: log the user in
        login(request, user)
        # E: decide where to send the user next
        return self.get_redirect_view(request, secret_id)

    def post(self, request, secret_id=None):
        """
        Passes the id of the Achievement the profile should include, if any.

        Parameters:
        request(HttpRequest): the POST request sent to the server
        secret_id(str): unique value on one of the Achievement instances

        Returns:
        HttpResponseRedirect: the view of:
                             1) the ProfileView, if there's no secret_id
                             2) the AchievementDetail, if there is
                             3) the Login template if form validation fails

        """
        # get form needed for user authentication
        form = self.get_form()
        # validate, then create
        if form.is_valid():
            return self.form_valid(request, form, secret_id)
        # or redirect back to the form
        else:
            return super().form_invalid(form)


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
                missions = achievement.quiz.get_related_missions(user.profile)
                # get only the missions not yet completed by the user
                missions = cqv.filter_completed_missions(missions, user)
            return missions

        def get_non_improvement_missions(achievement):
            """
            Get missions for the questions in areas in which the user
            may already be strong.
            """
            missions = list()
            if achievement is not None and achievement.quiz is not None:
                missions = achievement.quiz.get_unrelated_missions()
                # get only the missions not yet completed by the user
                missions = cqv.filter_completed_missions(missions, user)
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
            "footprint": round(user.profile.users_footprint, 2),
            "profile": user.profile,
            "is_random": is_random,
            "missions": missions,
            "categories": Mission.CATEGORIES,
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


class MissionTrackerComplete(View):
    """
    Display the QR codes for all tracking missions in the
    specified category. PDF download link included as well.
    """
    template_name = "tracker/print_qr_codes.html"

    def get_tracking_missions(self, category):
            """
            Returns a list of the tracking missions in this category.
            """
            # A: init the output
            tracking_missions = list()
            # B: filter all the tracking Missions
            tracking_missions = Mission.objects.filter(
                needs_auth=True, needs_scan=True, 
                question__category=category
            )
            # C: return the missions
            return tracking_missions

    def get(self, request, category):
        """
        Get the tracking missions in the category, to 
        show them on the template comntext.

        Parameters:
        request(HttpRequest): the GET request sent to the server
        category(str): the specific category of tracking Missions.
                       NOTE: This value an abbreviations of one 
                       of the Question.CATEGORIES.

        Returns: HttpResponse: the view of the template

        """
        context = dict()
        # add the host domain to the context
        domain = request.META["HTTP_HOST"]
        # prepend the domain with the application protocol
        if "localhost" in settings.ALLOWED_HOSTS:
            domain = f"http://{domain}"
        else:  # using a prod server
            domain = f"https://{domain}"
        context["domain"] = domain
        # Add the Missions and their category to the context
        context["category"] = (
            Mission.get_corresponding_mission_category(category)
        )
        context['missions'] = self.get_tracking_missions(category)
        # send the player to the template
        return render(request, self.template_name, context)
