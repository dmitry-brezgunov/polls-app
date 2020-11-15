from django.shortcuts import get_object_or_404, get_list_or_404
from django.utils import timezone
from polls.models import Poll, Question
from polls.serializers import PollSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import (CreateModelMixin, ListModelMixin,
                                   RetrieveModelMixin)
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from .models import UserAnswer
from .serializers import (DetailPollSerializer, PassedPollSerializer,
                          UserAnswerMultiChoiceSerializer,
                          UserAnswerOneChoiceSerializer,
                          UserAnswerTextSerializer)


class ActivePolls(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = Poll.objects.filter(end_date__gt=timezone.now())
    permission_classes = [AllowAny]
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.action == 'list':
            return PollSerializer
        return DetailPollSerializer


class PollAnswer(CreateModelMixin, GenericViewSet):
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        question = get_object_or_404(
            Question, pk=self.kwargs.get('question_id'))

        if question.choice_type == Question.ONE_CHOICE:
            return UserAnswerOneChoiceSerializer
        elif question.choice_type == Question.MULTI_CHOICE:
            return UserAnswerMultiChoiceSerializer
        else:
            return UserAnswerTextSerializer

    def perform_create(self, serializer):
        question = get_object_or_404(
            Question, pk=self.kwargs.get('question_id'))

        poll = get_object_or_404(Poll, pk=self.kwargs.get('poll_id'))

        if UserAnswer.objects.filter(
                user_id=serializer.validated_data['user_id'],
                question=question).exists():

            raise ValidationError('Вы уже ответили на этот вопрос')

        serializer.save(question=question, poll=poll)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['question_id'] = self.kwargs['question_id']
        return context


class PassedPolls(ListModelMixin, GenericViewSet):
    permission_classes = [AllowAny]
    pagination_class = PageNumberPagination
    serializer_class = PassedPollSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return get_list_or_404(
            Poll.objects.filter(user_answer__user_id=user_id).distinct())
