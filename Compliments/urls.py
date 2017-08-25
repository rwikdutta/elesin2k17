from .views import TeachersViewSet,DepartmentsViewSet,LikesViewSet,GratitudeViewSet,MessagesViewSet
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register(r'teachers',TeachersViewSet)
router.register(r'departments',DepartmentsViewSet)
router.register(r'likes',LikesViewSet)
router.register(r'gratitude',GratitudeViewSet)
router.register(r'messages',MessagesViewSet)

urlpatterns=router.urls