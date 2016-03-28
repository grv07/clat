from django import template
from course_mang.models import CourseDetail, CourseWeek
from CLAT.services import mail_handling,course_service

register = template.Library()

@register.filter(name='course_week')
def course_week(value):
    return course_service.duration_of_course(value.course_start_date,value.course_end_date)

# @register.filter(name='convert_to_courseweek_obj')
# def course_week(value):
#     return CourseWeek.objects.get()
