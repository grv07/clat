from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from course_mang.models import CourseDetail, CourseWeek, CourseVideos, CourseInformation, CourseImage
from CLAT.services import pagination, mail_handling,course_service, constants
from teacher.models import Teacher
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import TeacherModel
from .form import TeacherRegistrationForm
from user_login.models import AddressModel,City
from course_mang.utilities import teacher_required, check_quiz_link, edit_schedule_info, create_users_xls, admin_required
from course_mang.form import CourseImageForm
from django.contrib.auth.decorators import login_required
import json, os
from course_test_handling.models import Tests
from student.models import EnrolledCourses
from django.contrib.auth.models import User
from django.db import IntegrityError
from student.models import Student
# from django.core.servers.basehttp import FileWrapper
from wsgiref.util import FileWrapper
import logging

logger = logging.getLogger(__name__)

''' Teacher Home page '''
@teacher_required
def teacher_home(request):
	data = {}
	if request.user.is_authenticated():
		courses_owned = CourseDetail.objects.filter(teacher=request.user)
		data['courses_owned'] = courses_owned
	return render(request,'teacher/teacher_home.html',data)


''' Teacher Home page '''
@login_required
@teacher_required
def rescue_enroll(request):
	if request.is_ajax() and request.method == 'POST':
		try:
			course = CourseDetail.objects.get(course_uuid = request.POST.get('productinfo'), teacher = request.user)
		except User.DoesNotExist as e:
			print e.args
			msg = 'Unable to find this course with given credentials.'
			return HttpResponse(json.dumps(msg), content_type="application/json")

		from student.views import enroll_student
		from payment.models import CoursePayment
		from course_mang.utilities import check_payment
		status,extra = (None, None,)
		payment_status, result = check_payment(request.POST.get('txnid'))
		if payment_status:
			status, extra = enroll_student(request)
		# User can enroll ....
		if status == 0 and extra:
			logger.info('payment.success >> Under --CAN-- enroll for course ----')
			try:
				# ToDo
				from course_mang.utilities import check_payment

				status, result = check_payment(request.POST.get('txnid'))
				extra_data = {}
				if status:
					extra_data = result.get('transaction_details').get(request.POST.get('txnid'))
				# print extra_data,type(extra),extra_data.get('txnid')
				coursepayment = CoursePayment.objects.create(enrolledcourse = extra, txnid = extra_data.get('txnid'), extra_data = str(extra_data))
				#print 'course payment obj created success .....'
				# print coursepayment
				if coursepayment:
					msg = 'You are now enrolled in '+extra.course.course_name+' .'+'Amt. Rcvd = Rs'+ request.POST.get('amount')+'/-,'+'Status = '+extra_data.get('unmappedstatus')+','+'Txn Id = '+extra_data.get('txnid');
					# messages.success(request,msg, extra_tags='safe')
					extra.status = 'COURSE-PAYMENT-SUCCESS'
					print 'success >>>>>>>>>>> :) :) ;)'
					extra.save()
					logger.info('payment.success >>  SUCCESS user-email: '+request.POST.get('email'))
			except Exception as e:
				print e.args
				msg = 'There is a problem in saving transaction details!'
				logger.error('payment.success >>  H>>>>T---- '+ msg + ' ' + str(e.args)+' user-email: '+request.POST.get('email','NA')+ ' txnid: '+extra_data.get('txnid','NA')) 
				# messages.error(request, msg)
				if extra:
					extra.delete()
		
		elif status == 1 and extra:
			logger.error('teacher.rescue_enroll >>  Unable to enroll'+extra.course_name)
			msg = 'Unable to enroll in '+extra.course_name+' .'

		elif status == 2 and extra:
			logger.error('teacher.rescue_enroll >>  You are already enrolled in'+extra.course_name)
			msg = 'User is already enrolled in '+extra.course_name+' .'
		
		else:
			logger.error('teacher.rescue_enroll >>  TRANSACTION_ERROR_SERVER')
			msg = 'User unable to enroll in course-name: '+course.course_name+' .'
			# return HttpResponse(constants.TRANSACTION_ERROR_SERVER)			
		return HttpResponse(json.dumps(msg), content_type="application/json")

@teacher_required
def download_xls(request, course_uuid):

	course = CourseDetail.objects.get(course_uuid = course_uuid, teacher = request.user)
	# user_list = []
	if course:
		_users_enroll_course = EnrolledCourses.objects.filter(course = course)
		# user_list = [enroll_course.user for enroll_course in _users_enroll_course]

	try:
		assert _users_enroll_course,'Assert Error: Not have any user'
	except Exception as e:
		messages.info(request, 'Unable to find enrolled user(s) in this course.')
		return redirect('/teacher/manage/'+course_uuid)
	_sm_course_name = 'course_id_'+str(course.id)
	if create_users_xls(users_enroll_course = _users_enroll_course, _sm_course_name = _sm_course_name, course_name = course.course_name):
		dir_name = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
		file_dir_path = 'xls/'+_sm_course_name 
		filename = dir_name+'/'+file_dir_path+'/enrolled_user.xls'
		wrapper = FileWrapper(file(filename))
		response = HttpResponse(wrapper, content_type='text/plain')
		response['Content-Disposition'] = 'attachment; filename=%s' % os.path.basename(filename)
		response['Content-Length'] = os.path.getsize(filename)
		return response
	else:
		messages.error(request,'Error in your request please try again after some time.')
		return redirect('/teacher/manage/'+course_uuid)


'''Teacher register action'''
def teacher_register(request):
	if request.method == 'POST':
		post_req_data = request.POST
		data = {}
		register_form = TeacherRegistrationForm(data=post_req_data)
		teacher_model = TeacherModel(data=post_req_data)
		if register_form.is_valid():
			try:
				teacher_model = TeacherModel(data=post_req_data)
				if teacher_model.is_valid():
					address_model = AddressModel(data=post_req_data)
					if address_model.is_valid():
						try:
							city = City.objects.get(city_name=post_req_data.get('city', ''))
							address = address_model.save(commit=False)
							address.city_obj = city
							address.street1 = post_req_data.get('street1', '')
							address.street2 = post_req_data.get('street2', '')
							address.pincode = post_req_data.get('pincode', '')
							address.save()
						except Exception as e:
							print e.args
						try:
							import uuid
							teacher = teacher_model.save(commit=False)
							
							teacher.address = address
							teacher.uuid_key = uuid.uuid4()
							teacher_pass = post_req_data.get('password')
							teacher.set_password(teacher_pass)
							teacher.gender = post_req_data.get('gender',None) 
							p_date = post_req_data.get('d_o_b',None)
							
							if p_date:
								import datetime
								d_o_b = datetime.datetime.strptime(p_date, '%m/%d/%Y').date()
								teacher.d_o_b = d_o_b
							else:
								pass
							teacher.higher_education = post_req_data.get('higher_education',None)
							teacher.is_active = False
							teacher.save()
							kawrgs = {'teacher_pass' : teacher_pass,'teacher_uname' : teacher.username}
							messages.success(request,'Teacher created. Please ask the server administrator to activate your account.')
							return HttpResponseRedirect('/teacher/login/')
						except Exception as e:
							print e.args
					else:
						data = {'form': address_model,'register_error':True}
				else:
					data = {'form': teacher_model,'register_error':True}
			
			except Exception as e:
				print e.args
		else:
			data = {'form': register_form,'register_error':True}
		return render(request, 'teacher/register_teacher.html', data)
	else:
		teacher_form = TeacherModel()
		return render(request, 'teacher/register_teacher.html', {'form':teacher_form})




''' Teacher login action '''
def teacher_login(request):
	if request.user.is_authenticated():
		messages.info(request,'Please logout first and then re-login with a different account.')
		return HttpResponseRedirect('/home/')
	if request.method == 'POST':
		t_username = request.POST.get('username')
		t_password = request.POST.get('password')
		try:
			t_user = authenticate(username=t_username, password=t_password)
			teacher = Teacher.objects.get(pk=t_user.id)
		except Exception as e:
			t_user = None
			teacher = None
		if teacher is not None:
			if t_user.is_active:
				login(request, t_user)
				messages.success(request,'You logged in successfully.')
				return HttpResponseRedirect('/teacher/')
			else:
				messages.warning(request,'Your account is not yet active.')
				return render(request, 'teacher/login_teacher.html', {'t_not_active': True, 'next': request.POST.get('next')})
		else:
			course_list = CourseDetail.objects.all()
			course_list = pagination.get_paginated_list(obj_list=course_list,page = request.GET.get('page'))
			messages.error(request,'Please enter valid credentials.')
			return render(request, 'teacher/login_teacher.html', {'t_login_error': True, 'next': request.POST.get('next')})
	else:
		return render(request,'teacher/login_teacher.html',{})



@login_required
@teacher_required
def manage_course(request, course_uuid):
	data={}
	weeks={}
	course = CourseDetail.objects.get(course_uuid = course_uuid)
	data['course'] = course
	course_weeks = CourseWeek.objects.filter(course = course).order_by('module_number')
	data['course_weeks'] = course_weeks
	if course.course_durations == '01':
		num_of_weeks = abs(course_service.duration_of_course(course.course_start_date,course.course_end_date))
	else:
		num_of_weeks = course.course_durations
	data['weeks'] = num_of_weeks
	data['course_image_form'] = CourseImageForm()
	return render(request,'teacher/manage_course.html',data)


@login_required
@teacher_required
def change_display_image_video(request):
	course = CourseDetail.objects.get(course_uuid = request.POST.get('_c_id'))
	if course:
		if course.course_demo_file == 'img':
			course.course_demo_file = 'utb'
			msg = 'Now onwards Course Video will be displayed on detail page.'
		elif course.course_demo_file == 'utb':
			course.course_demo_file = 'img'
			msg = 'Now onwards Course Image will be displayed on detail page.'
		course.save()
		messages.success(request,msg)
		return HttpResponse(json.dumps(True), content_type="application/json")
	return HttpResponse(json.dumps(False), content_type="application/json")


@login_required
@teacher_required
def get_modules(request):
	course = CourseDetail.objects.get(course_uuid = request.GET.get('_c_id'))
	if course:
		modules = CourseWeek.objects.filter(course = course, week_number = request.GET.get('week')).order_by('module_number')
		modules_name = [week_obj.week_module_name for week_obj in modules]
		if modules_name:
			return HttpResponse(json.dumps(modules_name), content_type="application/json")
	return HttpResponse(json.dumps(modules_name), content_type="application/json")
 


@login_required
@teacher_required
def get_week_details(request):
	course = CourseDetail.objects.get(course_uuid=request.GET.get('_c_id'))
	if course:
		course_week = CourseWeek.objects.get(course=course,week_number=request.GET.get('week'),week_module_name=request.GET.get('module'))
		if course_week:
			return HttpResponse(json.dumps(course_week.week_detail), content_type="application/json")
	return HttpResponse(json.dumps(''), content_type="application/json")



@login_required
@teacher_required
def get_ordering(request):
	course = CourseDetail.objects.get(course_uuid=request.GET.get('_c_id'))
	if course:
		course_week = CourseWeek.objects.get(course=course,week_number=request.GET.get('week_number'),week_module_name=request.GET.get('module_name'))
		if course_week:
			print course_week
			return HttpResponse(json.dumps(course_week.module_number), content_type="application/json")

	return HttpResponse(json.dumps(''), content_type="application/json")




@login_required
@teacher_required
def update_courseweek_details(request):
	if request.method == 'POST' and request.is_ajax():
		course = CourseDetail.objects.get(course_uuid=request.POST.get('_c_id'))
		if course:
			course_week = CourseWeek.objects.get(course=course,week_number=request.POST.get('_week'),week_module_name=request.POST.get('_module'))
			if course_week:
				course_week.week_detail = request.POST.get('_week_details').strip()
				course_week.save()
				messages.info(request,'Course week details updated for '+request.POST.get('_module')+' module under week '+request.POST.get('_week'))
				return HttpResponse(json.dumps(True), content_type="application/json")
		return HttpResponse(json.dumps(False), content_type="application/json")



@login_required
@teacher_required
def update_course_details(request):
	if request.method == 'POST' and request.is_ajax():
		course_description = '\n'+request.POST.get('_c_desc').strip()
		course_objective = '\n'+request.POST.get('_c_objve').strip()
		course_eligibility = '\n'+request.POST.get('_c_eligbty').strip()
		course_crt_benefits = '\n'+request.POST.get('_c_cbf').strip()
		course_short_desc = '\n'+request.POST.get('_c_csd').strip()
		if len(course_description)<10 or len(course_objective) < 10 or len(course_eligibility) < 10:
			messages.error(request,'All 3 fields must have at least 10 characters.')
			return HttpResponse(json.dumps(True), content_type="application/json")
		course = CourseDetail.objects.get(course_uuid=request.POST.get('_c_id'))
		if course:
			try:
				course.course_information.description = course_description
				course.course_information.objective = course_objective
				course.course_information.crt_benefits = course_crt_benefits
				course.course_information.eligibility = course_eligibility
				course.course_information.short_description = course_short_desc
				course.course_information.save()
				messages.success(request,'Course details updated.')
				return HttpResponse(json.dumps(True), content_type="application/json")
			except Exception as e:
				CourseInformation.objects.create(course = course,course_description=course_description,course_objective=course_objective)

		return HttpResponse(json.dumps(False), content_type="application/json")



@login_required
@teacher_required
def update_course_demo_image(request):
	if request.method == 'POST':
		course = CourseDetail.objects.get(course_uuid=request.POST.get('course_id'))
		if 'picture' in request.FILES:
			picture = request.FILES.get('picture')
			if str(picture).split('.')[1] in constants.IMAGES_EXT_ALLOWED:
				
				try:
					if course.course_image.picture  != constants.DEFAULT_COURSE_IMAGE:
						os.remove(constants.ROOT_PATH_FOR_VIDEOS + str(course.course_image.picture))
					course.course_image.picture = picture
					course.course_image.save()    
				except Exception as e:
					print e.args
					CourseImage.objects.create(course = course, picture = constants.DEFAULT_COURSE_IMAGE) 
				
				messages.success(request,'Course image changed.')
			else:
				messages.error(request,'This image format is not allowed. Only jpg, png and gifs are allowed.')
			return HttpResponseRedirect('/teacher/manage/'+course.course_uuid+'/')
		else:
			messages.error(request,'No course image provided!!!')
			return HttpResponseRedirect('/teacher/manage/'+course.course_uuid+'/')



@login_required
@teacher_required
def update_course_type_name(request):
	if request.is_ajax() and request.method == 'POST':
		course = CourseDetail.objects.get(course_uuid=request.POST.get('_c_id'))
		course_duration = int(request.POST.get('_c_duration'))

		if course:
			if any([week_obj.week_number > course_duration for week_obj in course.course_week.all()]):
				messages.error(request,'Some module(s) exist inside weeks.Delete them and then change course duration.')
				return HttpResponseRedirect('/teacher/manage/'+course.course_uuid+'/')
			course.course_name = request.POST.get('_c_name').strip()
			course.course_sectors_and_associates = request.POST.get('_c_type')
			course.course_durations = course_duration
			course.save()
			messages.success(request,'Details updated successfully!!!')
			return HttpResponse(json.dumps(True), content_type="application/json")
		return HttpResponse(json.dumps(False), content_type="application/json")



@login_required
@teacher_required
def delete_course_module(request):
	if request.is_ajax() and request.method == 'POST':
		try:
			course = CourseDetail.objects.get(course_uuid=request.POST.get('_c_id'))
			total_modules = CourseWeek.objects.filter(course=course).count()
			module_name = request.POST.get('_module')
			week = request.POST.get('_week')
			end=110
			import shutil
			if CourseWeek.objects.filter(course = course, week_module_name = module_name, week_number = week):
				course_week = CourseWeek.objects.get(course = course, week_module_name = module_name, week_number = week)
				deleted_module_number = course_week.module_number 
				if CourseVideos.objects.filter(course=course,week=course_week,module_name=module_name):
					course_video = CourseVideos.objects.get(course=course,week=course_week,module_name=module_name)
					if course_video.video_type == 'articulate':
						end=117
					to_be_deleted = str(str(course_video.video_file)[:end])+'/'+str(module_name)+'/'
					if os.path.isdir(to_be_deleted):
						shutil.rmtree(to_be_deleted)
						course_video.delete()
						course_week.delete()
					else:
						return HttpResponse(json.dumps(False), content_type="application/json")
				else:
					course_week.delete()
				for i in xrange(deleted_module_number+1,total_modules+1):
					module = CourseWeek.objects.get(course=course,module_number = i)
					module.module_number = module.module_number - 1
					module.save()
				messages.success(request,'Week '+ week +' : Module named '+ module_name +' and all its contents are deleted successfully.')
			else:
				return HttpResponse(json.dumps(False), content_type="application/json")
		except Exception as e:
			print e.args
			return HttpResponse(json.dumps(False), content_type="application/json")

		return HttpResponse(json.dumps(True), content_type="application/json")


@login_required
@teacher_required
def delete_module_video(request):
	'''Delete a video of perticular module and able to re-fill it with new video'''
	if request.is_ajax() and request.method == 'POST':
		try:
			course = CourseDetail.objects.get(course_uuid = request.POST.get('_c_id'))
			# total_modules = CourseWeek.objects.filter(course = course).count()
			module_name = request.POST.get('_module')
			week = request.POST.get('_week')
			
			import shutil

			course_week = CourseWeek.objects.filter(course = course, week_module_name = module_name, week_number = week)
			assert course_week,'AssertError: this course_week not found with course'
			course_week = course_week[0]
			# deleted_module_number = course_week.module_number
			course_video = CourseVideos.objects.filter(course = course, week = course_week, module_name = module_name)
			assert course_video,'AssertError: this course_video not found with course' 
			course_video = course_video[0]

			to_be_deleted = '/'.join(str(course_video.video_file).split('/')[:-1])
			# print to_be_deleted
			if os.path.isdir(to_be_deleted):
				shutil.rmtree(to_be_deleted)
				course_video.delete()
				course_week.is_available = True
				course_week.save()
			else:
				return HttpResponse(json.dumps(False), content_type = "application/json")
			messages.success(request,'Week '+ week +' : Module named '+ module_name +' all its video(s) deleted successfully.')
			
		except Exception as e:
			print e.args
			return HttpResponse(json.dumps(False), content_type = "application/json")

		return HttpResponse(json.dumps(True), content_type = "application/json")


@login_required
@teacher_required
def create_quiz(request, course_uuid):                        
	data = {}
	course = CourseDetail.objects.get(course_uuid=course_uuid)
	data['course'] = course
	if not course.course_durations:
		duration = course_service.duration_of_course(course.course_start_date,course.course_end_date)
		data['course_duration_list'] = [i for i in xrange(1,duration+1)]
	else:
		data['course_duration_list'] = [i for i in xrange(1,int(course.course_durations)+1)]

	if request.method == 'POST':
		quiz_type = request.POST.get('quiz_type')    # quiz_category is module_name for inline and week_number for mid-term
		schedule_key = request.POST.get('quiz_url1').strip().split('/')[-1]
		schedules_key_list = []
		if check_quiz_link(request.POST.get('quiz_url1').strip()):
			module_name = request.POST.get('quiz_category')		
			if quiz_type == constants.QUIZ_TYPES[0]:

				try:
					schedule_key2 = request.POST.get('quiz_url2').strip().split('/')[-1]
					schedule_key3 = request.POST.get('quiz_url3').strip().split('/')[-1]
					
					if not check_quiz_link(request.POST.get('quiz_url2').strip()) or not check_quiz_link(request.POST.get('quiz_url3').strip()):
						messages.info(request,'Only Mettl URLs are accepted')
						return redirect('/teacher/manage/'+course.course_uuid+'/createquiz/')
					
					if schedule_key == schedule_key2 or schedule_key2 == schedule_key3 or schedule_key3 == schedule_key:
						messages.error(request,'Duplicate Quiz URLs not allowed!!!')
						return redirect('/teacher/manage/'+course.course_uuid+'/createquiz/')
		   
					have_any_with = lambda  schedule_key : Tests.objects.filter(schedule_key = schedule_key).count();
					
					if have_any_with(schedule_key) or have_any_with(schedule_key2) or have_any_with(schedule_key3):
						messages.error(request,'Duplicate Quiz URLs not allowed!!!')
						return redirect('/teacher/manage/'+course.course_uuid+'/createquiz/')	
					

					if Tests.objects.filter(course = course, module_name = module_name).count() < 3:
						if Tests.objects.create(course = course, schedule_key = schedule_key, module_name = module_name, test_type = constants.TEST_TYPES[0]):
							schedules_key_list.append(schedule_key)
							if Tests.objects.create(course = course, schedule_key = schedule_key2, module_name = module_name, test_type = constants.TEST_TYPES[0]):
								schedules_key_list.append(schedule_key2) 
								if Tests.objects.create(course = course, schedule_key = schedule_key3, module_name = module_name, test_type = constants.TEST_TYPES[0]):
									schedules_key_list.append(schedule_key3)
									messages.success(request,'All Inline tests are created for module '+module_name+'.')
								else:
									messages.error(request,'Problem in creating third inline tests.')
							else:
								messages.error(request,'Problem in creating second inline tests.')
						else:
							messages.error(request,'Problem in creating first inline tests.')
					else:
						messages.warning(request,'All tests are created.')

				except IntegrityError as ie:
					print ie.args
					messages.error(request,'Duplicate Quiz URL not allowed.')

			elif quiz_type == constants.QUIZ_TYPES[3]:
				schedules_key_list = []
				try:
					if Tests.objects.filter(course = course, test_type = constants.TEST_TYPES[2]).count() == 0:
						endterm_quiz = Tests.objects.create(course = course, module_name = module_name, test_type = constants.TEST_TYPES[2], schedule_key = schedule_key)
						if endterm_quiz:
							schedules_key_list.append(schedule_key)
							messages.success(request,'End Term Quiz created for module '+module_name+'.')
						else:
							messages.error(request,'Problem in creating End Term Quiz for module '+module_name+'.')
					else:
						messages.error(request,'Only 1 End Quiz can exists for course '+str(course.course_name)+'.')
				except IntegrityError as ie:
					print ie.args
					messages.error(request,'Duplicate Quiz URL not allowed.')

				

			elif quiz_type == constants.QUIZ_TYPES[2]:
				schedules_key_list = []
				casestudy_quiz_limit = 0
				if len(data['course_duration_list']) == 16:
					casestudy_quiz_limit = 1
				try:
					if Tests.objects.filter(course = course, module_name = module_name, test_type = constants.TEST_TYPES[3]).count() <= casestudy_quiz_limit:
						casestudy_quiz = Tests.objects.create(course = course, module_name = module_name,test_type = constants.TEST_TYPES[3], schedule_key=schedule_key)
						if casestudy_quiz:
							schedules_key_list.append(schedule_key)
							messages.success(request,'Case Study created for module '+module_name+'.')
						else:
							messages.error(request,'Problem in creating Case Study for module '+module_name+'.')
					else:
						messages.error(request,'Case Study already present for course '+str(course.course_name)+'.')
				except IntegrityError as ie:
					print ie.args
					messages.error(request,'Duplicate Quiz URL not allowed.')

				

			elif quiz_type == constants.QUIZ_TYPES[1]:
				# if len(data['course_duration_list']) == 16:
				schedules_key_list = []
				try:
					if Tests.objects.filter(course = course, module_name = module_name, test_type = constants.TEST_TYPES[1]).count() == 0:
						midterm_quiz = Tests.objects.create(course = course, module_name = module_name, test_type = constants.TEST_TYPES[1], schedule_key = schedule_key)
						if midterm_quiz:
							schedules_key_list.append(schedule_key)
							messages.success(request,'Mid Term Quiz created for module '+module_name+'.')
						else:
							messages.error(request,'Problem in creating Mid Term Quiz for module '+module_name+'.')
					else:
						messages.error(request,'Only 1 Mid Quiz can exists for course '+str(course.course_name)+'.')
				except IntegrityError as ie:
					print ie.args
					messages.error(request,'Duplicate Quiz URL not allowed.')
				# else:
				# 	messages.error(request,'Mid-term test is only available for course having 16 weeks duration.')
			else:
				message.info(request,'We can not get it , what you try to add.')
				pass		
			print [edit_schedule_info(schedule_key) for schedule_key in schedules_key_list]
		else:
			messages.info(request,'Only Mettl URL links are accepted.')
			pass
			
	return render(request,'course_test_handling/create_quiz.html',data)




@login_required
@teacher_required
def change_ordering(request,course_uuid):
	course = CourseDetail.objects.get(course_uuid=course_uuid)
	if request.method == 'POST' and request.is_ajax():
		try:
			old_order = int(request.POST.get('_c_old_number'))
			new_order = int(request.POST.get('_c_new_number'))

			def get_course_week(course, module_number):
				try :
					return CourseWeek.objects.get(course = course, module_number = module_number)
				except Exception as e:
					return None

			module_name = request.POST.get('_c_module_name')

			if old_order == 0:
				if not get_course_week(course = course, module_number = new_order):
					module = CourseWeek.objects.get(course = course, week_module_name = module_name)
					module.module_number = new_order
					module.save()
				else:
					messages.error(request,'Already have a module with this number, please select unique one.')

				return HttpResponse(json.dumps(True), content_type = "application/json")
				
			else:
				old_module = get_course_week(course = course, module_number = old_order)
				old_module.module_number = new_order

				new_module = get_course_week(course = course, module_number = new_order)
				old_module.save()

				new_module.module_number = old_order
				new_module.save()

				messages.success(request,'Module Numbers exchanged successfully.')

				return HttpResponse(json.dumps(True), content_type = "application/json")

		except Exception as e:
			messages.error(request,str(e.args))
			return HttpResponse(json.dumps(False), content_type="application/json")	
		return HttpResponse(json.dumps(False), content_type="application/json")
	
	data={}
	course_weeks = CourseWeek.objects.filter(course=course)
	if not course.course_durations:
		duration = course_service.duration_of_course(course.course_start_date,course.course_end_date)
		course_duration = [i for i in xrange(1,duration+1)] 
	else:
		course_duration = [i for i in xrange(1,int(course.course_durations)+1)]
	weeks = {}
	for week in course_duration:
		weeks[week] = course_weeks.filter(week_number=week).order_by('module_number')
	data['weeks'] = weeks
	data['total_modules'] = len(course_weeks)
	return render(request,'teacher/change_ordering.html',data)




@login_required
@teacher_required
def isInline(request):
	try:
		if request.is_ajax():
			course = CourseDetail.objects.get(course_uuid = request.GET.get('_c_id'))
			tests = Tests.objects.filter(course = course, module_name = request.GET.get('module'))
			if tests.count() == 3:
				return HttpResponse(json.dumps(True), content_type = "application/json")
			return HttpResponse(json.dumps(False), content_type = "application/json")
	except Exception as e:
		return HttpResponse(json.dumps(False), content_type = "application/json")



@login_required
@teacher_required
def getTestLink(request):
	try:
		if request.is_ajax():
			course = CourseDetail.objects.get(course_uuid = request.GET.get('_c_id'))
			test = Tests.objects.get(course = course, module_name = request.GET.get('module'))
			return HttpResponse(json.dumps(test.schedule_key), content_type = "application/json")
	except Exception as e:
		return HttpResponse(json.dumps(None), content_type = "application/json")




@login_required
@teacher_required
def getInlineTestLink(request):
	try:
		if request.is_ajax():
			version = int(request.GET.get('version'))
			course = CourseDetail.objects.get(course_uuid = request.GET.get('_c_id'))
			test = Tests.objects.filter(course = course, module_name = request.GET.get('module'))[version-1]
			return HttpResponse(json.dumps(test.schedule_key), content_type = "application/json")
	except Exception as e:
		print e.args
		return HttpResponse(json.dumps(None), content_type = "application/json")


@login_required
@teacher_required
def change_testschedules(request, course_uuid):
	data = {}
	course = CourseDetail.objects.get(course_uuid = course_uuid)
	data['course'] = course
	if not course.course_durations:
		duration = course_service.duration_of_course(course.course_start_date,course.course_end_date)
		data['course_duration_list'] = [i for i in xrange(1,duration+1)] 
	else:
		data['course_duration_list'] = [i for i in xrange(1,int(course.course_durations)+1)]

	if request.method == 'POST':
		req_post = request.POST
		newtestlink = req_post.get('newtestlink')
		if edit_schedule_info(newtestlink):
			try:
				test = Tests.objects.filter(course = course)

				if req_post.get('week') != 'FINAL TEST':
					oldtestlink = req_post.get('oldtestlink')
					test_obj = test.get(module_name = req_post.get('module'), schedule_key = oldtestlink)
					test_obj.schedule_key = newtestlink
					test_obj.save()
					if test_obj.test_type == constants.TEST_TYPES[0]:
						messages.success(request,'Test link changed for Inline test - '+ req_post.get('inlinetestnumber') +' under '+ req_post.get('module')+' .')
					elif test_obj.test_type == constants.TEST_TYPES[1]:
						messages.success(request,'Test link changed for Mid-term test under '+ req_post.get('module')+' .')
				else:
					test_obj = test.get(module_name = constants.END_TEST_MODULE)
					test_obj.schedule_key = newtestlink
					test_obj.save()
					messages.success(request,'Test link changed for End-term test.')
			except IntegrityError as ie:
				messages.error(request,'Duplicate Test link not allowed.')
		else:
			messages.info(request,'Invalid Test Key : Test link must be a METTL generated key.')
		return redirect(request.get_full_path())
		
	return render(request,'teacher/change_tests.html',data)


"""
ADMIN SECTION
"""
@login_required
@admin_required
def anaylse(request):
	data = {}
	teacher_list = Teacher.objects.all()
	data['teacher_list'] = Teacher.objects.all()
	data['student_list'] = Student.objects.all()
	data['course_list'] = CourseDetail.objects.all()

	return render(request, 'teacher/admin_analyse.html', data)



@login_required
@admin_required
def downloadxlsall(request):
	import datetime
	from CLAT.services import xls_engine
	
	if request.is_ajax() and request.method == 'GET':
		try:
			options = {
						'1' : { 'model' : CourseDetail, 'nameoffile' : 'allcourses'},
						'2' : { 'model' : Teacher, 'nameoffile' : 'allteachers'},
						'3' : { 'model' : Student, 'nameoffile' : 'allstudents'}
						}
			optionselected = str(request.GET.get('_option'))
			_list = options[optionselected]['model'].objects.all()

			if _list:
				if optionselected == '1':
					wb = xls_engine.all_courses(_list)
				
				if optionselected == '2':
					wb = xls_engine.all_teachers(_list)

				if optionselected == '3':
					wb = xls_engine.all_students(_list)
					
				file_dir_path = 'xls/'+options[optionselected]['nameoffile']
				if not os.path.exists(file_dir_path):
						os.makedirs(file_dir_path)
				assert wb,'AssertError: Work sheet not generated'				
				wb.save(file_dir_path + '/' + options[optionselected]['nameoffile'] +'.xls')
				return HttpResponse(json.dumps([True,options[optionselected]['nameoffile']]), content_type="application/json")
		except Exception as e:
			print e.args
			messages.error(request,'Unable to generate excel file.Try again.')
			return HttpResponse(json.dumps([False,None]), content_type="application/json")
	return HttpResponse(json.dumps([False,None]), content_type="application/json")


@login_required
@admin_required
def downloadfile(request,filename):
	try:
		if filename:
			dir_name = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
			file_dir_path = 'xls/'+filename
			filepath = dir_name+'/'+file_dir_path+'/'+ filename +'.xls'
			wrapper = FileWrapper(file(filepath))
			print filepath
			response = HttpResponse(wrapper, content_type='text/plain')
			response['Content-Disposition'] = 'attachment; filename=%s' % os.path.basename(filepath)
			response['Content-Length'] = os.path.getsize(filepath)
			return response
		else:
			messages.error(request,'Cannot download the file. No file present.')
	except Exception as e:
		print e.args
		messages.error(request,'The given file does not exist.Try again.')
	return redirect('/anaylse/')


@login_required
@admin_required
def activateCourse(request):
	try:
		if request.is_ajax() and request.method == 'POST':
			course = CourseDetail.objects.get(course_name=request.POST.get('_c_name'))
			if not course.can_enroll:
				course.can_enroll = True
				course.save()
				messages.success(request,'Course '+request.POST.get('_c_name')+' has been activated.Now students can see it.')
			else:
				messages.warning(request,'Course '+request.POST.get('_c_name')+' is already activated.')
			return HttpResponse(json.dumps(True), content_type = "application/json")
		return HttpResponse(json.dumps(False), content_type = "application/json")
	except Exception as e:
		print e.args
		return HttpResponse(json.dumps(False), content_type = "application/json")


@login_required
@teacher_required
def verify_transaction(request):
	if request.is_ajax() and request.method == 'POST':
		from course_mang.utilities import check_payment
		status, result = check_payment(request.POST.get('txnid'))
		return HttpResponse(json.dumps([status, result]), content_type = "application/json")
