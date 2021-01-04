from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from rest_framework.views import APIView
from rest_framework.response import Response

from accounts.models import Profile
from carbon_quiz.models.achievement import Achievement
from carbon_quiz.models.link import Link
from carbon_quiz.models.mission import Mission
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


class QRCodeReceiver(APIView):
    def get(self, request, mission_id):
        """
        Decides what destination the player scanning a QR code will have.
        If the player has an account, we send them to complete tracking 
        the mission.

        Otherwise, we send them to the landing page of the website.

        Parameters:
        request(HttpRequest): the GET request sent to the server.
                              Encapsulates the user making the request, 
                              so we can tell if they have a Profile or not.
        mission_id(int): if the player does have an account, we will have them
                         complete the Mission with this id.

        Returns: HttpResponse to either 1) the 'landing_page' view, or 
                 2) the MissionTrackingAchievement view below.

        """
        # A: see if there's a unique Profile associated with the player
        profiles= Profile.objects.filter(user=request.user)
        # B: if not, then send the player along to the landing page
        if len(profiles) != 1:
            return render(reverse("landing_page")) 
        elif len(profiles) == 1:  # there is an associated account
            # send the user along to earn the Achievement
            pk = profiles[0].id
            return HttpResponse(reverse(
                'api:mission_tracking_achievement',
                args=[pk, mission_id]
                )
            )


class MissionTrackingAchievement(APIView):
    def get(self, request, pk, mission_id):
        """
        Responds to a user scanning a QR code, in order
        to track a Mission and earn an Achievement

        Parameters:
        request(HttpRequest): the GET request sent to the server
        pk(int): the id of a Profile belonging to a player
        mission_id(int): the Mission with this id is being completed

        Returns: 
        HttpResponseRedirect: redirects the request to the POST 
                              handler for this endpoint
        
        """
        return self.post(request, pk, mission_id)

    def post(self, request, pk, mission_id):
        """
        Completes the flow of a player scanning a new 
        QR Code, by redirecting to a new Achievement.

        Parameters:
        request(HttpRequest): the GET request sent to the server
        pk(int): the id of a Profile belonging to a player
        mission_id(int): the Mission with this id is being completed

        Returns: 
        HttpResponseRedirect: view of the AchievementDetail
                              template, with the new Achievement
        
        """
        # A: get the player's Profile
        profile = Profile.objects.get(id=pk)
        # B: get the mission they're tracking
        mission = Mission.objects.get(id=mission_id)
        # C: create and save a new Achievement
        achievement = Achievement.objects.create(
            profile=profile,
            mission=mission,
            zeron_image_url=Achievement.set_zeron_image_url(mission),
        )
        achievement.save()
        # D: redirect to show the player their new Achievement
        return HttpResponseRedirect(achievement.get_absolute_url())
