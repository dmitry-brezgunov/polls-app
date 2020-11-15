from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ActivePolls, PollAnswer, PassedPolls

router = DefaultRouter()
router.register('active-polls', ActivePolls)
router.register(
    r'answer-poll/(?P<poll_id>\d+)/questions/(?P<question_id>\d+)',
    PollAnswer, basename='answer-poll')

router.register(
    r'passed-polls/(?P<user_id>\d+)', PassedPolls, basename='passed-polls')

urlpatterns = [
    path('', include(router.urls))
]
