from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from rest_framework.response import Response


# Create your views here.
class QuizUpdate(APIView):
    """
    Updates the questions that have been answered yes/no in the Quiz,
    and then moves to the next template.
    """
    def get(self, request, quiz_slug, response_to_question):
        """
        Uses the answer to the Question the user has just responded to,
        to update the array of questions related to a Quiz.

        Parameters:
        request(HttpRequest)
        quiz_slug(str): the unique slug value of one of the Quizzes
        response_to_question(int): 0 or 1, which means the user responded
                                   no or yes (respectively)

        Returns:
        HttpResponse: a view of the QuizDetail, with the next question, 
                      or missions for the user

        """
        pass