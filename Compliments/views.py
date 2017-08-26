from rest_framework import mixins,status
from rest_framework.response import Response
from .serializer import TeachersSerializer,MessagesSerializer,LikesSerializer,GratitudeSerializer,DepartmentsSerializer
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from .models import Teachers,Departments,Likes,Gratitude,Messages
from django.contrib.auth.decorators import login_required
# Create your views here.
class TeachersViewSet(ModelViewSet):
    queryset = Teachers.objects.all()
    serializer_class = TeachersSerializer
    # TODO: Allow Teachers to be created only by admin users through the pycharm admin, i.e. revoke post access and delete access from this view

class MessagesViewSet(mixins.CreateModelMixin,mixins.ListModelMixin,mixins.RetrieveModelMixin,GenericViewSet):
    queryset = Messages.objects.filter(deleted=False,verified_by_moderators=True)
    serializer_class = MessagesSerializer
    #TODO: Implement Delete For Messages with a seperate view

    def create(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        parent_teacher_obj=Teachers.objects.filter(id=request.data['teacher_id'])
        parent_teacher_obj=parent_teacher_obj.update(msg_count=parent_teacher_obj.values()[0]['msg_count']+1,last_msg_activity_id=serializer.data['id'])
        headers=self.get_success_headers(serializer.data)
        return Response(serializer.data,status=status.HTTP_201_CREATED,headers=headers)


class DepartmentsViewSet(ModelViewSet):
    queryset = Departments.objects.all()
    serializer_class = DepartmentsSerializer
    # TODO: Allow Departments to be created only by admin users through the pycharm admin, i.e. revoke post access and delete access from this view

class LikesViewSet(mixins.CreateModelMixin,mixins.ListModelMixin,mixins.RetrieveModelMixin,GenericViewSet):
    queryset = Likes.objects.all()
    serializer_class = LikesSerializer

    def create(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        parent_msg_obj=Messages.objects.filter(id=request.data['message_id'])
        parent_msg_obj=parent_msg_obj.update(last_like_count=parent_msg_obj.values()[0]['last_like_count']+1,last_like_activity_id=serializer.data['id'])
        headers=self.get_success_headers(serializer.data)
        return Response(serializer.data,status=status.HTTP_201_CREATED,headers=headers)

class GratitudeViewSet(mixins.CreateModelMixin,mixins.ListModelMixin,mixins.RetrieveModelMixin,GenericViewSet):
    queryset = Gratitude.objects.all()
    serializer_class = GratitudeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        parent_teacher_obj = Teachers.objects.filter(id=request.data['teacher_id'])
        parent_teacher_obj = parent_teacher_obj.update(gratitude_count=parent_teacher_obj.values()[0]['gratitude_count'] + 1,last_gratitude_activity_id=serializer.data['id'])
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)