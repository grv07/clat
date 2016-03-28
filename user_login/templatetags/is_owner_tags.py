from django import template
import datetime
from course_mang.models import CourseDetail
from course_mang.utilities import is_verified_user
register = template.Library()


@register.filter(name='is_owner')
def is_course_owner(value, arg):
    return value == arg

@register.filter(name='is_verify')
def is_verify(value):
	return is_verified_user(user = value)
    	

@register.simple_tag
def is_course_owner2(course_id = None, user_id = None):
    return False