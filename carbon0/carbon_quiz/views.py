import random

from django.conf import settings
from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView,
)
from django.views.generic import ListView
from mixpanel import Mixpanel, MixpanelException

from .models.link import Link
from .models.mission import Mission
from accounts.models import Profile
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


class QuizCreate(CreateView):
    """View to create new Quiz instance from randomly picked questions."""

    model = Quiz
    fields = []
    template_name = "carbon_quiz/quiz/create.html"
    queryset = Question.objects.all()

    def generate_random_question(self, category):
        """Gets a Question model in a specific category randomly."""
        category_questions = Question.objects.filter(category=category)
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


class QuizDetail(DetailView):
    """Displays questions on the quiz to answer, or the missions to complete."""

    model = Quiz
    template_name = "carbon_quiz/quiz/detail.html"

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
        # get the Quiz instance
        quiz = Quiz.objects.get(slug=slug)
        # set the context
        context = {"quiz": quiz}
        # init the other key value pairs, which we will set later
        additional_key_value_pairs = list()
        # if the next question needs to be shown
        if quiz.active_question < 5:
            # get the current Question
            question_obj = quiz.get_current_question()
            # set the addtional key value pairs to the context
            additional_key_value_pairs = [
                ("question", question_obj),
            ]
        # otherwise show the mission start page
        else:  #  quiz.active_question == 5:
            # if the user is logged in, acculmulate their total footprint
            if request.user.is_authenticated is True:
                # get the User profile
                profile = Profile.objects.get(user=request.user)
                # update their profile's footprint
                profile.increase_user_footprint(quiz)
            # find the missions the user can choose
            missions = list()
            # set a flag to tell if the Missions are random
            is_random = False
            # get the question id that each user actually interacted with
            for question_id in quiz.questions:
                # check if this question was answered no (needs a mission)
                if question_id > 0:
                    # get the question
                    question_obj = Question.objects.get(id=question_id)
                    # get a random Mission related to the Question
                    related_missions = Mission.objects.filter(question=question_obj)
                    mission_set = random.sample(set(related_missions), 1)
                    mission = mission_set.pop()
                    # add to the list of Missions
                    missions.append(mission)
            # if no missions to suggest, give 3 randomly
            if len(missions) == 0:
                missions = random.sample(set(Mission.objects.all()), 3)
                is_random = True
            # finally, take out missions completed before
            missions = filter_completed_missions(missions, request.user)
            # set the additional key value pairs
            additional_key_value_pairs = [
                ("missions", missions),  # possible missions for the user
                ("is_random", is_random),
            ]
        # add the Mixpanel token
        additional_key_value_pairs.append(
            ("MP_PROJECT_TOKEN", settings.MP_PROJECT_TOKEN)
        )
        # add additional key value pairs to the context
        context.update(additional_key_value_pairs)
        # return the response
        return render(request, self.template_name, context)


class MissionList(ListView):
    """Displays all the Missions not yet completed by the user."""

    model = Mission
    queryset = Mission.objects.all()
    # reuse the QuizDetail template, for when question is not in the context
    template_name = "carbon_quiz/mission/list.html"

    def get(self, request):
        """Return a view of all missions not yet completed, or
        all of them if the user is not authenticated.

        Parameters:
        request(HttpRequest): carries the user as a property

        Returns: HttpResponse: the view of the QuizDetail template

        """
        # start with all Missions in the queryset
        missions = self.queryset
        # get only the missions not yet completed by the user
        missions = filter_completed_missions(missions, request.user)
        # set the context
        context = {
            "missions": missions,
            "is_random": False,
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
    fields = []
    template_name = "carbon_quiz/achievement/create.html"
    queryset = Achievement.objects.all()

    def get(self, request, mission_id, chosen_link_id, quiz_slug=None):
        """
        Renders a page to show the question currently being asked.

        Parameters:
        request(HttpRequest): the GET request sent to the server
        mission_id(int): unique slug value of the Quiz instance
        chosen_link_id(int): the id of the Link model we will use
                             to complete the mission

        Returns:
        HttpResponse: the view of the detail template for the Achievement
                      (to be created)

        """
        # get the mission object
        mission = Mission.objects.get(id=mission_id)
        # get the links related to the mission
        link = Link.objects.get(id=chosen_link_id)
        # set the context
        context = {"mission": mission, "link": link}
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
        # track the event in Mixpanel
        track_achievement_creation(form.instance, user)
        # if it's available, set the quiz relationship on the new instance
        if quiz_slug is not None:
            # get the Quiz
            quiz = Quiz.objects.get(slug=quiz_slug)
            # connect the new Achievement to the Quiz
            form.instance.quiz = quiz
        return super().form_valid(form)

    def post(self, request, mission_id, chosen_link_id, quiz_slug=None):
        """
        Passes the id of the Mission the Achievement is for,
        as part of the POST request.

        Parameters:
        request(HttpRequest): the GET request sent to the server
        mission_id(int): unique slug value of the Quiz instance
        chosen_link_id(int): the id of the Link model we will use
                             to complete the mission

        Returns:
        HttpResponseRedirect: the view of the detail template for the Achievement
        """
        # get form needed for Achievement model instantiation
        form = self.get_form()
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
