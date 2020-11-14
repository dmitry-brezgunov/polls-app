from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ActivePolls

router = DefaultRouter()
router.register('active-polls', ActivePolls)

urlpatterns = [
    path('', include(router.urls))
]
