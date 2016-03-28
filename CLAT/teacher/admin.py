from teacher.models import Teacher 
from django.contrib import admin


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    pass
