from django.contrib.auth.models import User
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
# Create your models here.
@python_2_unicode_compatible
class Departments(models.Model):
    timestamp=models.DateTimeField(auto_now=True)
    dept_name=models.CharField(max_length=50)
    dept_abbr=models.CharField(max_length=10)

    def __str__(self):
        return self.dept_name

@python_2_unicode_compatible
class Teachers(models.Model):
    timestamp = models.DateTimeField(auto_now=True)
    msg_count = models.IntegerField(default=0)
    last_msg_activity_id = models.IntegerField(null=True,default=-1)
    gratitude_count = models.IntegerField(default=0)
    last_gratitude_activity_id = models.IntegerField(null=True,default=-1)
    name=models.CharField(max_length=100,unique=True)
    abbr=models.CharField(max_length=10,blank=True,unique=True)
    dept=models.ForeignKey(Departments,on_delete=models.CASCADE,related_name='teachers')

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Messages(models.Model):
    timestamp = models.DateTimeField(auto_now=True)
    deleted_timestamp=models.DateTimeField(blank=True,null=True,default=None)
    user_id=models.ForeignKey(User,related_name='messages',null=True,default=1)
    teacher_id = models.ForeignKey(Teachers, on_delete=models.CASCADE, related_name='messages')
    message_body = models.CharField(max_length=200, blank=False)
    moderator_approval_count = models.IntegerField(default=0)
    verified_by_moderators = models.BooleanField(default=False)
    last_like_activity_id = models.IntegerField(null=True,default=-1)
    last_like_count = models.IntegerField(default=0)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.message_body

@python_2_unicode_compatible
class Likes(models.Model):
    timestamp = models.DateTimeField(auto_now=True)
    user_id = models.ForeignKey(User, related_name='likes',null=True,default=1)
    message_id = models.ForeignKey(Messages, on_delete=models.CASCADE, related_name='likes')
    liked = models.BooleanField()
    unliked = models.BooleanField()

    def __str__(self):
        return str(self.id)
@python_2_unicode_compatible
class Gratitude(models.Model):
    timestamp = models.DateTimeField(auto_now=True)
    user_id = models.ForeignKey(User, related_name='gratitude',null=True,default=1)
    teacher_id = models.ForeignKey(Teachers, on_delete=models.CASCADE, related_name='gratitude')
    give_gratitude = models.BooleanField()
    remove_gratitude = models.BooleanField()

    def __str__(self):
        return str(self.id)
