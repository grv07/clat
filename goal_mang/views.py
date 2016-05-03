from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.models import User

import json
from django.shortcuts import redirect

from course_mang.models import CourseDetail, CourseWeek
from student.models import EnrolledCourses
from models import GoalModel, Goal, GoalBadge

from form import CreateGoalForm

@login_required()
def create_goal(request):
	if request.method == 'GET':
		enroll_courses = EnrolledCourses.objects.all()
		data = {'enroll_courses' : enroll_courses}
		return render(request, 'goal_mang/create_goal.html', data)

	elif request.method == 'POST':
	 	create_goal = CreateGoalForm(request.POST)
	 	user = request.user
	 	if create_goal.is_valid():
	 		if not Goal.objects.filter(user = user, goal_name = request.POST.get('goal_name')):
		 		goal = GoalModel(data = request.POST)
		 		goal.enr_course = EnrolledCourses.objects.get(pk = request.POST.get('enr_course'))
		 		goal = goal.save(commit = False)
		 		goal.user = request.user
		 		goal.save()
		 		badges_id_list = request.POST.getlist('badges')
		 		goal_badges = GoalBadge.objects.create(goal = goal, user = request.user)
		 		if badges_id_list:
		 			for badges_id in badges_id_list:
		 				goal_badges.add_badge_to_list(badges_id)
		 		messages.success(request,'Goal create successfully.')
		 	else:
		 		messages.info(request,'This goal name exit with this course.')

	 		data = {'enroll_courses' : EnrolledCourses.objects.all()}
	 		
	 		return render(request, 'goal_mang/create_goal.html', data)
	 	else:
	 		enroll_courses = EnrolledCourses.objects.all()
	 		data = {'form' : create_goal, 'enroll_courses' : enroll_courses}
	 		messages.error(request,'Please try again.')
	 		return render(request, 'goal_mang/create_goal.html', data)

@login_required()
def goal_list_actions(request):
	goals = Goal.objects.filter(user_id = request.user.id)
	
	data = {'goals': goals}
	return render(request, 'goal_mang/goal_list.html', data)

@login_required()
def goal_delete_action(request, goal_id):
	goal = Goal.objects.get(pk = goal_id)
	goal.delete()
	return redirect('/goal/list/')	

@login_required()
def get_module_name_list(request):
	if request.method == 'GET':
		try:
			week_module_names = list(CourseWeek.objects.filter(course = EnrolledCourses.objects.get(pk = 
				request.GET.get('enr_course_id')).course).values('week_module_name'))
			
			week_module_names =  [module_name.get('week_module_name') for module_name in week_module_names]
			
			return HttpResponse(json.dumps(week_module_names), content_type = "application/json")
		except Exception as e:
			print e.args
			return HttpResponse(False, content_type = "application/json")



# Create your views here.
