# Create your views here.
import os
import sys
import json  
from django.shortcuts import HttpResponseRedirect, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from assesment_engine.models import AssesmentRegisterdUser,UserResult, TestMarks, TestStatus, Result, SectionMarks
from assesment_engine import assesment_db_handling
from course_mang.utilities import student_required, edit_schedule_info, TEST_FINISH_MAIL_HTML, CERTIFICATE_MAIL_HTML, PROFESSIONAL_CERTIFICATE_HTML
from course_mang.models import CourseDetail, CourseWeek
from django.views.decorators.csrf import csrf_exempt
from CLAT.services.constants import METTL_CONFIG, PROGRESS_STATUSES, TEST_CHECK_FOR, TEST_STATUS
from user_login.tasks import send_mail
from student.models import EnrolledCourses, UserCourseProgress
from course_test_handling.models import Tests
from django.contrib.auth.models import User
from CLAT.settings import SITE_NAME
from qna_api.user_manager import register_user

# app_folder = os.path.abspath(os.path.join(os.path.dirname(__file__) , "../"))
# sys.path.insert(0,app_folder + "/mettl-api-sdk/src")


# from com.mettl.api.register.CandidateRegister import CandidateRegister
# from com.mettl.api.results.Results import Results
# from com.mettl.model.Candidates import Candidates
# from com.mettl.api.assessment.AssessmentInfo import AssessmentInfo
# from com.mettl.api.schedule.CreateSchedule import CreateSchedule
# from com.mettl.api.schedule.ScheduleInfo import ScheduleInfo
# from com.mettl.api.schedule.EditScheduleInfo import EditScheduleInfo


import logging
logger = logging.getLogger(__name__)

def test_finish_mail(to_email, full_name, module_name, pdf_link, status, marks, msg):
	#print TEST_FINISH_MAIL_HTML.format(full_name = full_name, module_name = module_name, pdf_link = pdf_link)
	send_mail(html_part = TEST_FINISH_MAIL_HTML.format(full_name = full_name.capitalize(), module_name = module_name, pdf_link = pdf_link, status = status, \
			scored = marks[1], total = marks[0], percentage = marks[2], msg = msg), to = to_email, subject = 'Congrats for completing the test')
	print 'Mail sent on finish test'

@csrf_exempt
def start_asm_notification(request):
	# logger.info('assesment_engine.start_asm_notification >> Test Start')
	asm_responce = json.loads(
		'''
	{
		"EVENT_TYPE": "startAssessment",
		"invitation_key": "f1bb27bf",
		"assessment_id": 66590,
		"candidate_instance_id": 1452533,
		"context_data": "{\\"applicant_id\\":874}",
		"timestamp_GMT": "Fri, 29 Aug 2014 08:55:26 GMT",
		"source_app": "certification-app",
		"notification_url": "http://application/path/listening/to/the/start/request",
		"name": "Amit",
		"email": "anshul.bisht06+90@gmail.com"
	}
'''  
		)
	asm_responce = json.loads(request.body)
	print asm_responce

	# if asm_responce['EVENT_TYPE'] == 'startAssessment':
		
	# 	logger.info('assesment_engine.start_asm_notification >> asm_responce[EVENT_TYPE] == startAssessment '+str(asm_responce['email']))

	# 	asm_reg_user = AssesmentRegisterdUser.objects.get(student_email = asm_responce['email'], schedule_key = asm_responce['invitation_key'])
	# 	assert asm_reg_user,'AssertError: AssesmentRegisterdUser not avail with {0} {1}'.format(asm_responce['email'], asm_responce['invitation_key'])
	# 	asm_reg_user.test_status = TEST_STATUS[0]

	# 	asm_reg_user.save()

	return HttpResponse(json.dumps(True), content_type = "application/json")


@csrf_exempt
def finish_asm_notification(request):
	logger.info('assesment_engine.finish_asm_notification >> Finish Start')
	asm_responce = json.loads(
	   '''
		{
			"EVENT_TYPE": "finishTest",
			"invitation_key": "f1bb27bf",
			"assessment_id": 66590,
			"candidate_instance_id": 1452533,
			"context_data": "{\\"applicant_id\\":874}",
			"timestamp_GMT": "Fri, 29 Aug 2014 09:48:53 GMT",
			"source_app": "certification-app",
			"notification_url": "http://application/path/listening/to/the/finish/request",
			"name": "Amit",
			"email": "anshul.bisht06+90@gmail.com",
			"finish_mode": "NormalSubmission"
		}'''
	)
	asm_responce = json.loads(request.body)

	# asm_responce = str(request.body)
	if asm_responce['EVENT_TYPE'] == 'finishTest':
		
		logger.info('assesment_engine.finish_asm_notification >> asm_responce[EVENT_TYPE] == finishTest '+str(asm_responce['email']))

		asm_reg_user = AssesmentRegisterdUser.objects.get(student_email = asm_responce['email'], schedule_key = asm_responce['invitation_key'])
		assert asm_reg_user,'AssertError: AssesmentRegisterdUser not avail with {0} {1}'.format(asm_responce['email'], asm_responce['invitation_key'])
		asm_reg_user.test_status = TEST_STATUS[1]
		asm_reg_user.save()

		return HttpResponse(json.dumps(True), content_type = "application/json")
	

@csrf_exempt
def grade_asm_notification(request):
	status = 'failed'
	logger.info('assesment_engine.grade_asm_notification >> ........Start')
	try:
		asm_responce = json.loads(request.body)
		if asm_responce['EVENT_TYPE'] == 'gradedAssessment':
			
			logger.info('assesment_engine.grade_asm_notification >> asm_responce[EVENT_TYPE] == gradedAssessment '+str(asm_responce['email']))

			asm_reg_user = AssesmentRegisterdUser.objects.get(student_email = asm_responce['email'], schedule_key = asm_responce['invitation_key'])
			assert asm_reg_user,'AssertError: AssesmentRegisterdUser not avail with {0} {1}'.format(asm_responce['email'], asm_responce['invitation_key'])
			

			asm_reg_user.test_status = TEST_CHECK_FOR[1]
			asm_reg_user.candidate_instance_id = int(asm_responce['candidate_instance_id'])
			
			max_marks = float(asm_responce['max_marks'])
			max_marks_scored = float(asm_responce['marks_scored'])
			percentage = max_marks_scored/max_marks
			user_result = UserResult.objects.create(assesmentRegisterdUser = asm_reg_user,
				percentile = asm_responce['percentile'], max_marks = max_marks,
				marks_scored = max_marks_scored, finish_mode = asm_responce['finish_mode'])
			user_result.save()
			logger.info('assesment_engine.grade_asm_notification >> user_result save SUCCESS'+str(asm_responce['email']))

			if percentage < 0.75:
				logger.info('assesment_engine.grade_asm_notification >> percentage < 0.75  User >>> FAIL'+str(asm_responce['email']))
				asm_reg_user.result_status = TEST_CHECK_FOR[2]
				asm_reg_user.save()
			else:
				status = 'passed'
				logger.info('assesment_engine.grade_asm_notification >> percentage > 0.75  User >>> PASS'+str(asm_responce['email']))
				asm_reg_user.result_status = TEST_CHECK_FOR[0]
				asm_reg_user.save()
			test = Tests.objects.filter(schedule_key = asm_responce['invitation_key'])
			msg = 'There is no re-attempt chance.'
			if test:
				if test[0].test_type == 'E':
					enrollcourse = EnrolledCourses.objects.get(course = test[0].course, user = User.objects.get(email = asm_responce['email']))
					enrollcourse.is_complete = True
					enrollcourse.save()
					if percentage >= 0.75:
						html = PROFESSIONAL_CERTIFICATE_HTML.format(course = test[0].course)
						send_mail.delay(html, asm_responce['email'], subject = 'Please register for taking the Professional Certificate')
					html = CERTIFICATE_MAIL_HTML.format(link = str(SITE_NAME)+'/download/certificate/'+test[0].course.course_uuid+'/', course = test[0].course.course_name)
					send_mail(html, asm_responce['email'], subject = 'Congratulations on completing the course')
				elif test[0].test_type == 'I':
					msg = 'If you have failed then you must retake the test on the same module.'
				if status == 'failed':
					msg = msg + 'If there is no re-attempt chance left then you must re-register to take the course.'
				test_finish_mail(to_email = asm_responce['email'], module_name = asm_responce['assessment_name'], \
								full_name = asm_responce['name'], pdf_link = str(SITE_NAME)+'/download/report/test/' + asm_responce['invitation_key'] + '/',\
								status = status, marks=(max_marks, max_marks_scored, round(percentage*100,2),), msg = msg)
			return HttpResponse(json.dumps(True), content_type = "application/json")
	except Exception as e:
		logger.info('assesment_engine.grade_asm_notification >> '+str(e.args))
		# print e.args
		return HttpResponse(json.dumps(False), content_type = "application/json")		


def can_take_test(user, course):
	return EnrolledCourses.objects.is_student_enrolled(user, course)

def register_student(username, email, schedule_key):
	return register_user(username, email, schedule_key)

def get_all_assesments(request):
	public  = METTL_CONFIG[0]
	private = METTL_CONFIG[1]
	is_prod = METTL_CONFIG[2]
	# print AssessmentInfo(public,private,is_prod).getAllAssessments({})
	# print AssessmentInfo(public,private,is_prod).getAssessmentDetails(assessment_id=66590)

@login_required
@student_required
def assessment_inline(request, course_uuid, test_key):
	course = CourseDetail.objects.get(course_uuid = course_uuid)
	'''
	{"status":"SUCCESS","username":"gaurav",
		"testUser":5,"is_new":false,
		"token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.
		eyJ1c2VybmFtZSI6ImdhdXJhdiIsInVzZXJfaWQiOjEsImVtYWlsIjoiZ3J2dHlhZ2kyMkBnbWFpbC5jb20iLCJleHAiOjE3NTkyMzM2NDl9.lH_Q3qu8lKVs5j4k6paYkA3MB8zECy4XmqB4vzEKxXk",
		"test":
			{"test_key":"c3vsg3jcp7","sectionNoWhereLeft":null,
				"existingAnswers":{"answers":{}},
				"status":"ToBeTaken","sectionsRemaining":[],"isTestNotCompleted":false
			}
		}
	'''
	logger.info('assesment_engine.assessment_inline >> User Take test for >>>'+str(course))
	if can_take_test(request.user, course):
		logger.info('assesment_engine.assessment_inline >> Under True << can_take_test(request.user, course) >>>'+str(course)+' UID:'+str(request.user.id))
		json_output = json.loads(register_student(request.user.username,request.user.email,test_key))
		print json_output
		reg_status = json_output['status']
		if reg_status == 'SUCCESS':
			logger.info('assesment_engine.assessment_inline >> Under  True << reg_status == SUCCESS UID:'+str(request.user.id))
			try:
				test_status = json_output['test']['status']
				test = Tests.objects.get(schedule_key = test_key)
				
				logger.info('assesment_engine.assessment_inline >> test_status>> '+str(test_status)+' UID:'+str(request.user.id))
				
				if test_status == 'ToBeTaken':
					assessment_reg_user,created = AssesmentRegisterdUser.objects.get_or_create(student = request.user, course=course, 
						test = test, defaults = {'remaning_attempts' : json_output['test']['remaining_attempts']-1,'schedule_key':test_key, 
						'student_email':request.user.email})

					test_url =  json_output['test']['testURL']
					logger.info('assesment_engine.assessment_inline >> markes as ToBeTaken UID:'+str(request.user.id))
					return HttpResponseRedirect(test_url)
				
				elif test_status == 'NOT_REMAINING':
					assment_reg_user = AssesmentRegisterdUser.objects.get(student = request.user, course = course, test = test)
					assment_reg_user.remaning_attempts = 0
					assment_reg_user.save()

					messages.info(request,"No remaning attempts.")
					return redirect('/course/details/'+course_uuid)

				elif test_status == 'INCOMPLETE':
					print 'under incomplete ........'
					test_url =  json_output['test']['testURL']
					return HttpResponseRedirect(test_url)

			except Exception as e:
				print e.args
				logger.error('assesment_engine.assessment_inline >> '+str(e.args)+' UID:'+str(request.user.id))
				return redirect('/course/details/'+course_uuid)
	# print e.args			
	logger.error('assesment_engine.assessment_inline >> You cant take this test UID:'+str(request.user.id))
	messages.info(request,"You can't take this test.")
	return redirect('/home/')



@login_required
@student_required
def assesment_end_test(request, course_uuid, schedule_key):
	course = CourseDetail.objects.get(course_uuid = course_uuid)
	course_weeks = CourseWeek.objects.filter(course = course)
	enrollcourse = can_take_test(request.user, course)

	logger.info('assesment_engine.assesment_end_test >> Under .......UID: '+str(request.user.id)+str(course))
	if enrollcourse:
		if all([ UserCourseProgress.objects.get(course_week = course_week, enrolled_courses = enrollcourse).progress_status == PROGRESS_STATUSES[2] for course_week in course_weeks]):
			json_output = register_student(request.user.username,request.user.email,schedule_key)
			reg_status = json_output['status']
			test_taken_status =  json_output['registrationStatus'][0]['status']

			if reg_status == 'SUCCESS':
				logger.info('assesment_engine.assesment_end_test >>Under  reg_status == SUCCESS UID:'+str(request.user.id)+str(course))
				try:
					test_status = (json_output['registrationStatus'][0])['status']
					test = Tests.objects.get(schedule_key = schedule_key)
					course = CourseDetail.objects.get(course_uuid=course_uuid)
					if test_status == 'ToBeTaken':
						logger.info('assesment_engine.assesment_end_test >>Under  test_status == ToBeTaken UID:'+str(request.user.id)+str(course))
						assessment_reg_user = AssesmentRegisterdUser.objects.initiate(student = request.user, course=course,schedule_key=schedule_key,student_email = request.user.email,
						registrationStatus_status = test_status, test = test)
						test_url =  (json_output['registrationStatus'][0])['url']
						return HttpResponseRedirect(test_url)
					elif test_status == 'Completed':
						assment_reg_user = AssesmentRegisterdUser.objects.get(student = request.user, course = course, schedule_key = schedule_key,test = test)
						assment_reg_user.registrationStatus_status = test_status
						logger.info('assesment_engine.assesment_end_test >>Under  test_status == Completed UID:'+str(request.user.id)+str(course))
						assment_reg_user.save()
						messages.info(request,'This test marks as completed.'+request.user)
						return redirect('/course/details/'+course_uuid)
				except Exception as e:
					logger.error('assesment_engine.assesment_end_test >>Under  test_status == Completed UID:'+str(request.user.id)+str(course)+str(e.args))
					return redirect('/course/details/'+course_uuid)
		else:
			logger.error('assesment_engine.assesment_end_test >>First complete all videos and tests UID:'+str(request.user.id)+str(course))
			messages.info(request,'First complete all videos and tests.')
			
			return redirect('/course/videos/'+course.course_uuid+'/')
	messages.info(request,"You can't take this test.")
	return redirect('/course/details/'+course_uuid)


@login_required
def assessment_student_result(request, asm_reg_user, schedule_key):
		public  = "4a9bbe63-b533-49de-b1bb-9f6adcc38dc5"
		private = "66ba7de5-4bff-4ba9-88a4-12b7d8d568f9"
		is_prod = True

		result = Results(public , private , is_prod)
		result_params = {}
		json_output = result.getResultForCandidateInSchedule(schedule_key, request.user.email, result_params)
		testStatus = json_output['testStatus']

		if testStatus['status'] == 'Completed':
			
			try:
			   assesmentRegisterdUser = asm_reg_user
			   
			   test_marks_obj = TestMarks.objects.update_or_create(quiz_marks = testStatus['result']['totalQuestion'], total_marks = testStatus['result']['totalMarks'],test_type='NOT AVAIL', 
				assesmentRegisterdUser = assesmentRegisterdUser) 
			   
			   test_status_obj = TestStatus.objects.update_or_create(assesmentRegisterdUser = assesmentRegisterdUser, status = testStatus['status'], htmlReport = testStatus['htmlReport'],
				startTime = testStatus['startTime'], endTime = testStatus['endTime'], completionMode = testStatus['completionMode'], pdfReport = testStatus['pdfReport'])
			   
			   json_result = testStatus['result']

			   result_obj = Result.objects.update_or_create(testStatus = test_status_obj[0], totalCorrectAnswers = json_result['totalCorrectAnswers'], 
				totalQuestion = json_result['totalQuestion'], totalMarks = json_result['totalMarks'], attemptTime = json_result['attemptTime'], analysis = json_result['analysis'],
				 totalUnAnswered = json_result['totalUnAnswered'], percentile = json_result['percentile'], maxMarks = json_result['maxMarks'])
			   
			   json_section = json_result['sectionMarks']
			   
			   for section in json_section:
					SectionMarks.objects.update_or_create(result = result_obj[0], totalCorrectAnswers = section['totalCorrectAnswers'], skillName = section['skillMarks'][0]['skillName'], totalMarks = section['totalMarks'],
						totalQuestion = section['totalQuestion'], timeTaken = section['timeTaken'], totalUnAnswered = section['totalUnAnswered'], maxMarks = section['maxMarks'], 
						questions = section['skillMarks'][0]['questions'])
			
			except Exception as e:
				print e.args
			
			messages.info(request,'You already took this test')
			return HttpResponseRedirect('/dashboard/')
		else:
			messages.info(request,'Your test result is under processing')
			return redirect('/home/')   


# def createSchedule(request, course_uuid, assessment_id):
# 	public  = "4a9bbe63-b533-49de-b1bb-9f6adcc38dc5"
# 	private = "66ba7de5-4bff-4ba9-88a4-12b7d8d568f9"
# 	is_prod = True

# 	sc = {"assessmentId": assessment_id,    
# 			"name": "Schedule 1w786",
# 			"imageProctoring": False,
# 			"webProctoring": {
# 			"enabled": False
# 			},
# 			"scheduleType": "AlwaysOn",
# 			"scheduleWindow": None,
# 			"access": {
# 			"type": "OpenForAll",
# 			"candidates": None,
# 			"sendEmail": False
# 			},
# 			"ipAccessRestriction": {
# 			"enabled": False
# 			},
# 			"allowCopyPaste": True,
# 			"exitRedirectionUrl": "http://equest.co/",
# 			"showResultsOnTestCompletion": False,
# 			"sourceApp": "eQuest",
# 			"testStartNotificationUrl": "http://equest.co/start/asm_notification/",
# 			"testFinishNotificationUrl": "http://equest.co/finish/asm_notification/",
# 			"testGradedNotificationUrl": "http://equest.co/grade/asm_notification/",
# 			}

# 	csh = CreateSchedule(public , private , is_prod)
# 	url = csh.createScheduleForAssessment(assessment_id, params = sc)
# 	headers = {'content-type': 'application/json'}
# 	response = requests.post(url, headers=headers)
# 	schedule_created = json.loads(response.content)
# 	print schedule_created
# 	if schedule_created['status'] == 'SUCCESS':
# 		schedule_key = schedule_created['createdSchedule']['accessKey']
# 		sc['exitRedirectionUrl'] = sc['exitRedirectionUrl'] + schedule_key + "/"
# 		print 'call edit method ............>>>>>>>>>'
# 		return edit_schedule_info(schedule_key, 66590, 'Schedule 1w786')
# 	else:
# 		print '>>>>>>>>>>>>>>>>>>> No schedule created'
# 	return HttpResponse('Test Link created!!!')




