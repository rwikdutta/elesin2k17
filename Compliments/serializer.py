from rest_framework import serializers

from .models import Teachers,Departments,Gratitude,Messages,Likes

class LikesSerializer(serializers.ModelSerializer):
    class Meta:
        model=Likes
        fields=('message_id','liked','unliked','id','timestamp','user_id')
        read_only_fields=('id','timestamp','user_id')

class VerifiedAndUndeletedMessagesSerializerInternal(serializers.ListSerializer):

    def to_representation(self, data):
        data=data.filter(verified_by_moderators=True,deleted=False)
        return super(VerifiedAndUndeletedMessagesSerializerInternal, self).to_representation(data)

class VerifiedMessagesSerializer(serializers.ModelSerializer):

    likes=LikesSerializer(read_only=True,many=True)

    class Meta:
        list_serializer_class=VerifiedAndUndeletedMessagesSerializerInternal
        model=Messages
        #Make sure user_id is not displayed since messages are anonymous
        fields=('message_body','deleted','id','timestamp','moderator_approval_count','verified_by_moderators','last_like_activity_id','last_like_count','likes','teacher_id')
        read_only_fields=('id','timestamp','moderator_approval_count','verified_by_moderators','last_like_activity_id','last_like_count','likes','deleted')

class GratitudeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Gratitude
        fields=('give_gratitude','remove_gratitude','id','timestamp','teacher_id','user_id')
        read_only_fields=('id','timestamp','user_id')

class MessagesSerializer(serializers.ModelSerializer):

    likes=LikesSerializer(read_only=True,many=True)
    class Meta:
        model=Messages
        #Make sure user_id is not displayed since messages are anonymous
        fields=('message_body','deleted','id','timestamp','moderator_approval_count','verified_by_moderators','last_like_activity_id','last_like_count','likes','teacher_id')
        read_only_fields=('id','timestamp','moderator_approval_count','verified_by_moderators','last_like_activity_id','last_like_count','likes','deleted')


class TeachersSerializer(serializers.ModelSerializer):
    gratitude=GratitudeSerializer(read_only=True,many=True)
    messages=VerifiedMessagesSerializer(read_only=True, many=True)
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


