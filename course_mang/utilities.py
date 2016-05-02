from __future__ import division
import os, sys, uuid, re
from django.contrib.auth.models import User
try:
	from CLAT.local_settings import RESTRICT_MODULE_TIME
except ImportError as e:
	from CLAT.prod_settings import RESTRICT_MODULE_TIME

from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist

from user_login.tasks import send_mail
from student.models import Student
from CLAT.settings import LOGIN_REDIRECT_URL
from student.models import EnrolledCourses
from allauth.socialaccount.models import SocialAccount
from payment.models import CoursePayment
from assesment_engine.models import AssesmentRegisterdUser, UserResult
# from com.mettl.api.schedule.ScheduleInfo import ScheduleInfo

# Set the path for the Mettl API SDK
app_folder = os.path.abspath(os.path.join(os.path.dirname(__file__) , "../"))
sys.path.insert(0,app_folder + "/mettl-api-sdk/src")

# Setting path is necessary above for below statements to be valid
#from com.mettl.api.results.Results import Results
from CLAT.settings import SITE_NAME

import logging
logger = logging.getLogger(__name__)



CLAT_LOGO_HTML = '<a href="http://Clat.co/" target="_blank"><img src="http://Clat.co/static/images/logo.png" alt="Clat logo image not available"></a><br><br>'

CLAT_HELP_HTML = '<p>In case you have any issues please mail us at talktous@Clat.co.in.</p><p>Warm Regards<br>Team Clat</p>'

ADDED_VIDEO_MAIL_HTML = CLAT_LOGO_HTML + '<h3>A new video has been added under module name {module_name} of course <span style="color:blue;font-size:20px;">{course_name}</span>.</h3>\
					  <h3><a href="{complete_link}">Click here</a> to view it.</h3><br><hr>\
					  <h3>Module details :</h3>\
					  <h4>{week_detail}</h4><br>'
					  
TEST_FINISH_MAIL_HTML = CLAT_LOGO_HTML + '<h2>Dear <span style = "color: blue;">{full_name}</span> ,</h2><p></p><h3>Welcome to Clat ( India\'s first Intelligent e-Quality Learning Management System ).</h3>\
				<p><hr></p><h3>You just finished your test name <span style = "color: blue;">{module_name}</span>. You have {status} the test.</h3>\
				<h3>You scored {scored} out of {total} ( percentage = {percentage}% ).  {msg}</h3>\
				<h3>Please visit this url for view/download your test result.\
				<a href="{pdf_link}" style= "-webkit-appearance: button;-moz-appearance: button;appearance: button;text-decoration: none;color: blue;">Click Here</a></h3>\
				<h3 style="color:red;">NOTE    :    In case if our button link is not working, please copy and paste following link in browser URL</h3><br><a href="{pdf_link}">{pdf_link}</a>\
				'

CERTIFICATE_MAIL_HTML = CLAT_LOGO_HTML + '<p>Hi<br><p>Reference your Registration with us for the {course} Course .<br> As per our records we find that you have<br>\
completed the course and have taken all the required assessments and exam for becoming eligible for the "Participation Certificate".</p>\
<p>Please go the following lick to receive your certificate {link}> .<br>A certificate carries a Certificate ID which can be used by you or your employer to verify the authenticity of the certificate achieved.<br>Further in case you have scored overall more than 75% marks then you are eligible to go for the "Professional Certificate" for which you will have a take an Onsite Proctored test at any of the \
certified QCI centres.<br>Some courses may require you to attend an onsite Workshop as well.</p><p>All the details for the Professional Certificate will be published on the Clat Portal.<br>Please keep in touch .</p>'+ CLAT_HELP_HTML +'</p>'

LOGIN_REMINDER = CLAT_LOGO_HTML + '<p>Hi<br><p>Reference your Registration with us for the {courses} Course(s) .<br>We find from our records that you have not logged into your account for the last {days} days , hence we are sending this Gentle Reminder  for \
				completing the course(s).</p>'+ CLAT_HELP_HTML +'</p>'


CONTACT_US = CLAT_LOGO_HTML + '<p style="color:black">FULL NAME: <span style="color:blue;">{0}</span><br><p style="color:black">INQUIRY TYPE: <span style="color:blue;">{1}</span></p><br><p style="color:black">PROFESSION: <span style="color:blue;">{2}</span></p><br>\
								<p style="color:black">CONTACT NUMBER: <span style="color:blue;">{3}</span></p><br><p style="color:black">FROM: <span style="color:blue;">{4}</span>,<br><br>MESSAGE: <br>{5}<br><br>Thank you.<p>'

ASK_QUERY = CLAT_LOGO_HTML + '<p style="color:black">FULL NAME: <span style="color:blue;">{username}</span><br><p style="color:black">COURSE NAME: <span style="color:blue;">{course_name}</span></p><p style="color:black">PROFESSION: <span style="color:blue;">{iama}</span></p>\
								<p style="color:black">MODULE NAME: <span style="color:blue;">{module_name}</span></p><p style="color:black">FROM: <span style="color:blue;">{user_email}</span>,<br><br>MESSAGE: <br><span style="color:blue">{message}</span><br><br>Thank you.<p>'

DEACTIVATE_REMINDER = CLAT_LOGO_HTML + '<p style="color:black">Dear <span style="color:blue;">%s</span>,<br><br>Thanks for using Clat ( India\'s first Intelligent e-Quality Learning Management System ).<br>We have observed that you have not logged-in for past 3 weeks.\
				Your account will be deactivated and you will be unable to view your enrolled courses.Please login frequently to view new courses and enrolled ones.<br>Thank you.<p>'


NO_ACTION_AFTER_REGISTRATION_REMINDER = CLAT_LOGO_HTML + '<p style="color:black">Dear <span style="color:blue;">{fullname}</span>,<br><br>Thanks for registering on Clat ( India\'s first Intelligent e-Quality Learning Management System ).<br>We have observed that you have not logged-in after completing registration.\
				<br>Please login frequently to keep up with the resources.<br> In case you have not verified yourself , <a href="{link}">click on this link</a> to verify yourself and get started.<br>Thank you.<p>'

COURSE_TIME_ABOUT_TO_OVER_MAIL_HTML = CLAT_LOGO_HTML + '<p>Hi<br><p>Reference your Registration with us for the {course} Course .<br>We find from our records that you have not logged into your account for the last {login_days} days. You have now less than 50% of the time remaining to\
			complete the course mentioned, hence we are sending this Gentle Reminder for completing the course.</p>'+ CLAT_HELP_HTML +'</p>'

COURSE_TIME_OVER_MAIL_HTML = CLAT_LOGO_HTML + '<p>Hi<br><p>Reference your Registration with us for the {course} Course .<br>Reference your Registration with us for the <XXXXX> Course .<br> We find from our records that you have not completed the course within the specified time hence we are sending this Gentle Reminder for\
			completing the course.<br> As per Clat policy you will now have to register again to take the course.</p>'+ CLAT_HELP_HTML +'</p>'

PASSWORD_RESET = CLAT_LOGO_HTML + '<p>Hi<br><p>Someone requested that the password be reset for the following account of\
				Clat :</p><p>Username: {username}</p><p>If this was a mistake, just ignore this email and nothing will happen.<br>To\
				reset your password, visit the following address:</p><p>{link}</p>'+ CLAT_HELP_HTML +'<p>'

PROFESSIONAL_CERTIFICATE_HTML = CLAT_LOGO_HTML + '<p>Hi<br><p>Reference your Registration with us for the {course} Course.</p>' +  CLAT_HELP_HTML + '</p>'

TRANSACTION_FAILURE_HTML = CLAT_LOGO_HTML + '<p>Hi<br><p>Your transaction for course <b>{course}</b> has been declined due to a server error.Please mail this issue with your transaction ID <b>({txnid})</b> to our support team at <a href="mailto:equestsupport@qcin.org?Subject=Transaction Server Error">equestsupport@qcin.org</a> .</p>'


"""
decorator for checking if the logged in user is a admin or not
If yes, then allow him/her. Otherwise, redirect to error page.
"""
def admin_required(function=None, redirect_url_=None):
		if redirect_url_ == None:
				
				redirect_url_ = LOGIN_REDIRECT_URL
		def wrapper(request, *args, **kwargs):
				try:
						if request.user.is_superuser:
								return function(request, *args, **kwargs)
						else:
							return redirect(request.POST.get('next',redirect_url_))
				except ObjectDoesNotExist as e:
						return redirect(request.POST.get('next',redirect_url_))
		return wrapper


"""
decorator for checking if the logged in user is a teacher or not
If yes, then allow him/her. Otherwise, redirect to error page.
"""
def teacher_required(function=None, redirect_url_=None):

		if redirect_url_ == None:
				redirect_url_ = LOGIN_REDIRECT_URL
		def wrapper(request, *args, **kwargs):
				try:
						if request.user.teacher:
								return function(request, *args, **kwargs)
				except ObjectDoesNotExist as e:
						return redirect(request.POST.get('next',redirect_url_))
		return wrapper


"""
decorator for checking if the logged in user is a student or not
If yes, then allow him/her. Otherwise, redirect to error page.
"""
def student_required(function=None, redirect_url_=None):
		# print 'Name of function that is call this decorator '+str(function.__name__)

		if redirect_url_ == None:
				redirect_url_ = LOGIN_REDIRECT_URL

		def wrapper(request, *args, **kwargs):
				if Student.objects.filter(student=request.user.id) or SocialAccount.objects.filter(user=request.user.id):
						return function(request, *args, **kwargs)
				else:                        
					if function.__name__ == 'assessment_register_student':
							from django.contrib import messages
							messages.info(request,'Only a student can register and take a test.')
					return redirect(request.POST.get('next',redirect_url_))
		return wrapper



def verify_account(student):
    if not student.is_verified:
        student.is_verified = True
        student.uuid_key = 'eq' + str(uuid.uuid4().fields[-1])[:8]
        student.save()
        return True
    else:
        return False        

    

def get_student_from_user(user):
    try:
        student = Student.objects.get(student=user.id)
        if student:
            return student
        else:
            return None
    except Exception as e:
        print e.args
        return None

''' Check if user is verified or not '''
def is_verified_user(user):
    try:
        student = get_student_from_user(user)
        if student:
            return student.is_verified
        else:
            return False
    except Exception as e:
        print e.args
        return None

'''Call when user want to send verification mail '''
def verfiy_acc_mail():
    pass


'''Call when user want to send verification mail by default its a welcome mail to user if << msg is None >>'''
def verification_mail(user, domain, msg = None, **kwargs):
    # print kwargs 
    student = User.objects.get(id=user)
    if student:
        complete_link = "http://" + str(domain) + "/account/verification/" + str(kwargs['uuid_key'])
        # print complete_link
        if not msg:
            # msg = '<p>Please verify your e-quest account <a href="' + complete_link + '"\
            #  style= "-webkit-appearance: button;-moz-appearance: button;appearance: button;text-decoration: none;color: blue;">Click Here</a> </p>\
            #   </br><p>Your login user name is: <span style="color:red">'+kwargs['student_uname']+'</span></p></br>\
            #   <p>Your password is:  <span style="color:red">'+kwargs['student_pass']+'</span>\
            #   <p>Your account phone number is:  <span style="color:red">'+kwargs['phone_number']+'</span>\
            #   <b>In case if our button link not work please copy and paste in browser tab :<br>'+complete_link+'</b>\
            #   </p>'
            msg = '<img src="http://Clat.co/static/images/logo.png" alt="Clat logo image not available"><br><br>\
                    <h2>Dear '+ str(kwargs['full_name']).capitalize() +',</h2><p></p><h3>Welcome to Clat ( India\'s first Intelligent e-Quality Learning Management System ).</h3>\
                    <p><hr></p><h3>Your account details are as follows</h3>\
                    <div style="text-align:left;"><h4>Username    :    <span style="color:blue;">'+kwargs['student_uname'] +'</span></h4>\
                    <h4>Password    :    <span style="color:blue;">'+ kwargs['student_pass'] +'</span></h4>\
                    <h4>Contact Number    :    <span style="color:blue;">'+  kwargs['phone_number'] +'</span></h4></div><hr>\
                    <h3>Please visit this url to activate your account\
                    <a href="' + complete_link + '"style= "-webkit-appearance: button;-moz-appearance: button;appearance: button;text-decoration: none;color: blue;">Click Here</a></h3>\
                    <h3 style="color:red;">NOTE    :    In case if our button link is not working, please copy and paste following link in browser URL</h3>\
                    <p>'+ complete_link +'</p>'
        send_mail(msg, student.email)
    else:
        pass


def is_enrolled(user, course):
	try:
		if EnrolledCourses.objects.is_student_enrolled(user, course):
			return [True, EnrolledCourses.objects.get(course=course, user=user)]
		return [False,None]
	except Exception as e:
		print e.args
		return [False, None]


"""
Get the test status and then fetch all test results if test is completed.
"""
def fetch_results(schedule_key, user_email):
		public  = "4a9bbe63-b533-49de-b1bb-9f6adcc38dc5"
		private = "66ba7de5-4bff-4ba9-88a4-12b7d8d568f9"
		is_prod = True
		
		result = Results(public, private, is_prod)
		result_params = {}
		json_output = result.getResultForCandidateInSchedule(schedule_key,user_email,result_params)
		testStatus = json_output['testStatus']
		if testStatus['completionMode'] == 'Completed':
				return testStatus
		return {}

"""
Check whether quiz URL is of METTL
"""
def check_quiz_link(quiz_key):
		if re.match(r'[a-zA-Z0-9]{8,22}',quiz_key):
				return True
		return False


'''
Use for get progress time of in %
'''
def check_progress_time(progress_time):
	data =  round(float((float(progress_time/60)*100/RESTRICT_MODULE_TIME)))
	if data >= 100:
		data = 100
	return data


def get_schedule_details(schedule_key):
	public  = "4a9bbe63-b533-49de-b1bb-9f6adcc38dc5"
	private = "66ba7de5-4bff-4ba9-88a4-12b7d8d568f9"
	is_prod = True
	schedule_info  = ScheduleInfo(public , private, is_prod)
	return schedule_info.getScheduleDetails(schedule_key, {})


def edit_schedule_info(schedule_key):
	from com.mettl.api.schedule.EditScheduleInfo import EditScheduleInfo
        print SITE_NAME	
	import requests
	import json
	public  = "4a9bbe63-b533-49de-b1bb-9f6adcc38dc5"
	private = "66ba7de5-4bff-4ba9-88a4-12b7d8d568f9"
	is_prod = True
	
	# api.mettl.com/v1/schedules/{access-key}
	schedule_details = get_schedule_details(schedule_key)
	response = json.loads(schedule_details)
	if response['status'] == 'SUCCESS':
		_schedule =  response['schedule']
		sc = {
				"assessmentId": _schedule['assessmentDetails']['id'],    
				"name": _schedule['name'],
				"imageProctoring": False,
				"webProctoring": {
				"enabled": False
				},
				"scheduleType": "AlwaysOn",
				"scheduleWindow": None,
				"access": {
				"type": "OpenForAll",
				"candidates": None,
				"sendEmail": False
				},
				"ipAccessRestriction": {
				"enabled": False
				},
				"allowCopyPaste": True,
				"exitRedirectionUrl": ""+str(SITE_NAME),
				"showResultsOnTestCompletion": False,
				"sourceApp": "Clat",
				"testStartNotificationUrl": str(SITE_NAME)+"/start/asm_notification/",
				"testFinishNotificationUrl": str(SITE_NAME)+"/finish/asm_notification/",
				"testGradedNotificationUrl": str(SITE_NAME)+"/grade/asm_notification/",
			}
			
		schedule_info = EditScheduleInfo(public, private, is_prod)
		url = schedule_info.editScheduleForAssessment(schedule_key, params = sc)
		
		headers = {'content-type': 'application/json'}

		response = requests.post(url, headers = headers)
		schedule_end_redirect_url_changes = json.loads(response.content)
		print schedule_end_redirect_url_changes
		if schedule_end_redirect_url_changes['status'] == 'SUCCESS':
			return True
		else:
			return False
	else:
		return False

def rescue_user_result(schedule_key,user_email):
	'''
		{u'status': u'Completed', u'htmlReport': 
		u'https://mettl.com/corporate/analytics/share-report?key=XnU0GWfoi%2FivwsPYvNqm%2FQ%3D%3D', 
		u'result': {u'totalCorrectAnswers': 16.0, 
			u'totalQuestion': 31.0, u'totalMarks': 16.0, u'attemptTime': 206.0,
			 u'sectionMarks': [{u'skillMarks': 
			 [{u'totalCorrectAnswers': 8.0, u'skillName': u'Measuring level of performance', 
			 u'totalMarks': 8.0, u'totalQuestion': 13.0, 
			 u'timeTaken': 122.0, u'totalUnAnswered': 3.0, u'maxMarks': 13.0, u'questions': None},
			  {u'totalCorrectAnswers': 0.0, u'skillName': u'Measuring level of performance', u'totalMarks': 0.0,
			   u'totalQuestion': 4.0, u'timeTaken': 0.0, u'totalUnAnswered': 4.0, u'maxMarks': 4.0, u'questions': None}],
			   u'totalCorrectAnswers': 8.0, u'sectionName': u'Section #1', u'totalMarks': 8.0,
			    u'totalQuestion': 17.0, u'timeTaken': 0.0, u'totalUnAnswered': 7.0, u'maxMarks': 17.0}, 
			    {u'skillMarks': [{u'totalCorrectAnswers': 8.0, u'skillName': u'Measuring level of performance', 
			    u'totalMarks': 8.0, u'totalQuestion': 14.0, u'timeTaken': 84.0, u'totalUnAnswered': 6.0, u'maxMarks': 14.0,
			     u'questions': None}], u'totalCorrectAnswers': 8.0, u'sectionName': u'Section #2',
			      u'totalMarks': 8.0, u'totalQuestion': 14.0, u'timeTaken': 0.0, 
			      u'totalUnAnswered': 6.0, u'maxMarks': 14.0}], u'analysis': None, 
			      u'totalUnAnswered': 13.0, u'percentile': 75.0, u'maxMarks': 31.0}, 
			      u'startTime': u'Fri, 15 Jan 2016 07:14:51 GMT', 
			      u'completionMode': u'Completed', 
			      u'endTime': u'Fri, 15 Jan 2016 07:18:18 GMT', 
			      u'pdfReport': 
	u'https://mettl.com/corporate/analytics/downloadPdfReport?key=XnU0GWfoi
	%2FivwsPYvNqm%2FQ%3D%3D&fname=anshul&aname=Clinical+Audit+Measuring+level+of+performance'}

	'''
	try:
		edit_schedule_info(schedule_key)
		test_result_status = fetch_results(schedule_key, user_email)
		if test_result_status['status'] == 'Completed':
			marks_scored = test_result_status['result']['totalMarks']
			max_marks = test_result_status['result']['maxMarks']
			percentile = test_result_status['result']['percentile']
			finish_mode = 'By rescue algo'
			
			print marks_scored,max_marks,percentile,finish_mode

			assessment_register_student = AssesmentRegisterdUser.objects.get(student_email = user_email, schedule_key = schedule_key)
			if assessment_register_student:
				UserResult.objects.create(assesmentRegisterdUser = assessment_register_student, percentile = percentile,
					max_marks = max_marks, marks_scored = marks_scored, finish_mode = finish_mode)
				percentage = marks_scored/max_marks
				if percentage < 0.75:
					assessment_register_student.result_status = 'FAIL'
				else:
					assessment_register_student.result_status = 'PASS'
				assessment_register_student.test_status = 'GRADED'
				assessment_register_student.save()	

	except Exception as e:
		print e.args
		logger.error('rescue_user_result  ERROR ::: >>>>>>>>>>>>>'+str(e.args))			

def create_users_xls(users_enroll_course, _sm_course_name, course_name):
	# Course name is small form if large then 20 char.
	import xlwt
	import ast
	try:
		style0 = xlwt.easyxf('font: name Times New Roman,height 270,color-index red, bold on',
			num_format_str='#,##0.00')
		style2 = xlwt.easyxf('font: name Times New Roman,,height 240, color-index blue, bold on',
			num_format_str='#,##0.00')
		style1 = xlwt.easyxf(num_format_str='D-MMM-YY')
		wb = xlwt.Workbook()
		ws = wb.add_sheet(_sm_course_name)
		
		ws.col(0).width = (len('Course: '+_sm_course_name)*367)
		ws.row(0).height_mismatch = True
		ws.row(0).height = 20*20

		ws.row(1).height_mismatch = True
		ws.row(1).height = 20*20
		ws.col(1).width = len('example@example.example')*367
		
		ws.row(2).height_mismatch = True
		ws.row(2).height = 20*20
		ws.col(2).width = len('example@example.example')*367

		ws.row(3).height_mismatch = True
		ws.row(3).height = 20*20
		ws.col(3).width = len('example@example.example')*234

		ws.row(4).height_mismatch = True
		ws.row(4).height = 20*20
		ws.col(4).width = len('example@example')*234

		ws.row(5).height_mismatch = True
		ws.row(5).height = 20*20
		ws.col(5).width = len('example@example.example')*250
		
		ws.row(6).height_mismatch = True
		ws.row(6).height = 20*20
		ws.col(6).width = len('example@example.example')*234

		ws.row(7).height_mismatch = True
		ws.row(7).height = 20*20
		ws.col(7).width = len('example@example.example')*234

		ws.row(8).height_mismatch = True
		ws.row(8).height = 20*20
		ws.col(8).width = len('example@example.example')*234

		ws.write(0, 0, 'Course: '+course_name, style0)
		ws.write(1, 0, 'User Name', style2)
		ws.write(1, 1, 'E-Mail', style2)
		ws.write(1, 2, 'Txn.Id', style2)
		ws.write(1, 3, 'Amount', style2)
		ws.write(1, 4, 'Status', style2)
		ws.write(1, 5, 'Name On Card', style2)
		ws.write(1, 6, 'PG TYPE', style2)
		ws.write(1, 7, 'Mode', style2)
		ws.write(1, 8, 'Added Date', style2)
		
		for i,enr_course in enumerate(users_enroll_course):
			_payment_extra_data = {}
			
			try:
				_payment_extra_data = ast.literal_eval(CoursePayment.objects.get(enrolledcourse = enr_course).extra_data)
			except Exception as e:
				logger.error('course_mang.utility.create_users_xls  ERROR ::: >>>>>>>>>>>>>'+str(e.args))

			ws.write(i+2, 0, enr_course.user.username)
			ws.write(i+2, 1, enr_course.user.email)
			ws.write(i+2, 2, _payment_extra_data.get('txnid', 'Not Avail'))
			ws.write(i+2, 3, _payment_extra_data.get('amount', 'Not Avail'))
			ws.write(i+2, 4, _payment_extra_data.get('status', 'Not Avail'))
			ws.write(i+2, 5, _payment_extra_data.get('name_on_card', 'Not Avail'))
			ws.write(i+2, 6, _payment_extra_data.get('PG_TYPE', 'Not Avail'))
			ws.write(i+2, 7, _payment_extra_data.get('mode', 'Not Avail'))
			ws.write(i+2, 8, _payment_extra_data.get('addedon', 'Not Avail'))

		file_dir_path = 'xls/'+_sm_course_name
		
		if not os.path.exists(file_dir_path):
				os.makedirs(file_dir_path)	
		wb.save(file_dir_path+'/enrolled_user.xls')

		return True
	except Exception as e:
		logger.error('create_users_xls error >> '+str(e.args))
		return False
			


def check_password(value):
	pattern = "^(?=.*?[a-zA-Z])(?=.*?[0-9])(?=.*?[@#&^%!*%$])[a-zA-Z0-9@#&^%!*%$]{8,20}$"
	if not re.findall(pattern, str(value)):
		return False
	return True


def check_payment(txnid):
	status = None
	from payu.utils import verify_payment
	from payu.models import Transaction
	result = verify_payment(txnid)
	try:	
		if result['status'] == 1:
			txn_data = result['transaction_details'][str(txnid)]
			if float(txn_data['net_amount_debit']) <= float(0.0) and txn_data['unmappedstatus'] == 'failed' and txn_data['status'] == 'failure':
				status = False
			elif float(txn_data['net_amount_debit']) > float(0.0) and txn_data['unmappedstatus'] == 'captured' and txn_data['status'] == 'success':
				status = True
		else:
			status = False
		student_id = Transaction.objects.get(transaction_id=txnid).user
		student = User.objects.get(pk = student_id)
		# print student.email
		result['user'] = { 'user_id' : student_id, 'user_email' : student.email }
		# print result
	except Exception as e:
		print e.args
		logger.error('payment.check_payment >>  '+str(e.args)+' '+txnid)
	return (status,result,)
