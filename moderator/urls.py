from rest_framework.routers import DefaultRouter
from .views import ModeratorActivityView,PendingModeratorActivity
from django.conf.urls import url
router=DefaultRouter()
router.register(r'activity',ModeratorActivityView)
urlpatterns=router.urls
urlpatterns.append(url(r'^pending/$', PendingModeratorActivity.as_view()))