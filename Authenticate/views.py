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

class UserSignUpAuthView(APIView):

    def post(self,request,format=None):
        last_name=request.data.get("last_name")
        first_name = request.data.get("first_name")
        username=request.data.get("email")
        email = request.data.get("email")
        password=request.data.get("password")
        dept_id=request.data.get("dept_id")
        year_of_study=request.data.get("year_of_study")
        serializer = UserSignUpAuthViewSerializer(data={'last_name': last_name, 'first_name': first_name, 'email': email, 'password': password,'year_of_study': year_of_study, 'dept': Departments.objects.filter(id=dept_id)})
        serializer.is_valid(raise_exception=True)
        probable_users_filter=ProbableUsers.objects.filter(email=email)
        if probable_users_filter.count()==1:
            user = User.objects.create_user(username, email, password)
        else:
            return Response({
                'status': 'Unauthorized',
                'message': 'This email doesnt exist in the list of probable users'
            })
        #TODO: Error checking here
        user.first_name=first_name
        user.last_name=last_name
        user.save()
        probable_users_filter.update(user_id_id=user.id)
        r=RegisteredUsers()
        r.user_id=user
        r.dept=Departments.objects.filter(id=dept_id)[0]
        r.year_of_study=year_of_study
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
                'status': 'Unauthorized',
                'message': 'Username or password incorrect'
            }, status=status.HTTP_401_UNAUTHORIZED)

        login(request, user)
        return Response(UserSignInAuthViewSerializer(user).data)

class UserSignOutAuthView(views.APIView):
    def get(self, request):
        logout(request)
        return Response({}, status=status.HTTP_204_NO_CONTENT)