from django.contrib.auth.models import User
from django.db import models
from Compliments.models import Messages
# Create your models here.
class ModeratorActivity(models.Model):
    timestamp=models.DateTimeField(auto_now=True)
    user_id=models.ForeignKey(User,related_name='moderator_activity')
    message_id=models.ForeignKey(Messages,related_name='moderator_activity')
    upvoted=models.BooleanField()
    downvoted=models.BooleanField()

