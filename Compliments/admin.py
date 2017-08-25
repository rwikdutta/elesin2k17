from django.contrib import admin

from .models import Likes,Messages,Gratitude,Teachers,Departments

# Register your models here.
admin.site.register(Likes)
admin.site.register(Messages)
admin.site.register(Gratitude)
admin.site.register(Teachers)
admin.site.register(Departments)