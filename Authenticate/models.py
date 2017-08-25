from django.core.exceptions import ValidationError
from django.db import models
from Compliments.models import Departments
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
# Create your models here.
@python_2_unicode_compatible
class ProbableUsers(models.Model):
    timestamp=models.DateTimeField(auto_now=True)
    email=models.EmailField(blank=False,unique=True)
    signed_up=models.BooleanField(default=False)
    user_id=models.OneToOneField(User,related_name='probable_users',null=True)
    def __str__(self):
        return self.email

@python_2_unicode_compatible
class RegisteredUsers(models.Model):
    timestamp=models.DateTimeField(auto_now=True)
    user_id = models.OneToOneField(User, related_name='registered_users')
    dept=models.ForeignKey(Departments,related_name='registered_users')
    def validity_year(self,value):
        if value>4 or value<0:
            raise ValidationError('Invalid entry for year of study')
    year_of_study=models.IntegerField(blank=False,validators=[validity_year])

    def __str__(self):
        return self.user_id





