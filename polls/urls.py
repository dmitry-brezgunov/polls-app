from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ChoiceViewSet, PollViewSet, QuestionViewSet

router = DefaultRouter()
router.register('polls', PollViewSet)
router.register(
    r'polls/(?P<poll_id>\d+)/questions', QuestionViewSet, basename='questions')

router.register(
    r'polls/(?P<poll_id>\d+)/questions/(?P<question_id>\d+)/choices',
    ChoiceViewSet, basename='choices')

urlpatterns = [
    path('', include(router.urls))
]
