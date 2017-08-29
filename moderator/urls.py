from rest_framework.routers import DefaultRouter
from .views import ModeratorActivityView,PendingModeratorActivity,CheckVotesForSingleMessage
from django.conf.urls import url
router=DefaultRouter()
router.register(r'activity',ModeratorActivityView)
router.register(r'checkVoteForMessage',CheckVotesForSingleMessage)
urlpatterns=router.urls
urlpatterns.append(url(r'^pending/$', PendingModeratorActivity.as_view()))