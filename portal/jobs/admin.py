from django.contrib import admin
from .models import Profile,createjobposts,applyjob
# Register your models here.
admin.site.register(Profile)
admin.site.register(createjobposts)
admin.site.register(applyjob)