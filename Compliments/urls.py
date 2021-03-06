from .views import TeachersViewSet,DepartmentsViewSet,LikesViewSet,GratitudeViewSet,MessagesViewSet,OwnUnverifiedMessages,MessagesDeleteView,TeacherGratitutedOrNot,MessageLikedOrNot,CheckMessageDeletePermission
from rest_framework.routers import DefaultRouter
from django.conf.urls import url

router=DefaultRouter()
router.register(r'teachers',TeachersViewSet)
router.register(r'departments',DepartmentsViewSet)
router.register(r'likes',LikesViewSet)
router.register(r'gratitude',GratitudeViewSet)
router.register(r'messages',MessagesViewSet)
router.register(r'unverifiedmessages',OwnUnverifiedMessages)
router.register(r'messageliked',MessageLikedOrNot)
router.register(r'teachergratituted',TeacherGratitutedOrNot)
router.register(r'checkmessagedeletepermission',CheckMessageDeletePermission)
urlpatterns=router.urls

urlpatterns.append(url(r'^messagedelete/',MessagesDeleteView.as_view())
)