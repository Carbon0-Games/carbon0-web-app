from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from rest_framework.views import APIView
from rest_framework.response import Response

from accounts.models import Profile
from carbon_quiz.models.achievement import Achievement
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
        # if the user just answered 'yes',
        if question_response == 1:
            # ignore the question later, when finding missions
            quiz.questions[quiz.active_question] = 0
        # if question was answered no
        elif question_response == 0 and quiz.active_question > 0:
            # increment the total carbon value so far
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
        all_profiles = Profile.objects.order_by('-users_footprint')
        # for loop to get all user names
        players = list()
        for (i,p) in enumerate(all_profiles):
            # create the player object
            player = {
                'position': i,
                'username': p.user.username,
                'score': p.users_footprint
            }
            # add to the list
            players.append(player)
        data = {
            "players": players
        }

        return Response(data)