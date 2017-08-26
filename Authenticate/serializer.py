from django.contrib.auth.models import User
from rest_framework import serializers
from Compliments.models import Departments
from Authenticate.nondbmodels import UserSignUpAuthViewModel
from Authenticate.models import RegisteredUsers,ProbableUsers

class UserSignUpAuthViewSerializer(serializers.Serializer):
    last_name=serializers.CharField(max_length=100)
    first_name = serializers.CharField(max_length=100)
    email=serializers.EmailField()
    password=serializers.CharField(max_length=50)
    dept=serializers.PrimaryKeyRelatedField(queryset=Departments.objects.all())
    year_of_study=serializers.IntegerField()

    def create(self, validated_data):
        return UserSignUpAuthViewModel(**validated_data)

class ProbableUsersSerializer(serializers.ModelSerializer):
    model=ProbableUsers
    fields=('id','timestamp','email','signed_up','user_id')
    read_only_fields=('timestamp','id')

class RegisteredUsersSerializer(serializers.ModelSerializer):
    model=RegisteredUsers
    fields=('id','timestamp','dept','year_of_study','user_id')
    read_only_fields=('timestamp','id')

class UserSignInAuthViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username')
