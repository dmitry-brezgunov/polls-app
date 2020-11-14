from polls.models import Choice, Poll, Question
from rest_framework import serializers

from .utils import ChoiceField


class DetailChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ('id', 'text', )


class DetailQuestionSerializer(serializers.ModelSerializer):
    choices = DetailChoiceSerializer(many=True, read_only=True)
    choice_type = ChoiceField(choices=Question.CHOICES_TYPE, read_only=True)

    class Meta:
        model = Question
        fields = ('id', 'text', 'choice_type', 'choices', )


class DetailPollSerializer(serializers.ModelSerializer):
    questions = DetailQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Poll
        fields = (
            'id', 'title', 'start_date', 'end_date',
            'description', 'questions',
        )
