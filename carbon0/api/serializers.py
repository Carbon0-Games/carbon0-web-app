from rest_framework.serializers import ModelSerializer

from carbon_quiz.models import Question, Mission

class QuestionSerializer(ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class MissionSerializer(ModelSerializer):
    class Meta:
        model = Mission
        fields = '__all__'
