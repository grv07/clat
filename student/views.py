from django.shortcuts import render, redirect
import json, os, sys
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from form import StudentRegistrationForm, UserForm, StudentProfileForm
from django.contrib.auth.models import User
from student.models import Student, StudentModel, StudentInterests, Certificate, EnrolledCourses, ProfilePicture, UserCourseProgress
from user_login.models import AddressModel, City, Address
from user_login import user_actions
from user_login.tasks import send_mail
from CLAT.services import constants
from CLAT.cities import cities
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from course_mang.utilities import student_required, CACHE_KEYS, verify_account, verification_mail
from teacher.models import Teacher
from course_mang.models import CourseDetail
from student.form import ProfilePictureForm
from django.views.decorators.csrf import csrf_exempt
from allauth.socialaccount.models import SocialAccount
from course_test_handling.models import Tests
from assesment_engine.models import AssesmentRegisterdUser, UserResult
from user_login.templatetags.test_tags import check_for_max_marks, module_inline_list, inline_test_key, module_midterm_list
from django.core.cache import cache
# from payu.utils import generate_hash, verify_hash
import logging

logger = logging.getLogger(__name__)
# app_folder = os.path.abspath(os.path.join(os.path.dirname(__file__) , "../"))
# sys.path.insert(0,app_folder + "/mettl-api-sdk/src")


# from com.mettl.api.register.CandidateRegister import CandidateRegister
# from com.mettl.api.results.Results import Results
# from com.mettl.model.Candidates import Candidates
# from com.mettl.api.assessment.AssessmentInfo import AssessmentInfo
# from com.mettl.api.schedule.CreateSchedule import CreateSchedule
# from com.mettl.api.schedule.ScheduleInfo import ScheduleInfo
# from com.mettl.api.schedule.EditScheduleInfo import EditScheduleInfo


def register_student_form(request):
	return render(request, 'register.html')


def user_action(request):
	post_req_data = request.POST
	# print post_req_data
	data = {}
	user_form = UserForm(data=request.POST)
	register_form = StudentRegistrationForm(data=post_req_data)
	student_model = StudentModel(data=post_req_data)
	if  user_form.is_valid() and register_form.is_valid():
		try:
			if student_model.is_valid():
				address_model = AddressModel(data=post_req_data)
				if address_model.is_valid():
					try:
						city = City.objects.get(city_name = post_req_data.get('city', ''))
						assert city,'AssertError: city not found in database'
						address = address_model.save(commit = False)
						address.city_obj = city
						address.save()
					except Exception as e:
						logger.error('under student.view.user_action '+str(e.args))
						messages.error(request,'Error when trying to create the user. Please try again.')
						data = {'form': register_form,'register_error':True,'value_state':post_req_data.get('state', ''),'value_city':post_req_data.get('city', ''),'mailing_addr':post_req_data.get('mailing_address', '')}
						return render(request, 'register.html', data)

					try:
						user = user_form.save()
						# print user.password
						user.set_password(user.password)
						user.email = post_req_data.get('email',None)
						# print user.email
						user.save()
						import uuid
						student = student_model.save(commit=False)
						student.student = user           
						student.address = address
						student.uuid_key = 'eq' + str(uuid.uuid4().fields[-1])[:8]
						student_pass = post_req_data.get('password',None)
						student.gender = post_req_data.get('gender',None)
						p_date = post_req_data.get('d_o_b',None)
						
						if p_date:
							import datetime
							d_o_b = datetime.datetime.strptime(p_date, '%m/%d/%Y').date()
							student.d_o_b = d_o_b
						else:
							pass
						student.higher_education = post_req_data.get('higher_education',None)
						student.i_agree = post_req_data.get('i_agree')
						student.save()
						kawrgs = {'student_pass' : student_pass,'student_uname' : user.username,'phone_number' : student.phone_number, 'full_name' : student.full_name, 'uuid_key' : student.uuid_key}
						verification_mail(user = user.id,domain = request.META['HTTP_HOST'],**kawrgs)
						return user_actions.login_user(request)
					except Exception as e:
						logger.error('under student.view.user_action '+str(e.args))
				else:
					data = {'form': address_model,'register_error':True,'value_state':post_req_data.get('state', ''),'value_city':post_req_data.get('city', ''),'mailing_addr':post_req_data.get('mailing_address', '')}
			else:
				data = {'form': student_model,'register_error':True , 'value_state':post_req_data.get('state', ''),'value_city':post_req_data.get('city', ''),'mailing_addr':post_req_data.get('mailing_address', '')}
		
		except Exception as e:
			logger.error('under student.view.user_action '+str(e.args))
	else:
		messages.error(request,'Error when trying to create the User.')
		data = {'form': register_form,'register_error':True,'value_state':post_req_data.get('state', ''),'value_city':post_req_data.get('city', ''),'mailing_addr':post_req_data.get('mailing_address', '')}
	return render(request, 'register.html', data)


def user_account_verification(request, uuid):
	student = None
	try:
	   student = Student.objects.get(uuid_key = uuid)
	   if verify_account(student):
		  messages.success(request,'Your account successfully verified.Please login.')
		  return redirect('/home/')
	   else:
		  messages.info(request,'You account has been verified already.')
		  return redirect('/home/')
	except Exception as e:
		logger.error('under student.view.user_account_verification '+str(e.args))
		messages.info(request,'Your account is not registered with us or already has been verified.') 
		return redirect('/home/')


def username_verification(request):
	if request.method == 'GET':
		try:
			if User.objects.filter(username=request.GET.get('username')).count() > 0:
				return HttpResponse(json.dumps(False), content_type="application/json")
			else:
				return HttpResponse(json.dumps(True), content_type="application/json")
		except Exception as e:
			logger.error('under student.view.username_verification '+str(e.args))
			return HttpResponse(json.dumps(True), content_type="application/json")
	else:
		return HttpResponse(json.dumps(True), content_type="application/json")


def user_email_verification(request):
	if request.method == 'GET':
		try:
			if User.objects.filter(email=request.GET.get('email')).count() > 0:
				return HttpResponse(json.dumps(False), content_type="application/json")
			else:
				return HttpResponse(json.dumps(True), content_type="application/json")
		except Exception as e:
			logger.error('under student.view.user_email_verification '+str(e.args))
			return HttpResponse(json.dumps(True), content_type="application/json")
	else:
		return HttpResponse(json.dumps(True), content_type="application/json")

def email_in_db(request):
	if request.method == 'GET':
		try:
			if User.objects.filter(email=request.GET.get('email')).count() > 0:
				return HttpResponse(json.dumps(True), content_type="application/json")
			else:
				return HttpResponse(json.dumps(False), content_type="application/json")
		except Exception as e:
			logger.error('under student.view.email_in_db '+str(e.args))
			return HttpResponse(json.dumps(False), content_type="application/json")
	else:
		return HttpResponse(json.dumps(False), content_type="application/json")

def user_phone_number_verification(request):
	if request.method == 'GET':
		result = False
		try:
			if request.user.is_authenticated():
				condition1 = Student.objects.filter(phone_number=request.GET.get('phone_number')).exclude(student=request.user).count()>0
			else:
				condition1 = Student.objects.filter(phone_number=request.GET.get('phone_number')).count()>0
			condition2 = Teacher.objects.filter(phone_number=request.GET.get('phone_number')).count()>0
			condition = condition1 or condition2
			if not request.GET.get('m') == constants.PHONE_VERIFY_USES[1] :
				if condition:
					result = False
				else:
					result = True
			else:
				if condition:
					result = True
				else:
					result = False

		except Exception as e:
			logger.error('under student.view.user_phone_number_verification '+str(e.args))
			result = False
		return HttpResponse(json.dumps(result), content_type="application/json")


def get_cities(request):
	state=request.GET['state']
	return HttpResponse(json.dumps(cities[state]), content_type="application/json")


@login_required
@student_required
def profile(request):
	data = {}
	try:
		user_id = request.user.id
		profile_picture_form = ProfilePictureForm()
		data['profile_picture_form'] = profile_picture_form
		data['e'] = False
		if request.method == 'POST':
			post_req_data = request.POST
			if Student.objects.filter(student = user_id):
				student = Student.objects.get(student = user_id)
			else:
				student = None
			student_form = StudentProfileForm(data = post_req_data, request = request)
			if student_form.is_valid():
				if Student.objects.filter(student = user_id):

					from .student_service import update_user_profile

					if update_user_profile(post_req_data, student):
						messages.success(request,' Profile details updated successfully.')
					else:
						messages.error(request,' Cannot update profile !!! ')
				else:
					city_created = City.objects.filter(city_name = post_req_data.get('city'), city_state = post_req_data.get('state'))[0]
					if city_created:
						address_created = Address.objects.create(city_obj=city_created,country=post_req_data.get('country'),street1=post_req_data.get('street1',''),street2=post_req_data.get('street2',''),pincode=post_req_data.get('pincode',''))
						if address_created:
							import uuid
							p_date = post_req_data.get('d_o_b')
							if p_date:
								import datetime
								d_o_b = datetime.datetime.strptime(p_date, '%m/%d/%Y').date()
								student_created = Student.objects.create(student = User.objects.get(id=user_id),uuid_key = uuid.uuid4(),full_name = post_req_data.get('full_name',''),address = address_created,phone_number = post_req_data.get('phone_number','1234567890'),\
									gender = post_req_data.get('gender'),d_o_b = d_o_b,higher_education = post_req_data.get('higher_education'),fblink = post_req_data.get('fblink'),glink = post_req_data.get('glink'))
							else:
								logger.error('under student.view.profile unable to get d_o_b paramter')
							if student_created:
								messages.success(request,'Profile details updated successfully.')
			else:
				data['student_form'] = student_form
				data['logged_user'] = post_req_data
				data['e'] = True
				if ProfilePicture.objects.filter(user=user_id) :
					user_profile_picture = ProfilePicture.objects.get_obj(user=user_id)
					data['profile_pic'] = user_profile_picture.picture
					if user_profile_picture.picture == constants.DEFAULT_PROFILE_IMAGE:
						data['is_default_picture'] = True
				return render(request, 'student/profile.html', data)

			return HttpResponseRedirect('/profile/')

		else:
			if Student.objects.filter(student = user_id):
				user = Student.objects.get(student=user_id)
				data['logged_user'] = user
			else:
				social_acc = SocialAccount.objects.filter(user=user_id)[0]
				if social_acc.provider == 'google':
					if social_acc.extra_data.has_key('id'):
						data['socialaccount_g_id'] = social_acc.extra_data.get('id', '')

				elif social_acc.provider == 'facebook':
					if social_acc.extra_data.has_key('id'):
						data['socialaccount_fb_id'] = social_acc.extra_data.get('id', '')

				messages.info(request,'Please update your profile.')
			if ProfilePicture.objects.filter(user=user_id) :
					user_profile_picture = ProfilePicture.objects.get_obj(user=user_id)
					data['profile_pic'] = user_profile_picture.picture
					if user_profile_picture.picture == constants.DEFAULT_PROFILE_IMAGE:
						data['is_default_picture'] = True
	except Exception as e:
		logger.error('under student.view.profile '+str(e.args))
		# else:
		# 	if SocialAccount.objects.filter(user=user_id):
		# 		if SocialAccount.objects.filter(user=user_id)[0].provider == 'google':
		# 			data['socialaccount_picture'] = SocialAccount.objects.get(user=user_id).extra_data['picture']
		

	return render(request, 'student/profile.html', data)



@csrf_exempt
@login_required
@student_required
def save_profile_picture(request):
	try:
		if request.method == 'POST':
			if 'picture' in request.FILES:
				from .student_service import update_thumbnail
				profile_picture_form = ProfilePictureForm(data=request.POST)
				if profile_picture_form.is_valid():
					user_profile_picture = update_thumbnail(request.user,request.FILES.get('picture',None))
					if not user_profile_picture:
						user_profile_picture = ProfilePicture.objects.create(user=User.objects.get(id=request.user.id),picture=request.FILES.get('picture'))
				else:
					return profile_picture_form.errors            
				import json
				return HttpResponse(json.dumps({'success':True,'file_name': constants.OLD_ROOT_PATH_FOR_VIDEOS + str(user_profile_picture.picture)}), content_type="application/json")
			else:
				return HttpResponse(json.dumps({'success':False,'file_name': constants.OLD_ROOT_PATH_FOR_VIDEOS + str(user_profile_picture.picture)}), content_type="application/json")
		else:
			user_profile_picture = ProfilePicture.objects.get(user=request.user.id)    
			import json
			return HttpResponse(json.dumps({'success':True,'file_name': constants.OLD_ROOT_PATH_FOR_VIDEOS + str(user_profile_picture.picture)}), content_type="application/json")                    
	except Exception as e:
		logger.error('under student.view.remove_profile_picture '+str(e.args))
		return HttpResponse(json.dumps({}), content_type="application/json")


@csrf_exempt
@login_required
@student_required
def remove_profile_picture(request):
	if request.method == 'POST' and request.is_ajax():
		try:
			from .student_service import update_thumbnail
			profile_picture_obj = update_thumbnail(request.user)
			if profile_picture_obj:
				return HttpResponse(json.dumps(True), content_type="application/json")
		except Exception as e:
			logger.error('under student.view.remove_profile_picture '+str(e.args))
		return HttpResponse(json.dumps(False), content_type="application/json")


def verify_certificate(request):
	if request.method == 'GET':
		return render(request,'student/verify_certificate.html')
	else:
		uuid_key = request.POST.get('cert_id',None)
		try:
			certificate = Certificate.objects.get(uuid_key = uuid_key)
			user_name = certificate.enr_course.user.username
			course_name = certificate.enr_course.course.course_name
			messages.success(request,'&nbsp;Certificate is assign to <b>{0}</b> with <b>{1}</b>, <br><b>G.P.A:&nbsp;{2}</b>'.format(user_name.upper(), course_name.upper(), certificate.marks_score), extra_tags='safe')
			return render(request,'student/verify_certificate.html',{'code':uuid_key,'marks_score':certificate.marks_score, 'username':user_name,'coursename':course_name, 'total_marks':certificate.max_marks})
		except Exception as e:
			logger.error('under student.verify_certificate >>> '+str(e.args))
			messages.error(request,'Unable to find certificate with this register id')
			return render(request,'student/verify_certificate.html')	



def enroll_student(request):
	if request.method == 'POST':
		enrolled = None
		try:
			total_modules = 0
			course_uuid = request.POST.get('productinfo', None)
			if course_uuid:
				user = request.user
				course = CourseDetail.objects.get(can_enroll=True, course_uuid = course_uuid)
				if not EnrolledCourses.objects.is_student_enrolled(user, course):
					enrolled = EnrolledCourses.objects.enroll_student(user, course)
					if enrolled:
						try:
							# cache.set(CACHE_KEYS['d'] % request.user.id,None)
							all_weeks = course.course_week.all().order_by('added_date')
							for week in all_weeks:
								UserCourseProgress.objects.create(course_week = week, enrolled_courses = enrolled)
							first_module = UserCourseProgress.objects.get(course_week = all_weeks[0], enrolled_courses = enrolled)
							if first_module:
								total_modules = len(all_weeks)
								first_module.access_status = constants.ACCESS_STATUSES[0]
								first_module.save()
							else:
								logger.error('under student.view.verify_certificate cannot get or open first module of course.'+' UID-'+str(request.user.id))
						except Exception as e:
							print e.args
							logger.error('under student.view.enroll_student '+str(e.args)+' UID-'+str(request.user.id))
							if enrolled:
								enrolled.delete()
							return (1,course,)
						stu_inter = StudentInterests.objects.filter(user = user)
						if stu_inter.count() == 1:
							interests_obj = stu_inter[0]
							if course.course_sectors_and_associates not in interests_obj.category:
								interests_obj.category = str(interests_obj.category)+";"+str(course.course_sectors_and_associates)
								interests_obj.save()
								# print interests_obj.category
						else:
							interest_added = StudentInterests.objects.create(user = user,category = course.course_sectors_and_associates)
							# print interest_added
						from CLAT.services.cron_engine import enroll_success

						if not enroll_success(enrolled, request.POST.get('txnid', None), total_modules):
							logger.error('under student.view.enroll_student unable to email post course enroll message.'+' UID-'+str(request.user.id))
						return (0,enrolled,)					
					else:
						return (1,course,)
				else:
					return (2,course,)
		except Exception as e:
			print e.args
			logger.error('under student.enroll_student >>>> '+str(e.args)+' UID-'+str(request.user.id))
			return (-1,enrolled,)

@login_required
@student_required
def enroll(request):
	status, extra = enroll_student(request)
	if status == 0:
		messages.success(request, "Sucessfully enrolled  in "+str(extra.course.course_name.upper()))
		return redirect('/dashboard/') 
	elif status == 1:
		messages.error(request,'Unable to enroll in '+extra.course_name.upper()+' .')
		return redirect('/course/details/'+extra.course_uuid+'/') 
	elif status == 2:
		messages.info(request,'You are already enrolled in '+extra.course_name.upper()+' .')
		return redirect('/course/videos/'+extra.course_uuid+'/')
	else:
		return HttpResponse(constants.TRANSACTION_ERROR_SERVER)

@login_required
def unenroll_student(request,course_uuid):
	if request.method == 'POST':
		user = request.user
		course = CourseDetail.objects.get(course_uuid=course_uuid, can_enroll=True)
		if EnrolledCourses.objects.is_student_enrolled(user,course):
			enrolled = EnrolledCourses.objects.unenroll_student(user,course)
			if enrolled:
				messages.info(request,'You are now unenrolled from '+course.course_name+'.')
				return HttpResponseRedirect('/dashboard/')
			else:
				messages.error(request,'Unable to unenroll from '+course.course_name+'.')
				return HttpResponse('error in unenrolling')
		else:
			messages.info(request,'Not allowed : You are not enrolled in '+course.course_name+'.')
			return HttpResponseRedirect('/course/details/'+str(course.course_uuid)+'/')


@login_required
@student_required
def dashboard(request):
	user = request.user
	data = {}
	# d_cache = cache.get(CACHE_KEYS['d'] % request.user.id)
	# print d_cache,'*'*80
	# if not d_cache:
	total_courses_enrolled = EnrolledCourses.objects.list_all_courses_enrolled(user)
	data['total_courses_enrolled'] = total_courses_enrolled
	data['total_courses'] = len(EnrolledCourses.objects.filter(user = user))
	# cache.set(CACHE_KEYS['d'] % request.user.id, data)
	return render(request, 'student/dashboard.html', data)
	# return render(request, 'student/dashboard.html', d_cache)


@login_required
@student_required
def fetch_enrolled_courses(request):
	if request.is_ajax():
		try:
			from django.template.loader import get_template
			from django.template import Context
			
			start = int(request.GET.get('start_at_enrolledcourse'))
			total_courses_enrolled = EnrolledCourses.objects.list_all_courses_enrolled(request.user,3*(start-1),3*start)
			t = get_template('student/_student_dashboard.html')
			html = t.render(Context({'total_courses_enrolled': total_courses_enrolled,'view_report_link':False,'request':request,'user':request.user}))
			ajax_data = {'start_at_enrolledcourse':start,'html':html}
		except Exception as e:
			logger.error('under student.view.fetch_enrolled_courses '+str(e.args)+' UID-'+str(request.user.id))
		return HttpResponse(json.dumps(ajax_data), content_type="application/json")


@login_required
@student_required
def test_progress(request, course_uuid):
	try:
		data = {}
		course = CourseDetail.objects.get(course_uuid = course_uuid, can_enroll=True)
		if EnrolledCourses.objects.is_student_enrolled(request.user, course):
			data['course'] = course
			tests = Tests.objects.get(course = course)
			if tests:
				# bar_width = tests.filter(test_type = constants.TEST_TYPES[2]).count() + tests.filter(test_type = constants.TEST_TYPES[1]).count() + tests.filter(test_type = constants.TEST_TYPES[0]).count()
				# data['bar_width'] = float(100/bar_width)
				# if data['bar_width'] >= 15:
				data['bar_width'] = 10
				return render(request,'student/test_progress.html', data)
			else:
				messages.info(request,'No course tests are present.')
				return HttpResponseRedirect('/course/details/'+str(course.course_uuid)+'/')
			
		messages.error(request,'You are not an enrolled user.')
	except Exception as e:
		print e.args
		logger.error('under student.view.test_progress '+str(e.args)+' UID-'+str(request.user.id))
	return redirect('/home/')



@login_required
@student_required
def download_test_report(request, test_type, schedule_key):
	try:
		asm_obj = AssesmentRegisterdUser.objects.get(student = request.user, schedule_key = schedule_key)
		return redirect(UserResult.objects.get(assesmentRegisterdUser = asm_obj).report_link)
	except Exception as e:
		logger.error('under student.view.download_test_report '+str(e.args)+' UID-'+str(request.user.id))
		#messages.error(request,'Sorry, we cannot generate your '+test_type+' test report.')
		messages.error(request,'Error : Invalid link for '+test_type+' test report.')
		return redirect('/dashboard/')

'''
def is_inlines_attempt(course):
	tests = Tests.objects.filter(course = course)
	total_inline_tests = tests.filter(test_type = 'I')
	for test in total_inline_tests:
		all_grades_list += [ checkFor for asreguser in AssesmentRegisterdUser.objects.filter(test = test, course = course, student = user) if asreguser.result_status == checkFor]
'''

'''
A helper function checking whether student has passed all tests in the enrolled course.
'''
def isAllTestsGradedOrPassed(request, course, user, checkFor, module_inline_list = None):
	try:
		tests = Tests.objects.filter(course = course)

		total_inline_tests = tests.filter(test_type = constants.TEST_TYPES[0])
		total_midterm_tests = tests.filter(test_type = constants.TEST_TYPES[1])
		total_endterm_test = tests.filter(test_type = constants.TEST_TYPES[2], module_name = constants.END_TEST_MODULE)

		if checkFor == constants.TEST_CHECK_FOR[0]:
			all_grades_list = []
			for test in tests:
				all_grades_list += [ checkFor for asreguser in AssesmentRegisterdUser.objects.filter(test = test, course = course, student = user) if asreguser.result_status == checkFor]
			total_tests = total_inline_tests.count()//3 + total_midterm_tests.count() + total_endterm_test.count()
			if total_tests == len(all_grades_list):
				return True

		elif checkFor == constants.TEST_CHECK_FOR[1]:
			grade = []
			if module_inline_list:
				for module in module_inline_list:
					inline_tests_in_module = total_inline_tests.filter(module_name = module.week_module_name)
					inline_graded_tests = 0
					inline_pass_tests = 0
					for each_inline in inline_tests_in_module:
						for asreguser in AssesmentRegisterdUser.objects.filter(test = each_inline, course = course, student = user):
							if asreguser.test_status == checkFor :
								inline_graded_tests += 1
							if asreguser.result_status == constants.TEST_CHECK_FOR[0]:
								inline_pass_tests += 1

					if inline_graded_tests in [1, 2]:
						if inline_pass_tests == 0:
							messages.info(request,'First give all inline tests under '+module.week_module_name+' .Only then you are eligible for certificate.')
							return False
						elif inline_pass_tests == 1:
							grade.append(True)
					elif inline_graded_tests == 3:
						if inline_pass_tests == 0 or inline_pass_tests == 1:
							grade.append(True)
						else:
							messages.info(request,'First give all inline tests under '+module.week_module_name+' .Only then you are eligible for certificate.')
							return False
					else:
						messages.info(request,'First give all inline tests under '+module.week_module_name+' .Only then you are eligible for certificate.')
						return False

			if total_midterm_tests:
				asreguser = AssesmentRegisterdUser.objects.filter(test = total_midterm_tests[0], course = course, student = user, test_status = constants.TEST_CHECK_FOR[1])
				if asreguser:
					grade.append(True)
				else:
					messages.info(request,'First give mid term tests under '+total_midterm_tests[0].module_name+' .Only then you are eligible for certificate.')
					return False

			if total_endterm_test:
				asreguser = AssesmentRegisterdUser.objects.filter(test = total_endterm_test[0], course = course, student = user, test_status = constants.TEST_CHECK_FOR[1])
				if asreguser:
					grade.append(True)
				else:
					messages.info(request,'First give end term test. Only then you are eligible for certificate.')
					return False
			if all(grade):
				return True
		
		return False
	except Exception as e:
		logger.error('under student.view.isAllTestsGradedOrPassed '+str(e.args)+' UID-'+str(request.user.id))
		return False


'''
A helper function which is called when student wishes to download certificate. This saves the info in certificate table.
'''
def saveCertificateDetails(request, course, status, module_inline_list, module_midterm_list):
	try:
		user = request.user
		enroll_course = EnrolledCourses.objects.get(course = course, user = user)
		certificate_filter = Certificate.objects.filter(enr_course = enroll_course)
		if not certificate_filter:
			total_marks = 0.0
			marks_scored = 0.0
			assreguser_lists = []

			for module_name_inline_test in module_inline_list:
				inline_test = inline_test_key(module_name_inline_test.week_module_name, course)
				assreguser = AssesmentRegisterdUser.objects.filter(test_status = constants.TEST_CHECK_FOR[1], schedule_key = check_for_max_marks(inline_test, user),student = request.user)		
				if assreguser:
					assreguser_lists.append(assreguser[0])
			
			for module_name_mid_test in module_midterm_list:
				mid_test = Tests.objects.get(module_name=module_name_mid_test.week_module_name,course = course, test_type = constants.TEST_TYPES[1])				
				assreguser = AssesmentRegisterdUser.objects.get(test = mid_test, test_status = constants.TEST_CHECK_FOR[1], student = request.user)

				assreguser_lists.append(assreguser)

			end_test = Tests.objects.get(module_name = constants.END_TEST_MODULE, course = course, test_type = constants.TEST_TYPES[2])
			assreguser_lists.append(AssesmentRegisterdUser.objects.get(test = end_test, student = request.user, test_status = constants.TEST_CHECK_FOR[1], schedule_key = end_test.schedule_key))

			for assreguser in assreguser_lists:
				userresult = UserResult.objects.get(assesmentRegisterdUser = assreguser)
				total_marks += float(userresult.max_marks)
				marks_scored += float(userresult.marks_scored)

			import uuid
			certificate = Certificate.objects.create(uuid_key = 'EQ'+str(uuid.uuid4().fields[-1])[:8], enr_course = enroll_course, status = status, max_marks = total_marks, marks_score  = marks_scored)         
			if certificate:
				messages.info(request,'Certificate information for '+ course.course_name +' is generated .')
				from course_mang.utilities import CERTIFICATE_MAIL_HTML
				send_mail.delay(html_part = CERTIFICATE_MAIL_HTML.format(course = course.course_name, link = 'http://Clat.co/lms/media/certificate/'+certificate.uuid_key+'/cert.png'), to = request.user.email, subject = 'Clat certificate link')

		else:
			certificate = certificate_filter[0]
			messages.info(request,'Already have certificate information.')

		from CLAT.services.certificate_generation_engine import create_certificate
		return (certificate, create_certificate(certificate_id = certificate.uuid_key, fullname = user.username, coursename = course.course_name, added_date = certificate.added_date))
	except Exception as e:
		logger.error('under student.view.saveCertificateDetails '+str(e.args)+' UID-'+str(request.user.id))
		return None


'''
If isAllTestGraded() returns True then user is eligible for certificate.Download It.
'''
@login_required
@student_required
def download_certificate(request, course_uuid):
	data = {}
	course = CourseDetail.objects.get(course_uuid = course_uuid)
	module_inlines = module_inline_list(course)
	module_midterms = module_midterm_list(course)

	if request.method == 'POST':
		return redirect('/dashboard/')
	else:
		certificate = None	
		if isAllTestsGradedOrPassed(request, course, request.user, constants.TEST_CHECK_FOR[1], module_inlines):
			try:
				if isAllTestsGradedOrPassed(request, course, request.user, constants.TEST_CHECK_FOR[0]):
					status = constants.CERTIFICATE_RESULT[0]
				else:
					status = constants.CERTIFICATE_RESULT[1]
				data['status'] = status
				certificate, certificate_path = saveCertificateDetails(request, course, status, module_inlines, module_midterms)
				data['code'] = certificate.uuid_key
				data['marks_score'] = certificate.marks_score
				data['total_marks'] = certificate.max_marks
				data['username'] = request.user.username
				data['coursename'] = course.course_name 
			except Exception as e:
				logger.error('under student.view.download_certificate '+str(e.args)+' UID-'+str(request.user.id))
				messages.error(request, 'Error in download_certificate')
			return render(request, 'student/verify_certificate.html',data)		
		else:
			return redirect('/dashboard/')




@login_required
@student_required
def certificates(request):
	data = {}
	try:
		data['courses_certificates'] = []
		enroll_courses = EnrolledCourses.objects.filter(user = request.user)
		for enroll_course in enroll_courses:
			data['courses_certificates'] +=  Certificate.objects.filter(enr_course = enroll_course)
	except Exception as e:
		logger.error('under student.view.certificates '+str(e.args)+' UID-'+str(request.user.id))
	return render(request, 'student/certificates.html', data)
