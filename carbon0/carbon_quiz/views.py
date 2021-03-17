from heapq import nlargest
import random
from typing import Any, Dict

from django.conf import settings
from django.db.models import F
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import (
    CreateView,
    UpdateView,
)
from django.views.generic import ListView
from django.views.generic.base import View
from mixpanel import Mixpanel, MixpanelException

from .forms import AchievementForm, QuizForm
from .models.link import Link
from .models.mission import Mission
from accounts.models.profile import Profile
from .models.question import Question
from .models.quiz import Quiz
from .models.achievement import Achievement
from django.conf import settings


def track_achievement_creation(achievement, user):
    """Logs the creation of a new Achievement,
    and its player if they're logged in.

    Parameter:
    achievement(Achievement): the Achievement being created
    user(User): the user earning the Achievement

    Returns: None

    """
    # instantiate the Mixpanel tracker
    mp = Mixpanel(settings.MP_PROJECT_TOKEN)
    # Set the properties
    properties = dict()
    properties["achievementType"] = achievement.mission.question.category
    # set the user property
    if user.is_authenticated:
        properties["user"] = user.username
    else:  # user is not authenticated
        properties["user"] = "visitor"
    # track the event
    try:
        mp.track(
            properties["user"], event_name="createAchievement", properties=properties
        )
    # let Mixpanel fail silently in the dev environment
    except MixpanelException:
        pass
    return None


def filter_completed_missions(missions, user):
    """Given a set of missions and a user, return only non-completed missions.

    Parameters:
    missions: QuerySet of Missions
    user: can be authenticated or not

    Returns: set of Missions
             if the user is not authenticated,
             we return all the same missions

    """
    # if the user is signed in
    if user.is_authenticated:
        # get all the Missions related to a user,
        achievements = Achievement.objects.filter(profile=user.profile)
        user_missions = set([a.mission for a in achievements])
        # get only the missions not yet completed by the user
        missions = set(missions) - user_missions
    return missions


def get_domain(request: HttpRequest) -> str:
    """
    Uses meta data about the request to tell us what the domain
    of the server is, and whether we are using HTTP/HTTPS.
    """
    domain = request.META["HTTP_HOST"]
    # prepend the domain with the application protocol
    if "localhost" in settings.ALLOWED_HOSTS:
        domain = f"http://{domain}"
    else:  # using a prod server
        domain = f"https://{domain}"
    return domain


def get_missions_for_journey(missions, player_level, category):
    """
    Given a profile and a category, return Missions appropiate for the player.

    Parameters:
    missions(QuerySet<Mission>): all non-completed missions
    player_level(int): level of the player in one of the 5 cateogories
    category(str): one of the choices in the Question.CATEGORIES
                    array. If provided, we need to provide Missions
                    in a specific category

    Returns: list of Missions in that category, <= the priority level

    """
    # get all Questions related to the category
    category_questions = Question.objects.filter(
        category=category, is_quiz_question=True
    )
    # keep only Missions related those Questions
    missions = [
        m
        for m in missions
        if m.question in category_questions and m.priority_level <= player_level
    ]
    # take the first 3 that meet the priority level, or progressively lower
    return nlargest(3, missions, key=lambda x: x.priority_level)


class QuizCreate(CreateView):
    """View to create new Quiz instance from randomly picked questions."""

    model = Quiz
    fields = []
    template_name = "carbon_quiz/quiz/create.html"
    queryset = Question.objects.filter(is_quiz_question=True)

    def generate_random_question(self, category):
        """Gets a Question model in a specific category randomly."""
        category_questions = Question.objects.filter(
            category=category, is_quiz_question=True
        )
        return random.sample(set(category_questions), 1)[0]

    def form_valid(self, form):
        """Initializes the Questions the user will answer on the Quiz."""
        # get random questions - 2 in each category, in two sets
        quiz_questions = list()
        for category in Question.CATEGORIES:
            # get the value stored for the category field on the model
            category_value, category_full_name = category
            # get a Question instance in that category
            next_question = self.generate_random_question(category_value)
            # add the id of the Question to the list
            quiz_questions.append(next_question.id)
        # set the questions list on the model
        form.instance.questions = quiz_questions
        # make the title of the model
        num_quizzes = len(Quiz.objects.all())
        form.instance.title = f"New Quiz {num_quizzes + 1}"
        return super().form_valid(form)


class QuizDetail(UpdateView):
    """Displays questions on the quiz to answer, or the missions to complete."""

    model = Quiz
    quiz_template_name = "carbon_quiz/quiz/detail.html"
    mission_template_name = "carbon_quiz/mission/results.html"
    queryset = Quiz.objects.all()
    form_class = QuizForm

    def get(self, request, slug, question_number):
        """
        Renders a page to show the question currently being asked, or the
        missions relevant for the User to complete.

        Parameters:
        request(HttpRequest): the GET request sent to the server
        slug(slug): unique slug value of the Quiz instance
        question_number(int): the number of the question in the quiz

        Returns:
        HttpResponse: the view of the detail template for the Quiz

        """

        def display_quiz_question(quiz):
            """
            Gets the current question to display on the quiz.
            Return the name of the template for quiz questions.
            """
            # get the current Question
            question_obj = quiz.get_current_question()
            # set the addtional key value pairs to the context
            key_value_pairs = [
                ("question", question_obj),
            ]
            return key_value_pairs, self.quiz_template_name

        def display_mission_results(user):
            """
            Gets Missions to best match the user's answers to the quiz.
            Return the name of the template for resulting missions.
            """
            # set a bool for if Missions are random (decided based on auth)
            is_random = False
            missions = list()
            # if the user is logged in, acculmulate their total footprint
            if request.user.is_authenticated is True:
                # get the User profile
                profile = Profile.objects.get(user=user)
                # update their profile's footprint
                profile.increase_user_footprint(quiz)
                # find the missions the user can choose
                missions = quiz.get_related_missions(request.user.profile)
            else:  # choose missions randomly for site visitors
                # if no missions to suggest, give 3 randomly (don't require auth)
                missions = Mission.objects.filter(needs_auth=False)
                missions = random.sample(set(missions), 3)
                is_random = True
            # finally, take out missions completed before
            missions = filter_completed_missions(missions, request.user)
            # set the additional key value pairs
            key_value_pairs = [
                ("missions", missions),  # possible missions for the user
                ("is_random", is_random),
            ]
            return key_value_pairs, self.mission_template_name

        # get the Quiz instance
        quiz = Quiz.objects.get(slug=slug)
        # set the context
        context = {"quiz": quiz}
        # init the other key value pairs, which we will set later
        additional_key_value_pairs = list()
        # if the next question needs to be shown
        if quiz.active_question < 5:
            # get the current Question
            additional_key_value_pairs, template_name = display_quiz_question(quiz)
        # otherwise show the mission start page
        else:  #  quiz.active_question == 5:
            additional_key_value_pairs, template_name = display_mission_results(
                request.user
            )
        # add the Mixpanel token
        additional_key_value_pairs.append(
            ("MP_PROJECT_TOKEN", settings.MP_PROJECT_TOKEN)
        )
        # add additional key value pairs to the context
        context.update(additional_key_value_pairs)
        # return the response
        return render(request, template_name, context)

    def form_valid(self, form, slug):
        # get the Quiz and current Question
        quiz = Quiz.objects.get(slug=slug)
        question_obj = quiz.get_current_question()
        # increment the total carbon value of this quiz so far
        quiz.increment_carbon_value(question_obj)
        # increment the active_question for the next call
        quiz.increment_active_question()
        # add to the Quiz model's answers, and redirect to the next page
        new_answer = form.cleaned_data["open_response_answers"][0]
        quiz.open_response_answers.append(new_answer)
        quiz.save()
        return HttpResponseRedirect(quiz.get_absolute_url())

    def post(self, request, slug, question_number):
        """
        Processes the response to an open response question,
        and moves on to the next part of the quiz.

        Parameters:
        request(HttpRequest): the GET request sent to the server
        slug(slug): unique slug value of the Quiz instance
        question_number(int): the number of the question in the quiz

        Returns:
        HttpResponseRedirect: the view of the detail template for the Quiz

        """
        form = self.form_class(request.POST)
        if form.is_valid():
            return self.form_valid(form, slug)
        else:
            return self.form_invalid(form)


class MissionList(ListView):
    """Displays all the Missions not yet completed by the user,
       and are separate from the gardening missions.
    """

    model = Mission
    queryset = Mission.objects.filter(plant__isnull=True)
    # reuse the QuizDetail template, for when question is not in the context
    template_name = "carbon_quiz/mission/list.html"

    def get(self, request, pk=None, category=None):
        """Return a view of missions the Player should complete next, or
        all of them if the user is not authenticated.

        request(HttpRequest): carries the user as a property
        pk(int): id of a Profile
        category(str): one of the choices in the Question.CATEGORIES
                       array. If provided, we need to provide Missions
                       in a specific category

        Returns: HttpResponse: the view of the QuizDetail template

        """
        # get only the missions not yet completed by the user
        missions = filter_completed_missions(self.queryset, request.user)
        # get the Profile, as well as it's level in the category
        if pk is not None:
            profile = Profile.objects.get(id=pk)
            player_level = profile.get_player_level(category)
            # player has completed all Missions - time for special Zeron!
            if len(missions) == 0:
                # make an Achievement, w/ the tree zeron
                new_achievement = Achievement.objects.create(
                    profile=profile, zeron_image_url=settings.TREE_ZERON_PATHS
                )
                new_achievement.save()
                # redirect to the AchievementDetail view
                return HttpResponseRedirect(new_achievement.get_absolute_url())
            # choose missions based on the player journey
            elif player_level is not None and category is not None:
                missions = get_missions_for_journey(missions, player_level, category)
        # set the context
        context = {
            "missions": missions,
            "MP_PROJECT_TOKEN": settings.MP_PROJECT_TOKEN,
        }
        # return the response
        return render(request, self.template_name, context)


class MissionDetail(DetailView):
    """Represents the view the user gets to complete their Mission."""

    model = Mission
    template_name = "carbon_quiz/mission/detail.html"

    def get(self, request, pk, quiz_slug=None):
        """
        Renders a page to show the Mission currently being completed.

        Parameters:
        request(HttpRequest): the GET request sent to the server
        pk(id): unique slug value of the Mission instance

        Returns:
        HttpResponse: the view of the detail template for the Mission

        """
        # get the mission object
        mission = Mission.objects.get(id=pk)
        # get the links related to the mission
        links = Link.objects.filter(mission=mission)
        # set the context
        context = {"mission": mission, "links": links}
        # add the quiz_slug if appropiate
        if quiz_slug is not None:
            context["quiz_slug"] = quiz_slug
        # return the response
        return render(request, self.template_name, context)


class AchievementCreate(CreateView):
    """Creates the award the user gets for completing a mission."""

    model = Achievement
    # fields = ['mission_response']
    form_class = AchievementForm
    template_name = "carbon_quiz/achievement/create.html"
    queryset = Achievement.objects.all()

    def get(self, request, mission_id, quiz_slug=None):
        """
        Renders a page to show the question currently being asked.
        Assume we only want the first link related to a mission.

        Parameters:
        request(HttpRequest): the GET request sent to the server
        mission_id(int): unique slug value of the Quiz instance

        Returns:
        HttpResponse: the view of the detail template for the Achievement
                      (to be created)

        """
        # get the mission object
        mission = Mission.objects.get(id=mission_id)
        # init the context
        context = {"mission": mission}
        # add links (URL address), if that's what the mission needs
        link_descriptions, link_addresses = Link.get_mission_links(mission)
        if len(link_addresses) > 0:
            # add to the context
            context["link_address"] = link_addresses[0]
        # do the same for the link descriptions
        if len(link_descriptions) > 0:
            # add to the context
            context["link_description"] = link_descriptions[0]
        # return the response
        return render(request, self.template_name, context)

    def form_valid(self, form, mission_id, quiz_slug, user):
        """Instaniates a new Achievement model."""
        # get the related Mission model
        mission = Mission.objects.get(id=mission_id)
        # set it on the new Achievement
        form.instance.mission = mission
        # set the url of the Zeron image field
        form.instance.zeron_image_url = Achievement.set_zeron_image_url(mission)
        # set the answer to the mission, if present
        if "mission_answer" in form:
            form.instance.mission_response = form.cleaned_data["mission_answer"]
        # track the event in Mixpanel
        track_achievement_creation(form.instance, user)
        # if it's available, set the quiz relationship on the new instance
        if quiz_slug is not None:
            # get the Quiz
            quiz = Quiz.objects.get(slug=quiz_slug)
            # connect the new Achievement to the Quiz
            form.instance.quiz = quiz
        return super().form_valid(form)

    def post(self, request, mission_id, quiz_slug=None):
        """
        Passes the id of the Mission the Achievement is for,
        as part of the POST request.

        Parameters:
        request(HttpRequest): the GET request sent to the server
        mission_id(int): unique slug value of the Quiz instance

        Returns:
        HttpResponseRedirect: the view of the detail template for the Achievement
        """
        # get form needed for Achievement model instantiation
        form = self.form_class(request.POST)
        # validate
        if form.is_valid():
            # if the user is logged in
            if request.user.is_authenticated:
                # set the profile on the new instance
                form.instance.profile = request.user.profile
            # then initialize the rest of the new Achievement
            return self.form_valid(form, mission_id, quiz_slug, request.user)
        # or redirect back to the form
        else:
            return super().form_invalid(form)


class AchievementDetail(DetailView):
    """Displays the award the user receives for completing a Mission."""

    model = Achievement
    template_name = "carbon_quiz/achievement/detail.html"

    def get(self, request, pk):
        """
        Renders the view of the Achievement, specifically the zeron.

        Parameters:
        request(HttpRequest): the GET request sent to the server
        pk(id): unique slug value of the Achievement instance

        Returns:
        HttpResponse: the view of the detail template for the Achievement

        """
        # get the achievement object for the context
        achievement = Achievement.objects.get(id=pk)
        # add achievment pk to request session
        request.session["achievement_pk"] = pk
        # set the context
        context = {
            "achievement": achievement,
            "app_id": settings.FACEBOOK_SHARING_APP_ID,
        }
        # set the images needed for the context
        browser_zeron_model = achievement.zeron_image_url[0]  # .glb file path
        ios_zeron_model = achievement.zeron_image_url[1]  # .usdz file path
        # add to context, if we have an environment that has env variables
        if not (browser_zeron_model is None or ios_zeron_model is None):
            context.update(
                [
                    ("browser_model", browser_zeron_model),
                    ("ios_model", ios_zeron_model),
                ]
            )
        # if the user is authenticated
        if request.user and request.user.is_authenticated:
            # show their profile's footprint (already be authenicated)
            context["profile"] = achievement.profile
        # otherwise get the quiz related to the achievement
        else:  # user requesting the view is not logged in
            context["quiz"] = achievement.quiz
        # return the response
        return render(request, self.template_name, context)


class MissionTracker(View):
    """
    Where the player is sent to once they enter the "Track Mission" feature,
    to find the QR codes of different tracking missions.
    """

    template_name = "carbon_quiz/tracker/print_qr_codes.html"

    def get_tracking_categories(self):
        """
        Returns a list of the Mission category types
        which currently have tracking missions.
        """
        # A: init the output
        tracking_categories = list()
        # B: map the Question categories to the Mission categories
        categories = dict(
            zip(Question.get_category_abbreviations(), Mission.CATEGORIES)
        )
        # C: filter all the tracking Missions
        tracking_missions = Mission.objects.filter(
            needs_auth=True, needs_scan=True, plant__isnull=True
        )
        # D: see which Mission categories have tracking missions
        for question_category in categories.keys():
            # look up tracking missions in this cateogory
            missions = tracking_missions.filter(question__category=question_category)
            # if they are found, add the category
            if len(missions) > 0:
                mission_category = categories[question_category]
                tracking_categories.append(mission_category)
        # E: return the categories
        return tracking_categories

    def get(self, request):
        """
        Display a series of links to the form, where the user can track their
        Mission.

        Parameters:
        request(HttpRequest): the GET request sent to the server

        Returns: HttpResponse: a view of the template
        """
        # init the context
        context = dict()
        context["domain"] = get_domain(request)
        context["missions"] = Mission.objects.filter(
            needs_scan=True, needs_auth=True, plant__isnull=True
        )
        # return the context
        return render(request, self.template_name, context)
