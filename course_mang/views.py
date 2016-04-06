from django.shortcuts import render, render_to_response, redirect
from course_mang.models import CourseDetail, CourseWeek
import json
from django.http import HttpResponse
from user_login.models import City
from django.contrib.auth.decorators import login_required
from .utilities import SECTORS_ASSOCIATES_CHOICES, student_required, is_enrolled
from CLAT.services import tracking_engine
from course_test_handling.models import Tests
from django.contrib import messages
from student.models import UserCourseProgress
import logging
logger = logging.getLogger(__name__)

def course_submit(request):
	pass

@login_required()
def articulate_video_action(request, course_uuid, week_uuid, module_name, folder_name):
	data={}
	data['course_uuid'] = course_uuid
	data['module_name'] = module_name
	data['week_uuid'] = week_uuid
	data['folder_name'] = folder_name

	return render(request, 'course_mang/show_articulate_video.html', {'data': data})

@login_required
def video_action(request, path):
	try:
		logger.info('Under course_mang.video_action')
		if path:
			data = {}
			path_split = path.split('/')
			course = CourseDetail.objects.get(course_uuid = path_split[4])
			enrolled_status_and_obj = is_enrolled(request.user, course)
			logger.info('course_mang.video_action >> Enroll Status for user is '+str(enrolled_status_and_obj))
			if enrolled_status_and_obj[0]:
				logger.info('Student is enrolled on course')
				course_week = CourseWeek.objects.get(week_module_name = path_split[6], week_uuid = path_split[5])
				if UserCourseProgress.objects.get(course_week = course_week, enrolled_courses = enrolled_status_and_obj[1]).access_status == 'OPEN':
					data['course_uuid'] = course.course_uuid
					data['path'] = path
					data['module_name']=path_split[6]
					return render(request, 'course_mang/only_video.html', data)
			else:
				messages.error(request, 'You are not enrolled.')
		else:
			return Http404
	except Exception as e:
		logger.error('course_mang.view.video_action '+str(e.args)+' UID-'+str(request.user.id))
		return redirect('/dashboard/')


@login_required
@student_required
def inline_progress(request, course_uuid, module_name):
	logger.info('>>>>>> Under course_mang.inline_progress')
	print 'underrnnnnnnn'
	if request.method == 'GET':
		try:
			data = {}
			course = CourseDetail.objects.get(course_uuid = course_uuid)
			data['course'] = course
			data['bar_width'] = 15
			data['week_module_name'] = module_name
			return render(request, 'student/inline_progress.html', data)
		except Exception as e:
			print e.args
			logger.error('course_mang.view.inline_progress '+str(e.args)+' UID-'+str(request.user.id))
	return redirect('/dashboard/')


@login_required
def video_action_teacher(request, path):
	if path:
		data = {}
		path_split = path.split('/')
		course = CourseDetail.objects.get(course_uuid = path_split[4])
		data['course_uuid'] = course.course_uuid
		data['path'] = path
		data['module_name']=path_split[6]
		return render(request, 'course_mang/only_video.html', data)
	return redirect('/dashboard/')


	
@login_required()
def utb_video_action(request, video_url):
	return render(request, 'course_mang/view_youtube_course_video.html', {'link': video_url})

@login_required()
def mp4_demo_action(request, uuid):
	course_obj = CourseDetail.objects.get(course_uuid=uuid)
	return render(request, 'course_mang/view_demo_course_video.html', {'course_obj': course_obj})

@login_required()
def mp4_video_action(request, course_uuid, module_name, week_uuid, video_file_name):
	data={}
	data['course_uuid'] = course_uuid
	data['module_name'] = module_name
	data['week_uuid'] = week_uuid
	data['video_file_name'] = video_file_name
	
	return render(request, 'course_mang/view_mp4_course_video.html', {'data': data})

@login_required()
def course_name_validation(request):
	if request.method == 'GET':

		_error = HttpResponse(json.dumps(False), content_type = "application/json")
		_success = HttpResponse(json.dumps(True), content_type = "application/json")

		try:
			if CourseDetail.objects.get(course_name = request.GET.get('course_name')):
				return _error
			else:
				return _success
		except Exception as e:
			logger.error('course_mang.view.course_name_validation '+str(e.args)+' UID-'+str(request.user.id))
			return _success
	else:
		return _success


def state_india(request):
	try:
		from django.core import serializers
		city_list = City.objects.using('city').all()
		data = serializers.serialize('json', city_list, fields = ('id', 'city_name'))
		return HttpResponse(data, content_type = 'application/json')
	except Exception as e:
		logger.error('course_mang.view.state_india '+str(e.args))
		return HttpResponse([], content_type = 'application/json')




# AJAX GET request for loading modules of navigated course
def get_modules(request):
	try:
		c_id = request.GET['c_id']
		week_objs = CourseWeek.objects.filter(course = c_id).order_by('added_date')
		available_modules = [week.week_module_name for week in week_objs if week.is_available == True]
		return HttpResponse(json.dumps(available_modules), content_type = 'application/json')
	except Exception as e:
		logger.error('course_mang.view.get_modules '+str(e.args))
		return HttpResponse(json.dumps([]), content_type = 'application/json')


def all_courses(request):
	data={}
	try:
		offset = 6
		searched_course_name = request.GET.get('course_name',None)

		if searched_course_name == None or len(searched_course_name.replace(' ','')) == 0 or len(searched_course_name) == 0:
			course_list = CourseDetail.objects.filter()[:offset]
		else:
			course_list = CourseDetail.objects.filter(course_name__icontains = searched_course_name.strip())[:offset]
			if len(course_list) == 0:
				course_list = []

		data = {'course_list':course_list,'searched_course_name':searched_course_name}
		data['total_courses'] = len(CourseDetail.objects.all())

		from collections import OrderedDict

		count_for_courses = OrderedDict()
		for i in SECTORS_ASSOCIATES_CHOICES:
			count_for_courses[i[0]] = CourseDetail.objects.filter(course_sectors_and_associates = i[0]).count()
		count_for_courses = OrderedDict(sorted(count_for_courses.items(), key = lambda x: -x[1]))
		data['filtered_courses_by_numbers'] = count_for_courses
	except Exception as e:
		logger.error('course_mang.view.all_courses '+str(e.args))
	return render(request, 'course_mang/all_courses.html', data)


def filter_courses(request):
	if request.is_ajax() and request.method == 'GET':
		try:
			offset = 6
			based_on = request.GET.get('based_on')
			course_type_value = request.GET.get('course_type_value')

			from django.template.loader import get_template
			from django.template import Context

			if based_on == 'course_type':
				value = request.GET['value']
				course_list = [course for course in CourseDetail.objects.filter(course_sectors_and_associates__iexact = value)[:offset]]
				t = get_template('course_mang/course_list.html')
				html = t.render(Context({'course_list': course_list,'request':request}))

				return HttpResponse(json.dumps({'html':html, 
					'course_count':len(CourseDetail.objects.filter(course_sectors_and_associates__iexact=value)),'category_name':value}), content_type='application/json')
			
			elif course_type_value:
				start_course_type = int(request.GET.get('start_course_type'))
				course_list = [course for course in CourseDetail.objects.filter(course_sectors_and_associates__iexact=course_type_value)[offset*(start_course_type-1):offset*start_course_type]]
				t = get_template('course_mang/course_list.html')
				html = t.render(Context({'course_list': course_list,'request':request}))
				
				return HttpResponse(json.dumps({'start_course_type':start_course_type, 'html':html}), content_type = 'application/json')
			
			else:
				return HttpResponse(json.dumps(False), content_type = 'application/json')
		except Exception as e:
			logger.error('course_mang.view.filter_courses '+str(e.args))
			return HttpResponse(json.dumps(False), content_type = 'application/json')




def more_courses(request):
	if request.is_ajax() and request.method == 'GET':
		try:
			offset = 6
			from django.template.loader import get_template
			from django.template import Context

			start = int(request.GET.get('starting_filter_score'))
			course_list = [course for course in CourseDetail.objects.filter()][offset*(start-1):offset*start]
			t = get_template('course_mang/course_list.html')
			html = t.render(Context({'course_list': course_list,'request':request}))

			return HttpResponse(json.dumps({'starting_filter_score':start, 'html':html, 'course_count':len(course_list)}), content_type = 'application/json')
		except Exception as e:
			logger.error('course_mang.view.more_courses '+str(e.args))
			return HttpResponse(json.dumps(False), content_type = 'application/json')


def get_course_names(request):
	if request.is_ajax():
		results = []
		try:
			q = request.GET.get('term', '')
			courses = CourseDetail.objects.filter(course_name__icontains = q)
			for course in courses:
				results.append(course.course_name)
		except Exception as e:
			logger.error('course_mang.view.get_course_names '+str(e.args))
		return HttpResponse(json.dumps(results), content_type = 'application/json')


@login_required
def check_module(request):
	try:
		module_name = request.GET.get('module_name')
		el_id = request.GET.get('el_id')
		return HttpResponse(json.dumps(True), content_type = 'application/json')
	except Exception as e:
		logger.error('course_mang.view.check_module '+str(e.args)+' UID-'+str(request.user.id))
		return HttpResponse(json.dumps(False), content_type = 'application/json')



@login_required
def check_module_under_week(request):
	try:
		week_number = request.GET.get('checkforweek')
		num_of_modules = len(CourseWeek.objects.filter(week_number = week_number, course = CourseDetail.objects.get(course_uuid = request.GET.get('c_uuid'))))
		if num_of_modules < 4:
			return HttpResponse(json.dumps(True), content_type = 'application/json')
		else:
			return HttpResponse(json.dumps(False), content_type = 'application/json')
	except Exception as e:
		logger.error('course_mang.view.check_module_under_week '+str(e.args)+' UID-'+str(request.user.id))
		return HttpResponse(json.dumps(False), content_type = 'application/json')


@login_required
@student_required
def post_time_spent(request):	
	if request.method == 'POST' and request.is_ajax():
		try:
			time_spent = int(float(request.POST.get('_timespent')))
			current_url = request.POST.get('_currentpath')
			
			if not request.session.get('_timespent',None):
				request.session['_timespent'] = time_spent
			else:
				request.session['_timespent'] += time_spent
			# When collect-time more then 60
			if request.session['_timespent'] >= 60:	
				tracking_engine.start_tracking(request.user, current_url, request.session['_timespent'])
				del request.session['_timespent']
			return HttpResponse(json.dumps(True), content_type = 'application/json')
		except Exception as e:
			logger.error('course_mang.view.post_time_spent '+str(e.args)+' UID-'+str(request.user.id))
			if request.session['_timespent'] > 0:	
				tracking_engine.start_tracking(request.user, current_url, request.session['_timespent'])
				del request.session['_timespent']
			return HttpResponse(json.dumps(False), content_type = 'application/json')
	else:
		return HttpResponse(json.dumps(False), content_type = 'application/json')
