from rest_framework import serializers
from .models import ModeratorActivity

class ModeratorActivitySerializer(serializers.ModelSerializer):

    class Meta:
        model=ModeratorActivity
        fields=('id','timestamp','user_id','message_id','upvoted','downvoted')
        read_only_fields=('id','timestamp','user_id')