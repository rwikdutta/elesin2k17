from .views import UserSignUpAuthView,UserSignInAuthView,UserSignOutAuthView,CheckAuth
# from rest_framework.routers import DefaultRouter
#
# router=DefaultRouter()
# router.register(r'signup',usersignuppost,base_name='signup')
# urlpatterns=router.urls


from django.conf.urls import url
urlpatterns=[
    url(r'^signup/$',UserSignUpAuthView.as_view()),
    url(r'^login/$', UserSignInAuthView.as_view()),
    url(r'^logout/$', UserSignOutAuthView.as_view()),
    url(r'^checklogin/$', CheckAuth.as_view())
]
