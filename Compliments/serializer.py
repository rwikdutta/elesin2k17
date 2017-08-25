from rest_framework import serializers

from .models import Teachers,Departments,Gratitude,Messages,Likes

class LikesSerializer(serializers.ModelSerializer):
    class Meta:
        model=Likes
        fields=('message_id','liked','unliked','id','timestamp')
        read_only_fields=('id','timestamp')

class GratitudeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Gratitude
        fields=('give_gratitude','remove_gratitude','id','timestamp','teacher_id')
        read_only_fields=('id','timestamp')

class MessagesSerializer(serializers.ModelSerializer):

    likes=LikesSerializer(read_only=True,many=True)
    class Meta:
        model=Messages
        fields=('message_body','deleted','id','timestamp','moderator_approval_count','verified_by_moderators','last_like_activity_id','last_like_count','likes','teacher_id')
        read_only_fields=('id','timestamp','moderator_approval_count','verified_by_moderators','last_like_activity_id','last_like_count','likes')

class TeachersSerializer(serializers.ModelSerializer):
    gratitude=GratitudeSerializer(read_only=True,many=True)
    messages=MessagesSerializer(read_only=True, many=True)
    class Meta:
        model=Teachers
        fields=('name','abbr','dept','id','timestamp','msg_count','last_msg_activity_id','gratitude_count','last_gratitude_activity_id','gratitude','messages')
        read_only_fields=('id','timestamp','msg_count','last_msg_activity_id','gratitude_count','last_gratitude_activity_id','gratitude','messages')

class DepartmentsSerializer(serializers.ModelSerializer):
    teachers=TeachersSerializer(read_only=True,many=True)
    class Meta:
        model=Departments
        fields=('dept_name','dept_abbr','id','teachers')
        read_only_fields=('id','teachers')