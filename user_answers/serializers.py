from polls.models import Choice, Poll, Question
from rest_framework import serializers

from .models import UserAnswer
from .utils import (ChoiceField, FilteredListSerializer,
                    QuestionChoicesForeignKey)


class DetailChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ('text', )


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


class UserAnswerTextSerializer(serializers.ModelSerializer):
    question = serializers.SlugRelatedField(slug_field='text', read_only=True)
    text_answer = serializers.CharField(required=True)

    class Meta:
        model = UserAnswer
        fields = ('user_id', 'question', 'text_answer', )


class UserAnswerOneChoiceSerializer(serializers.ModelSerializer):
    question = serializers.SlugRelatedField(slug_field='text', read_only=True)
    one_choice_answer = QuestionChoicesForeignKey(
        slug_field='text', required=True)

    class Meta:
        model = UserAnswer
        fields = ('user_id', 'question', 'one_choice_answer', )


class UserAnswerMultiChoiceSerializer(serializers.ModelSerializer):
    question = serializers.SlugRelatedField(slug_field='text', read_only=True)
    multi_choice_answer = QuestionChoicesForeignKey(
        slug_field='text', many=True, allow_empty=False)

    class Meta:
        model = UserAnswer
        fields = ('user_id', 'question', 'multi_choice_answer', )


class UserAnswerSerializer(serializers.ModelSerializer):
    one_choice_answer = serializers.SlugRelatedField(
        slug_field='text', read_only=True)

    multi_choice_answer = serializers.SlugRelatedField(
        slug_field='text', read_only=True, many=True)

    class Meta:
        model = UserAnswer
        list_serializer_class = FilteredListSerializer
        fields = ('text_answer', 'one_choice_answer', 'multi_choice_answer', )


class PassedQuestionSerializer(serializers.ModelSerializer):
    user_answer = UserAnswerSerializer(read_only=True, many=True)

    class Meta:
        model = Question
        fields = ('text', 'user_answer', )


class PassedPollSerializer(serializers.ModelSerializer):
    questions = PassedQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Poll
        fields = ('id', 'title', 'questions', )
