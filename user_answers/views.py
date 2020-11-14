from django.utils import timezone
from polls.models import Poll
from polls.serializers import PollSerializer
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from .serializers import DetailPollSerializer


class ActivePolls(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = Poll.objects.filter(end_date__gt=timezone.now())
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action == 'list':
            return PollSerializer
        return DetailPollSerializer
