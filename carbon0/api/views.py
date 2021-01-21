from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from rest_framework.views import APIView
from rest_framework.response import Response

import accounts.views as av
from accounts.models import Profile
from carbon_quiz.models.achievement import Achievement
from carbon_quiz.models.link import Link
from carbon_quiz.models.mission import Mission
from carbon_quiz.models.question import Question
from carbon_quiz.models.quiz import Quiz


class QuizUpdate(APIView):
    """
    Updates the questions that have been answered yes/no in the Quiz,
    and then moves to the next template.
    """

    def post(self, request, quiz_slug, question_response):
        """
        Uses the answer to the Question the user has just responded to,
        to update the array of questions related to a Quiz.

        Parameters:
        request(HttpRequest)
        quiz_slug(str): the unique slug value of one of the Quizzes
        question_response(int): 0 or 1, which means the user responded
                                   no or yes (respectively)

        Returns:
        HttpResponse: a view of the QuizDetail, with the next question,
                      or missions for the user

        """
        # get the Quiz instance
        quiz = Quiz.objects.get(slug=quiz_slug)
        # get the current Question
        question_obj = quiz.get_current_question()
        # if the user answered in a way that's good
        if question_response != question_obj.improvement_response:
            # ignore the question later, when finding missions
            quiz.questions[quiz.active_question] = 0
            quiz.previous_carbon_value = quiz.carbon_value_total
        # otherwise:
        else:
            # increment the total carbon value of this quiz so far
            quiz.previous_carbon_value = quiz.carbon_value_total
            quiz.increment_carbon_value(question_obj)
        # increment the active_question for the next call
        quiz.increment_active_question()
        # return a redirect view the next Question on the Quiz, so it updates
        path_components = {
            "slug": quiz_slug,
            # for the question number, increment zero-indexed number
            "question_number": quiz.active_question + 1,
        }
        return HttpResponseRedirect(
            reverse_lazy("carbon_quiz:quiz_detail", kwargs=path_components)
        )


class QuizData(APIView):
    """Data needed to make the bar chart on the QuizDetail view."""

    def get(self, request, pk):
        """Returns the total carbon value of a Quiz instance, given its id."""
        # get the Quiz instance
        quiz = Quiz.objects.get(id=pk)
        # structure the data
        data = {
            "labels": ["Your Carbon Footprint"],
            "footprint": [quiz.carbon_value_total],
        }
        # return the data
        return Response(data)


class ProfileData(APIView):
    """Data needed to make the bar chart on the AchievementDetail view."""

    def get(self, request, pk):
        """Return the carbon foortprint of a Profile, given its id."""
        # get the profile instance
        profile = Profile.objects.get(id=pk)
        # structure the data
        data = {
            "labels": ["Your Carbon Footprint"],
            "footprint": [profile.users_footprint],
        }
        # return the data
        return Response(data)


class AchievementData(APIView):
    """Data needed to make the bar chart on the AchievementDetail view."""

    def get(self, request, pk):
        """Return the carbon foortprint of an Achievement, given its id."""
        # get the Achievement instance
        achievement = Achievement.objects.get(id=pk)
        # structure the data
        data = {
            "labels": ["Carbon Footprint"],
            "footprint": [achievement.calculate_new_footprint(has_user=False)],
        }
        # return the data
        return Response(data)


class UserFootPrintData(APIView):
    """Returns usernames and foot print values in ascending order"""

    def get(self, request):
        all_profiles = Profile.objects.order_by("users_footprint")
        # for loop to get all user names
        players = list()
        for (i, p) in enumerate(all_profiles):
            # create the player object
            player = {
                "position": i,
                "username": p.user.username,
                "score": p.users_footprint,
            }
            # add to the list
            players.append(player)
        data = {"players": players}

        return Response(data)


class FootprintOverTime(APIView):
    def get(self, request, pk):
        """Returns JSON data on a user's carbon footprint over time.
        Parameters:
        request(HttpRequest)
        pk(int): the id of the Profile instance encapsulating the
                 user's carbon footprint data
        Return: dict: A JSON object that maps that encapsulates the
                      data points needed to plot the carbon footprint
                      data on a line chart.
        """
        # get the Profile related to the pk
        profile = Profile.objects.get(id=pk)
        # get all the Achievements related to the Profile, ordered by pk
        achievements = Achievement.objects.filter(profile=profile).order_by("id")
        # init the lists for the data and their labels
        data, labels = list(), list()
        # record the starting footprint value, and its label
        footprint = 1000
        data.append(footprint)
        labels.append("Starting Value")
        # iterate over all the Achievements
        for a in achievements:
            # if there's a related Quiz, add it first
            if a.quiz:
                # increase the footprint
                footprint += a.quiz.carbon_value_total
                # record the increase
                data.append(footprint)
                # record the label for this point
                labels.append("Completed Quiz")
            # decrease the footprint
            footprint = a.calculate_new_footprint()
            # record the new value
            data.append(footprint)
            # record the label for this point
            labels.append("Completed Mission")
        # finally, add the current user footprint
        if footprint != profile.users_footprint:
            data.append(profile.users_footprint)
            labels.append("Current Footprint")
        # return the response
        return Response(
            {"Events": labels, "Footprint": data}  # Time axis  # Vertical Axis
        )


class AchievementCreateLink(APIView):
    def get(self, request, mission_id, quiz_slug=None):
        """Returns a fully-qualified path to AchievementCreate,
        given a Mission and Quiz instance.

        We have the ASSUMPTION that there is only one Link object
        related to the Mission.

        Parameters:
        mission_id(int): id field of a Mission instance
        quiz_slug(str): slug value of one of the Quizzes

        Returns: str for the URL path

        """
        # get the Link related to the Mission
        mission_obj = Mission.objects.get(id=mission_id)
        link = Link.get_mission_links(mission_obj)[0]
        # get the available arguments for the URL path
        arguments = [mission_id, link.id]
        if quiz_slug is not None:
            arguments.append(quiz_slug)
        # form and return the path
        path = reverse("carbon_quiz:achievement_create", args=arguments)
        return path


class MissionTrackingAchievement(APIView):
    def get(self, request, mission_id, pk=0):
        """
        Responds to a user scanning a QR code, in order
        to track a Mission and earn an Achievement

        Parameters:
        request(HttpRequest): the GET request sent to the server
        mission_id(int): the Mission with this id is being completed
        pk(int): the id of a Profile belonging to a player

        Returns:
        HttpResponseRedirect: redirects the request to the POST
                              handler for this endpoint

        """
        # A: init the primary key of the Profile to be anonymous
        pk = 0
        # B: check to see if the user is authenticated or not
        if request.user.is_authenticated:
            # see if there's a unique Profile associated with the player
            profiles = Profile.objects.filter(user=request.user)
            # if not, send the user to the landing page (maybe there's an error)
            if len(profiles) != 1:
                return render(reverse("landing_page"))
            elif len(profiles) == 1:  # there is an associated account
                # otherwise set the primary key
                pk = profiles[0].id
        # C: regardless, send the user along to earn the Achievement
        return self.post(request, mission_id, pk)

    def post(self, request, mission_id, pk=0):
        """
        Completes the flow of a player scanning a new
        QR Code, by redirecting to a new Achievement.

        Parameters:
        request(HttpRequest): the GET request sent to the server
        mission_id(int): the Mission with this id is being completed
        pk(int): the id of a Profile belonging to a player

        Returns:
        HttpResponseRedirect: view of the AchievementDetail
                              template, with the new Achievement

        """
        # A: get the mission they're tracking
        mission = Mission.objects.get(id=mission_id)
        # B: Create and Save the new Achievement
        achievement = Achievement.objects.create(
            mission=mission,
            zeron_image_url=Achievement.set_zeron_image_url(mission),
        )
        achievement.save()
        # C: Check if we can send the player to the AchievementDetail now
        if pk > 0:
            # get the player's Profile, and connect it with the Achievement
            profile = Profile.objects.get(id=pk)
            achievement.profile = profile
            achievement.save()
            # add a message as well
            messages.add_message(
                request,
                messages.SUCCESS,
                "Congratulations - you've earned a new Zeron!",
            )
            # redirect to show the player their new Achievement
            return HttpResponseRedirect(achievement.get_absolute_url())
        else:  # no pk, so send the user and Achievement to LoginView
            domain = av.get_domain(request)
            path = reverse("accounts:login", args=[achievement.secret_id])
            url = "".join([domain, path])
            return HttpResponseRedirect(url)


class CategoryTrackerData(APIView):
    
    def get(self, request, category):
        """
        Given the category that a Question for a tracking mission 
        falls into, we return the image URL for the sign that
        the player can use to track their progress.

        e.g. "R" as input --> "images/Sticker_Recycle.png" as output

        Parameters:
        request(HttpRequest): a GET request sent to the server
        category(str): one of the values in Question.CATEGORIES

        Returns:
        str: the relative URL for the sign image, within the STATIC_ROOT

        """
        # A: map the Question categories to the image URLs
        img_urls = [
            'images/Sticker_Diet.png',
            'images/Sticker_Transport.png',
            'images/Sticker_Recycling.png',
            'No image',  # assuming none of the Offsets missions are tracked
            'images/Sticker_Utilities.png'
        ]
        category_img_urls = dict(zip(
            Question.get_category_abbreviations(), img_urls
        ))
        # B: return the corresponding image URL
        img_url = {"imageURL": category_img_urls[category]}
        return Response(img_url)
