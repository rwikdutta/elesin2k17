from rest_framework import mixins,status
from rest_framework.response import Response
from rest_framework import permissions
from .serializer import TeachersSerializer,MessagesSerializer,LikesSerializer,GratitudeSerializer,DepartmentsSerializer
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from .models import Teachers,Departments,Likes,Gratitude,Messages
from rest_framework.views import APIView
from datetime import datetime
# Create your views here.
class TeachersViewSet(mixins.ListModelMixin,mixins.RetrieveModelMixin,GenericViewSet):
    queryset = Teachers.objects.all()
    serializer_class = TeachersSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class MessagesViewSet(mixins.CreateModelMixin,mixins.ListModelMixin,mixins.RetrieveModelMixin,GenericViewSet):
    queryset = Messages.objects.filter(deleted=False,verified_by_moderators=True)
    serializer_class = MessagesSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def create(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        parent_teacher_obj=Teachers.objects.filter(id=request.data['teacher_id'])
        parent_teacher_obj=parent_teacher_obj.update(msg_count=parent_teacher_obj.values()[0]['msg_count']+1,last_msg_activity_id=serializer.data['id'])
        headers=self.get_success_headers(serializer.data)
        return Response(serializer.data,status=status.HTTP_201_CREATED,headers=headers)


class DepartmentsViewSet(mixins.ListModelMixin,mixins.RetrieveModelMixin,GenericViewSet):
    queryset = Departments.objects.all()
    serializer_class = DepartmentsSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class LikesViewSet(mixins.CreateModelMixin,mixins.ListModelMixin,mixins.RetrieveModelMixin,GenericViewSet):
    queryset = Likes.objects.all()
    serializer_class = LikesSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def create(self, request, *args, **kwargs):
        # TODO: Checking of this call
        if (('liked' in request.data and request.data['liked']=='true') and ('unliked' in request.data and request.data['unliked']=='true')) or ('liked' not in request.data and 'unliked' not in request.data) or (request.data['liked']=='false' and request.data['unliked']=='false'):
            return Response({
                'error': True,
                'message': 'One and only one out of liked or unliked can be set to true',
            }, status=status.HTTP_400_BAD_REQUEST)
        likes_qs=Likes.objects.filter(message_id_id=request.data.message_id,user_id_id=request.user.id)
        if likes_qs.count()==0 and 'unliked' in request.data and request.data['unliked']=='true':
            return Response({
                'error': True,
                'message': 'You havent liked it before, so you cant unlike it',
            }, status=status.HTTP_400_BAD_REQUEST)
        elif 'liked' in request.data and request.data['liked']=='true' and likes_qs.last().liked==True:
            return Response({
                'error': True,
                'message': 'Already liked by you',
            }, status=status.HTTP_400_BAD_REQUEST)
        elif 'unliked' in request.data and request.data['unliked']=='true' and likes_qs.last().unliked==True:
            return Response({
                'error': True,
                'message': 'You cant unlike something which hasnt originally been liked by you',
            }, status=status.HTTP_400_BAD_REQUEST)
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
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def create(self, request, *args, **kwargs):
        # TODO: Checking of this call
        if (('give_gratitude' in request.data and request.data['give_gratitude']=='true') and ('remove_gratitude' in request.data and request.data['remove_gratitude']=='true')) or ('give_gratitude' not in request.data and 'remove_gratitude' not in request.data) or (request.data['give_gratitude']=='false' and request.data['remove_gratitude']=='false'):
            return Response({
                'error': True,
                'message': 'One and only one out of give_gratitude or remove_gratitude can be set to true',
            }, status=status.HTTP_400_BAD_REQUEST)
        gratitude_qs = Gratitude.objects.filter(teacher_id_id=request.data.teacher_id, user_id_id=request.user.id)
        if gratitude_qs.count() == 0 and 'remove_gratitude' in request.data and request.data['remove_gratitude'] == 'true':
            return Response({
                'error': True,
                'message': 'You havent shown gratitude before so you cant remove it',
            }, status=status.HTTP_400_BAD_REQUEST)
        elif 'give_gratitude' in request.data and request.data['give_gratitude'] == 'true' and gratitude_qs.last().give_gratitude == True:
            return Response({
                'error': True,
                'message': 'You have already shown gratitude to this teacher',
            }, status=status.HTTP_400_BAD_REQUEST)
        elif 'remove_gratitude' in request.data and request.data['remove_gratitude'] == 'true' and gratitude_qs.last().remove_gratitude == True:
            return Response({
                'error': True,
                'message': 'You cant withdraw gratitude from someone before even showing gratitude',
            }, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        parent_teacher_obj = Teachers.objects.filter(id=request.data['teacher_id'])
        parent_teacher_obj = parent_teacher_obj.update(gratitude_count=parent_teacher_obj.values()[0]['gratitude_count'] + 1,last_gratitude_activity_id=serializer.data['id'])
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class MessagesDeleteView(APIView):
    #TODO: Checking of this view
    def post(self,request,format=None):
        message_set=Messages.objects.filter(user_id_id=request.user.id,id=request.data.id,deleted=False)
        if message_set.count()==1:
            message_set.update(deleted=True,deleted_timestamp=datetime.now())
            teacher_qs=Teachers.objects.filter(id=message_set.last().teacher_id_id)
            teacher_qs.update(msg_count=teacher_qs.last().msg_count-1)
            return Response({
                'message': 'Successfully deleted'
            },status=status.HTTP_200_OK)
        else:
            return Response({
                'message': 'There was a problem...perhaps you dont have necessary permission or perhaps a non-deleted message with that id doesnt exist'
            }, status=status.HTTP_403_FORBIDDEN)


class OwnUnverifiedMessages(mixins.ListModelMixin,mixins.RetrieveModelMixin,GenericViewSet):
    # TODO: Checking of this view
    queryset = Messages.objects.filter(deleted=False,verified_by_moderators=False)
    serializer_class = MessagesSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).filter(user_id=self.request.user)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        if 'pk' in kwargs and Messages.objects.filter(id=kwargs['pk']).filter(
                user_id_id=request.user.id).count() == 1:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        else:
            return Response({
                'error': True,
                'message': 'You cant access this info',
            }, status=status.HTTP_403_FORBIDDEN)

