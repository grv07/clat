from django.shortcuts import render, redirect
from course_mang.models import CourseDetail, CourseVideos
import user_actions
from CLAT.cities import cities
from .tasks import send_mail
from django.views.decorators.csrf import csrf_exempt
import json
from django import template
from django.http import HttpResponse, HttpResponseRedirect
from CLAT.services import pagination, otp_engine, constants
from django.template import Context, loader
from django.contrib import messages
from django.template.loader import get_template
from teacher.models import Teacher
from student.models import Student
from django.contrib.auth.models import User
from CLAT.services import course_service
from CLAT.updations import update_pre_enroll_users_db
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from course_mang.utilities import student_required, check_password, CONTACT_US, PASSWORD_RESET, ASK_QUERY, verify_account
from .form import ContactForm, QueryForm
from .models import Badges

import logging
logger = logging.getLogger(__name__)
from qna_api.user_manager import register_user

def update(request):
	update_pre_enroll_users_db.update_for_enroll_users()
	return ' /.........Done'

def badges(request):
	if request.method == 'GET':
		all_badges = Badges.objects.filter(min_percentage__lte=request.GET.get('percentage'))
		data = []
		if all_badges:
			for badges in all_badges:
				data.append({'id':badges.id, 'name':badges.badge_name, 'color':badges.badge_color})
		return HttpResponse(json.dumps(data), content_type="application/json")

''' Handle paginate ajax call for Courses '''
def paginate_action(request):
	logger.info('under paginate_action view')
	t = get_template('course_mang/course_list.html')
	course_list = CourseDetail.objects.all()
	course_list = pagination.get_paginated_list(obj_list = course_list, page = request.GET.get('page'))
	html = t.render(Context({'course_list': course_list,'request':request}))
	return HttpResponse(json.dumps({'html':html}), content_type="application/json")

'''Landing Page'''
def home(request):
	course_list= []
	# send_mail.delay('jo choka udte hue', 'grvtyagi22@gmail.com', subject = 'Clat contact message')
	if not request.user.is_authenticated:
		course_list = CourseDetail.objects.filter(can_enroll=True)
	else:
		try:
			if request.user.student:
				course_list = CourseDetail.objects.filter(can_enroll=True)
		except Exception as e:
			logger.error('under user_login.view.home '+str(e.args))
			course_list = CourseDetail.objects.filter(can_enroll=True)
	course_list = pagination.get_paginated_list(obj_list = course_list, page = request.GET.get('page'))
	return render(request, 'new_home.html', {'course_list': course_list})


@csrf_exempt
def file_view(request):
	import io
	import os
	return render(request, 'test.html')

def user_login_form(request):
	data = {}
	try:
		logger.info('under user_login_form view')
		course_list = CourseDetail.objects.all()
		course_list = pagination.get_paginated_list(obj_list = course_list, page = request.GET.get('page'))
		next = request.GET.get('next')
		data = {'next': request.GET.get('next'),'course_list': course_list }
		if next:
		   data['login_error'] = True 
		   messages.info(request,'Please login first')
	except Exception as e:
		logger.error('under user_login.view.user_login_form '+str(e.args))
	return render(request,'new_home.html',data)


def user_login_action(request):
	if request.method == 'POST':
		return user_actions.login_user(request)
	else:
		return user_login_form(request)


def user_logout(request):
	return user_actions.logout_user(request)

def user_otp_verification(request):
	if request.method == 'POST':
		from user_login.form import OTPVerify_code_Form        
		otp_code_form = OTPVerify_code_Form(data = request.POST)
		if otp_code_form.is_valid():
			logger.info('Under user_login.view.user_otp_verification otp-form valid')
			otp_code = request.POST.get('otp_code',None)
			student = None
			if otp_code:
				logger.info('Under user_login.view.user_otp_verification otp-code is not None')
				try:
				   student = Student.objects.get(otp_code = otp_code)
				   if verify_account(student):
					  messages.success(request,'Your account Successfully verified. Please login.')
					  logger.info('Under user_login.view.user_otp_verification OTP verification successful.')
					  return redirect('/home/')
				   else:
					  messages.info(request,'This user is verified.') 
					  return redirect('/home/')   
				except Exception as e:
					logger.error('under user_login.view.user_otp_verification '+str(e.args))
					messages.info(request,'This user not registered with us.') 
					return redirect('/home/')
		else:
			logger.error('under user_login.view.user_otp_verification '+str(otp_code_form.errors))
			messages.info(request,'OTP code not valid.')
			return render(request,'acc_verification.html',{'form':otp_code_form})
	else:
		return render(request,'acc_verification.html')

def account_verification_msg(request):
	return render(request, 'acc_verification.html')


'''Use to return a FAQ page '''
def faq_page(request):
	return render(request,'faq.html')


'''Use to return a Privacy Policy page '''
def privacy_policy(request):
	return render(request,'privacy_policy.html')


'''Use to return a Contact page '''
def contact(request):
	# logger.info('under contact view'
	data = {}
	# print request.POST
	if request.method == 'POST':
		try:
			contact_form = ContactForm(request.POST)
			if contact_form.is_valid():
				from course_mang import utilities
				contact = contact_form.save(commit=False)
				contact.fullname = request.POST.get('fullname', None)
				contact.email = request.POST.get('email', None)
				contact.inquirytype = request.POST.get('inquirytype', None)
				contact.phone = request.POST.get('phone', None)
				contact.iama = request.POST.get('iama', None)
				contact.message = request.POST.get('message', None)
				contact.save()

				msg = CONTACT_US.format(str(request.POST.get('fullname', None)).capitalize(), request.POST.get('inquirytype', None), request.POST.get('iama', None), request.POST.get('phone', None), request.POST.get('email', None), request.POST.get('message', None))
				send_mail(msg, 'grvtyagi22@gmail.com', subject = 'Clat contact message')
				messages.info(request, 'We have received your inquiry message. We will get back to you shortly.')
			else:
				logger.info('Under user_login.view.contact '+str(contact_form.errors))
				data['errors'] = contact_form.errors
		except Exception as e:
			logger.error('Under user_login.view.contact '+str(e.args))	
			messages.error(request, 'Unable to contact right now.May be a server fault.')
	return render(request, 'contact_page.html', data)



'''Have questions functionslity ......'''
def have_question(request, course_uuid):
	course = CourseDetail.objects.get(course_uuid = course_uuid)
	# print request.POST
	if request.method == 'GET':
		return render(request, 'have_question.html', {'course':course})
	else:
		query_form = QueryForm(request.POST)
		if query_form.is_valid():
			logger.info('user_login.have_question form is valid.')
			query = query_form.save()

			html = ASK_QUERY.format(username = query.username, course_name = request.POST.get('course_name', None), iama = query.iama,
				module_name = query.module_name, user_email = query.user_email, message = query.message)
			
			send_mail(html, 'gaurav@madmachines.io', subject = 'Clat query')
			messages.success(request, 'Your query send successfully.')
			return render(request, 'have_question.html', {'course':course})
		else:
			logger.error('user_login.have_question form is not valid '+str(query_form.errors))
			return render(request,'have_question.html', {'form' : query_form, 'course':course})

def get_cities(request):
	state=request.GET['state']
	logger.info('under user_login.view.get_cities')
	return HttpResponse(json.dumps(cities[state]), content_type="application/json")
 
'''This method call otp_engine method for send  a message to current user'''
def send_otp_code(request):
	if request.method == 'POST':
		from user_login.form import OTPVerify_mob_Form
		otp_code = otp_engine.id_generator()
		otp_mob_no_form = OTPVerify_mob_Form(data = request.POST)
		if otp_mob_no_form.is_valid():
			logger.info('under user_login.view.send_otp_code otp_mob_no_form is valid.')
			try:
			  student = Student.objects.get(phone_number = request.POST.get('user_phone', None))
			  student.otp_code = otp_code
			  student.save()
			  msg = "Hello {0}, One Time Password (OTP) for your e-Quest account verification is {1}. Welcome to India's first e-quality platform.".format(request.user.username,str(student.otp_code))
			  status = otp_engine.send_otp_msg(student,msg)
			  messages.info(request,status['msg'])
			  return render(request, 'acc_verification.html', {'is_otp_send_success' : status['status']})
			except Exception as e:
				logger.error('under user_login.view.send_otp_code '+str(e.args))
				messages.error(request,'Unable to find the user.')
				return render(request,'acc_verification.html')
								
		else:
			logger.info('under user_login.view.send_otp_code otp_mob_no_form is not valid '+str(otp_mob_no_form.errors))
			return render(request,'acc_verification.html', {'form' : otp_mob_no_form})
	else:
		return render(request,'acc_verification.html')


"""
Standard 404 error page
"""
def error404(request):
	template = loader.get_template('error_404.html')
	context = Context({
		'message': 'All: %s' % request,
		})
	return HttpResponse(content=template.render(context), content_type='text/html; charset=utf-8', status=404)

'''About Page'''
def about_page(request):
	return render(request,'about.html')

'''Term and Services'''
def terms_and_services(request):
	return render(request,'terms_services.html')     


'''Certification policy'''
def certification_policy(request):
	return render(request,'certification_policy.html')
"""
Standard 500 error page
"""
def error500(request):
	template = loader.get_template('error_500.html')
	context = Context({
		'message': 'All: %s' % request,
		})
	return HttpResponse(content=template.render(context), content_type='text/html; charset=utf-8', status=500)



"""
Function for rescuing password and username
"""
def rescue_credentials(request,_type):
	if request.user.is_authenticated():
		messages.info(request,'First logout and then try to rescue password.')
		return HttpResponseRedirect('/')
	if request.method == 'POST':
		user_obj = None
		_user = None
		option = request.POST['option']
		email = request.POST.get('email')
		phone_number = request.POST.get('phone_number')
		try:
			if _type == constants.PASSWORD_VERIFY_USES[0]:
				logger.info('under user_login.view.rescue_credentials student password')
				if option == constants.PASSWORD_VERIFY_OPTIONS[0]:
					user_obj = User.objects.get(email = email)
					_user = user_obj.student_profile
				if option == constants.PASSWORD_VERIFY_OPTIONS[1]:
					student_obj = Student.objects.get(phone_number = phone_number)
					user_obj = student_obj.student
					_user = student_obj
				username = user_obj.username
			if _type == constants.PASSWORD_VERIFY_USES[1]:
				if option == constants.PASSWORD_VERIFY_OPTIONS[0]:
					_user = Teacher.objects.get(email = email)
				if option == constants.PASSWORD_VERIFY_OPTIONS[1]:
					_user = Teacher.objects.get(phone_number = phone_number)
				user_obj = _user
				username = _user.username
		except ObjectDoesNotExist as e:
			logger.error('under user_login.view.rescue_credentials '+str(e.args))
			if option == constants.PASSWORD_VERIFY_OPTIONS[0]:
				messages.error(request,'This e-mail is not registered with e-QUEST.')
			if option == constants.PASSWORD_VERIFY_OPTIONS[1]:
				messages.error(request,'This phone number is not registered with e-QUEST.')
			return render(request, 'rescue.html')

		if _user:
			logger.info('under user_login.view.rescue_credentials password recovery link generated.')
			complete_link = "http://" + str(request.META['HTTP_HOST']) + "/account/reset/password/" + str(_user.uuid_key) + "/"+_type+"/"
			html = PASSWORD_RESET.format(link = complete_link, username = str(username))
			send_mail(html, user_obj.email, 'Password Reset Request')
			messages.info(request, 'An email has been sent to '+str(user_obj.email)+'. Please reset your password using the link in the email.')
		else:
			logger.info('under user_login.view.rescue_credentials password recovery link not generated.')
			if option == constants.PASSWORD_VERIFY_OPTIONS[0]:
				messages.error(request, 'This e-mail is not registered with e-QUEST.')
			elif option == constants.PASSWORD_VERIFY_OPTIONS[1]:
				messages.error(request, 'This phone number is not registered with e-QUEST.')

	return render(request, 'rescue.html')



"""
Change the password
"""
def change_password(request,_uuid,_type):
	if request.user.is_authenticated():
		messages.info(request,'First logout and then try to rescue password.')
		return HttpResponseRedirect('/')
	if _type != constants.PASSWORD_VERIFY_USES[1] and _type != constants.PASSWORD_VERIFY_USES[0]:
		logger.info('under user_login.view.change_password invalid URL.')
		return HttpResponse('Invalid requests : Suspicious URL!!!')
	if request.method == 'POST':
		if _type != constants.PASSWORD_VERIFY_USES[1] and _type != constants.PASSWORD_VERIFY_USES[0]:
			logger.info('under user_login.view.change_password invalid URL.')
			return HttpResponse('Invalid requests : Suspicious URL!!!')
		else:
			new_password = request.POST['new_password']
			confirm_password = request.POST['confirm_password']
			if new_password == confirm_password:
				if check_password(new_password):
					try:
						import uuid
						if _type == constants.PASSWORD_VERIFY_USES[1]:
							logger.info('under user_login.view.change_password student password.')
							user_object = Teacher.objects.get(uuid_key = _uuid)
							user_object.set_password(confirm_password)
							user_object.uuid_key = uuid.uuid4()
						if _type == constants.PASSWORD_VERIFY_USES[0]:
							student_obj = Student.objects.get(uuid_key = _uuid)
							user_object = User.objects.get(id = student_obj.student.id)
							user_object.set_password(confirm_password)
							student_obj.uuid_key = 'eq' + str(uuid.uuid4().fields[-1])[:8]
							student_obj.save()
						user_object.save()
						messages.success(request,'Password changed succesfully.')
					except Exception as e:
						logger.error('under user_login.view.change_password '+str(e.args))
						messages.error(request,'Password cannot be reset. The reset link has expired.')
					return HttpResponseRedirect('/')
				else:
					messages.error(request,"Password must contain A-Z,a-z,0-9 & any of the special characters @#$%^&+=")
			else:
				messages.error(request,"Error! Both passwords do not match. Make sure they match. Try again.")
	return render(request,'password_reset.html')

def clear_session(request):
	del request.session['not_verify']
	del request.session['otp_send']
	del request.session['phone_number']
	logger.info('under user_login.view.clear_session completed.')
	return redirect(request.GET.get('next', '/home/'))
