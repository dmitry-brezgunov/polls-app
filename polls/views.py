from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from .models import Choice, Poll, Question
from .serializers import ChoiceSerializer, PollSerializer, QuestionSerializer


class PollViewSet(ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAdminUser]


class QuestionViewSet(ModelViewSet):
    serializer_class = QuestionSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        poll = get_object_or_404(Poll, pk=self.kwargs.get('poll_id'))
        return Question.objects.filter(poll=poll)

    def perform_create(self, serializer):
        poll = get_object_or_404(Poll, pk=self.kwargs.get('poll_id'))
        serializer.save(poll=poll)


class ChoiceViewSet(ModelViewSet):
    serializer_class = ChoiceSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        question = get_object_or_404(
            Question, pk=self.kwargs.get('question_id'),
            choice_type__in=(Question.ONE_CHOICE, Question.MULTI_CHOICE))

        return Choice.objects.filter(question=question)

    def perform_create(self, serializer):
        question = get_object_or_404(
            Question, pk=self.kwargs.get('question_id'))

        serializer.save(question=question)
