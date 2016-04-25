from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User

from course_mang.models import CourseDetail
from student.models import EnrolledCourses

'''
User can Create his/her custom goal for courses with respect to time and marks in tests.
'''
class Goal(models.Model):
	enr_course = models.ForeignKey(EnrolledCourses, related_name = 'goal_enr_course', blank = True)
	user = models.ForeignKey(User)

	goal_name  = models.CharField(max_length = 100)
	start_module  = models.CharField(max_length = 100)
	end_module  = models.CharField(max_length = 100)
	goal_description = models.CharField(max_length = 250, null = True, blank = True)
	pass_percentage = models.IntegerField(null=True, blank= True)
	
	goal_start_time = models.DateField(auto_now_add = True)
	goal_end_time = models.DateField(auto_now_add = True)

	can_update = models.BooleanField(default = False)

	added_date = models.DateTimeField(auto_now_add = True)
	updated_date = models.DateTimeField(auto_now = True)


class GoalModel(ModelForm):
    class Meta:
        model = Goal
        exclude = ('user',)
# Create your models here.
