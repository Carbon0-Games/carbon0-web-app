from rest_framework.serializers import ModelSerializer

from carbon_quiz.models.mission import Mission
from carbon_quiz.models.question import Question


class QuestionSerializer(ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class MissionSerializer(ModelSerializer):
    class Meta:
        model = Mission
        fields = '__all__'
