from django.db import connection
from django.shortcuts import render
from rest_framework import mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import mixins, GenericViewSet
from rest_framework import permissions
from rest_framework.response import Response
from moderator import permissions as custom_permissions
from moderator.models import *
from moderator.serializer import *
from rest_framework.views import APIView
from Teachers_Day_2k17_Complimenter.custom_settings import NECESSARY_VALIDATION_COUNT_MODERATOR
# Create your views here.

class ModeratorActivityView(mixins.CreateModelMixin,mixins.ListModelMixin,mixins.RetrieveModelMixin,GenericViewSet):
    queryset = ModeratorActivity.objects.all() #Extra checking to limit the returned records to be only that of the corresponding user later added in the list method implementation
    serializer_class = ModeratorActivitySerializer
    permission_classes = (custom_permissions.isModerator,)

    def create(self, request, *args, **kwargs):
        data_mod=dict(request.data)
        moderator_qs=ModeratorActivity.objects.filter(user_id_id=request.user.id,message_id_id=request.data['message_id'])
        if 'upvoted' not in data_mod:
            data_mod['upvoted']=['false']
        if 'downvoted' not in data_mod:
            data_mod['downvoted']=['false']
        serializer=self.get_serializer(data=request.data)
        if (data_mod['upvoted'][0]=='true' and data_mod['downvoted'][0]=='true') or (data_mod['upvoted'][0]=='false' and data_mod['downvoted'][0]=='false'):
            return Response({
                'error': True,
                'message': 'One and only one out of upvote or downvote can be true',
            }, status=status.HTTP_200_OK)
        if moderator_qs.count()==0 and data_mod['downvoted'][0]=='true':
            return Response({
                'error': True,
                'message': 'You cant remove vote from something that you havent upvoted'
                           }, status=status.HTTP_200_OK)
        elif moderator_qs.last()!=None and moderator_qs.last().upvoted and data_mod['upvoted'][0]=='true':
            return Response({
                'error': True,
                'message': 'You have already upvoted'
            }, status=status.HTTP_200_OK)
        elif moderator_qs.last()!=None and moderator_qs.last().downvoted and data_mod['downvoted'][0]=='true':
            return Response({
                'error': True,
                'message': 'It is not yet upvoted so you cant downvote it'
            }, status=status.HTTP_200_OK)
        serializer.is_valid(raise_exception=True)
        serializer.save(user_id=self.request.user)
        messages_qs=Messages.objects.filter(id=serializer.instance.message_id_id)
        if serializer.instance.upvoted:
            messages_qs.update(moderator_approval_count=messages_qs.values()[0]['moderator_approval_count']+1)
            if messages_qs.last().moderator_approval_count>=NECESSARY_VALIDATION_COUNT_MODERATOR:
                messages_qs.update(verified_by_moderators=True)
        elif serializer.instance.downvoted:
            messages_qs.update(moderator_approval_count=messages_qs.values()[0]['moderator_approval_count'] - 1)
            if messages_qs.last().moderator_approval_count<NECESSARY_VALIDATION_COUNT_MODERATOR:
                messages_qs.update(verified_by_moderators=False)
        headers=self.get_success_headers(serializer.data)
        return Response(serializer.data,status=status.HTTP_201_CREATED,headers=headers)


    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).filter(user_id=self.request.user)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        if 'pk' in kwargs and ModeratorActivity.objects.filter(id=kwargs['pk']).filter(user_id_id=request.user.id).count()==1:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        else:
            return Response({
                'error': True,
                'message': 'You cant access this info',
            },status=status.HTTP_200_OK)

#Since pagination has not been implemented for this view, try doing a background AJAX call
class PendingModeratorActivity(APIView):

    def dictfetchall(self,cursor):
        "Return all rows from a cursor as a dict"
        columns = [col[0] for col in cursor.description if col[0]!='user_id_id']
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def my_custom_sql(self,request):
        cursor = connection.cursor()
        cursor.execute(
            "SELECT * FROM (SELECT * FROM (SELECT id FROM Compliments_messages where Compliments_messages.verified_by_moderators=0 and Compliments_messages.deleted=0 except SELECT message_id_id FROM moderator_moderatoractivity where moderator_moderatoractivity.user_id_id={})) as tem INNER JOIN Compliments_messages as m ON m.id=tem.id".format(request.user.id))
        rows = self.dictfetchall(cursor)
        return rows

    def get(self,request,format=None):
        perm=custom_permissions.isModerator()
        if perm.has_permission(request=request,view=self):
            data=self.my_custom_sql(request=request)
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': True,
                'message': 'You cant access this info',
            }, status=status.HTTP_200_OK)


class CheckVotesForSingleMessage(mixins.RetrieveModelMixin,GenericViewSet):
    queryset=ModeratorActivity.objects.all()
    serializer_class = ModeratorActivitySerializer
    permission_classes = (custom_permissions.isModerator,)

    def retrieve(self, request, *args, **kwargs):
        if 'pk' in kwargs and Messages.objects.filter(id=kwargs['pk'],deleted=False).count()==0:
            return Response({
                'error': True,
                'message': 'You cant access this info or the message id you entered is invalid',
            }, status=status.HTTP_200_OK)
        #When there's no entry corresponding to this
        qs=ModeratorActivity.objects.filter(message_id_id=kwargs['pk'],user_id_id=request.user.id)
        if 'pk' in kwargs and qs.count()==0:
            return Response({
                'id':-1,
                'upvoted': False,
                'downvoted': True,
                'message_id':kwargs['pk']
            }, status=status.HTTP_200_OK)
        elif 'pk' in kwargs:
            serializer=self.get_serializer(qs.last())
            return Response(serializer.data)