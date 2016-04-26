from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.models import User


import json


from course_mang.models import CourseDetail, CourseWeek
from student.models import EnrolledCourses

from models import GoalModel, Goal
from form import CreateGoalForm

@login_required()
def create_goal(request):
	if request.method == 'GET':
		enroll_courses = EnrolledCourses.objects.all()
		data = {'enroll_courses' : enroll_courses}
		return render(request, 'goal_mang/create_goal.html', data)

	elif request.method == 'POST':
		print type(request.user)
	 	create_goal = CreateGoalForm(request.POST)
	 	user = request.user
	 	if create_goal.is_valid():
	 		goal = GoalModel(data = request.POST)
	 		goal.enr_course = EnrolledCourses.objects.get(pk = request.POST.get('enr_course'))
	 		goal = goal.save(commit = False)
	 		goal.user = request.user
	 		goal.save()

	 		messages.success(request,'Goal create successfully.')
	 		data = {'enroll_courses' : EnrolledCourses.objects.all()}
	 		
	 		return render(request, 'goal_mang/create_goal.html', data)
	 	else:
	 		print create_goal.errors
	 		enroll_courses = EnrolledCourses.objects.all()
	 		data = {'form' : create_goal, 'enroll_courses' : enroll_courses}
	 		messages.error(request,'Please try again.')
	 		return render(request, 'goal_mang/create_goal.html', data)

@login_required()
def get_module_name_list(request):
	if request.method == 'GET':
		try:
			week_module_names = list(CourseWeek.objects.filter(course = CourseDetail.objects.get(pk = request.GET.get('course_id'))).values('week_module_name'))
			week_module_names =  [module_name.get('week_module_name') for module_name in week_module_names]
			return HttpResponse(json.dumps(week_module_names), content_type = "application/json")
		except Exception as e:
			print e.args
			return HttpResponse(False, content_type = "application/json")

@login_required()
def goal_list_actions(request):
	goals = Goal.objects.filter(user_id = request.user.id)
	# print request.user.id
	data = {'goals': goals}
	return render(request, 'goal_mang/goal_list.html', data)

# Create your views here.