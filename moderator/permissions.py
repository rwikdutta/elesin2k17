from rest_framework.permissions import BasePermission
from django.contrib.auth.models import User
from rest_framework.compat import is_authenticated
class isModerator(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return request.user.groups.filter(name="Moderators").count()==1
        else:
            return False

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.groups.filter(name="Moderators").count()==1
        else:
            return False
