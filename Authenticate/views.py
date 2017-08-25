from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import mixins
from rest_framework.response import Response
# Create your views here.
from rest_framework.views import APIView
from .models import RegisteredUsers,ProbableUsers
from .serializer import UserSignUpAuthViewSerializer
from .nondbmodels import UserSignUpAuthViewModel
from Compliments.models import Departments

# class UserSignUpAuthView(APIView):
#
#     def post(self,request,format=None):
#         last_name=request.data.get("last_name")
#         first_name = request.data.get("first_name")
#         username=request.data.get("email")
#         email = request.data.get("email")
#         password=request.data.get("password")
#         dept_id=request.data.get("dept_id")
#         year_of_study=request.data.get("year_of_study")
#         serializer = UserSignUpAuthViewSerializer(data={'last_name': last_name, 'first_name': first_name, 'email': email, 'password': password,'year_of_study': year_of_study, 'dept': Departments.objects.filter(id=dept_id)})
#         serializer.is_valid(raise_exception=True)
#         probable_users_filter=ProbableUsers.objects.filter(email=email)
#         if probable_users_filter.count()==1:
#             user=User.objects.create_user(username,email,password)
#         user.first_name=first_name
#         user.last_name=last_name
#         user.save()
#         probable_users_filter.update(user_id_id=probable_users_filter)