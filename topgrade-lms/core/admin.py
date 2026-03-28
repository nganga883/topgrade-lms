from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import User, Course, Material

admin.site.register(User)
admin.site.register(Course)
admin.site.register(Material)

from .models import Assignment, Submission

admin.site.register(Assignment)
admin.site.register(Submission)