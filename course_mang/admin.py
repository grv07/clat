from course_mang.models import CourseDetail 
from django.contrib import admin


@admin.register(CourseDetail)
class CourseDetailAdmin(admin.ModelAdmin):
    exclude = ('enroll_start_date','enroll_end_date','course_start_date','course_end_date','course_start_time','course_end_time','course_demo_file_url',)

