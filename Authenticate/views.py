from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.http import Http404
from django.shortcuts import render
from rest_framework import mixins,views,status
from rest_framework.response import Response
# Create your views here.
from rest_framework.views import APIView, exception_handler
from .models import RegisteredUsers,ProbableUsers
from .serializer import UserSignUpAuthViewSerializer, UserSignInAuthViewSerializer
from .nondbmodels import UserSignUpAuthViewModel
from Compliments.models import Departments
from Teachers_Day_2k17_Complimenter.custom_settings import NECESSARY_PROBABLE_USERS_VALIDATION
from moderator.permissions import isModerator
from django.views.decorators.csrf import csrf_exempt

class UserSignUpAuthView(APIView):

    def post(self,request,format=None):
        #TODO: Implement sending user id and password via email
        last_name=request.data.get("last_name")
        first_name = request.data.get("first_name")
        username=request.data.get("email")
        email = request.data.get("email")
        password=request.data.get("password")
        dept_id=request.data.get("dept_id")
        year_of_study=request.data.get("year_of_study")
        if User.objects.filter(email=request.data['email']).count()>0:
            return Response({
                'error': True,
                'message': 'Email already exists'
            }, status=status.HTTP_200_OK)
        if RegisteredUsers.objects.filter(mac_adddress=request.data['mac_adddress']).count() > 0:
            return Response({
                'error': True,
                'message': 'An account already created from this phone'
            }, status=status.HTTP_200_OK)

        serializer = UserSignUpAuthViewSerializer(data={'last_name': last_name, 'first_name': first_name, 'email': email, 'password': password,'year_of_study': year_of_study, 'dept': Departments.objects.filter(id=dept_id)})

        serializer.is_valid(raise_exception=True)
        if NECESSARY_PROBABLE_USERS_VALIDATION:
            probable_users_filter=ProbableUsers.objects.filter(email=email)
            if probable_users_filter.count()==1:
                user = User.objects.create_user(username, email, password)
            else:
                return Response({
                    'error':True,
                    'status': 'Unauthorized',
                    'message': 'This email doesnt exist in the list of probable users'
                },status=status.HTTP_200_OK)
        else:
            user = User.objects.create_user(username, email, password)
        user.first_name=first_name
        user.last_name=last_name
        user.save()
        if NECESSARY_PROBABLE_USERS_VALIDATION:
            probable_users_filter.update(user_id_id=user.id)
        r=RegisteredUsers()
        r.user_id=user
        r.dept=Departments.objects.filter(id=dept_id)[0]
        r.year_of_study=year_of_study
        r.mac_adddress=request.data['mac_adddress']
        r.save()
        data=serializer.data
        del data['password']
        return Response(data)


class UserSignInAuthView(APIView):

    def post(self,request,format=None):
        user=authenticate(
            username=request.data.get("username"),
        password=request.data.get("password"))
        if user is None or not user.is_active:
            return Response({
                'error': True,
                'status': 'Unauthorized',
                'message': 'Username or password incorrect'
            }, status=status.HTTP_200_OK)

        login(request, user)
        return Response(UserSignInAuthViewSerializer(user).data)

class UserSignOutAuthView(views.APIView):
    def get(self, request):
        logout(request)
        return Response({
                'status': 'Logged out',
                'message': 'Logged out successfully'
            },status=status.HTTP_200_OK)

class CheckAuth(views.APIView):
    def get(self,request):
        if request.user.is_authenticated:
            moderator=isModerator()
            return Response({
                'status': 'Logged In',
                'username': request.user.username,
                'is_moderator':moderator.has_permission(request,self)
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': 'Logged Out',
            }, status=status.HTTP_200_OK)