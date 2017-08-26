from rest_framework.permissions import BasePermission
from django.contrib.auth.models import User
from rest_framework.compat import is_authenticated
class isModerator(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.groups.filter(name="Moderators").count()==1

    def has_permission(self, request, view):
        return super().has_permission(request, view)