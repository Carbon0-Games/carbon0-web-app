from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from rest_framework.response import Response


# Create your views here.
class QuizUpdate(APIView):
    """
    Updates the questions that have been answered yes/no in the Quiz,
    and then moves to the next template.
    """