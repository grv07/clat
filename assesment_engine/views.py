# Create your views here.
import os
import sys
import json  
from django.shortcuts import HttpResponseRedirect, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from assesment_engine.models import AssesmentRegisterdUser,UserResult

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


import logging
logger = logging.getLogger(__name__)

def test_finish_mail(to_email, full_name, module_name, pdf_link, status, marks, msg):
	#print TEST_FINISH_MAIL_HTML.format(full_name = full_name, module_name = module_name, pdf_link = pdf_link)
	send_mail(html_part = TEST_FINISH_MAIL_HTML.format(full_name = full_name.capitalize(), module_name = module_name, pdf_link = pdf_link, status = status, \
			scored = marks[1], total = marks[0], percentage = marks[2], msg = msg), to = to_email, subject = 'Congrats for completing the test')
	print 'Mail sent on finish test'

@csrf_exempt
def start_asm_notification(request):
	logger.info('assesment_engine.start_asm_notification >> Test Start')
	# asm_response = json.loads(
	# 	'''
	# 	{
	# 		"EVENT_TYPE": "startTest",
	# 		"test_key": "fn8jmwq6df", 
	# 		"username": "anshul02", 
	# 		"notification_url": "http://localhost:8001/start/asm_notification/", 
	# 		"sitting_id": 145, 
	# 		"timestamp_IST": "2016-03-29 10:42:35.829936+00:00", 
	# 		"test_user_id": 100, 
	# 		"email": "ansh.vengaboyz@gmail.com"
	# 	}
	# 	'''  
	# )
	asm_response = json.loads(request.body)

	print asm_response
	try:
		if asm_response['EVENT_TYPE'] == 'startTest':
			
			logger.info('assesment_engine.start_asm_notification >> asm_response[EVENT_TYPE] == startAssessment '+str(asm_response['email']))

			asm_reg_user = AssesmentRegisterdUser.objects.get(student_email = asm_response['email'], schedule_key = asm_response['test_key'])
			assert asm_reg_user,'AssertError: AssesmentRegisterdUser not avail with {0} {1}'.format(asm_response['email'], asm_response['test_key'])
			asm_reg_user.test_status = TEST_STATUS[0]

			asm_reg_user.save()
	except Exception as e:
		print e.args		
	return HttpResponse(json.dumps(True), content_type = "application/json")

@csrf_exempt
def finish_asm_notification(request):
	logger.info('assesment_engine.finish_asm_notification >> Finish Start')
	# asm_response = json.loads(
	#    '''
	# 	{
	# 		"EVENT_TYPE": "finishTest",
	# 		"test_key": "fn8jmwq6df", 
	# 		"username": "anshul02", 
	# 		"notification_url": "http://localhost:8001/start/asm_notification/", 
	# 		"sitting_id": 145, 
	# 		"timestamp_IST": "2016-03-29 10:42:35.829936+00:00", 
	# 		"test_user_id": 100, 
	# 		"email": "ansh.vengaboyz@gmail.com",
	# 		"finish_mode": "NormalSubmission"
	# 	}
	# 	'''
	# )
	asm_response = json.loads(request.body)
	print asm_response
	# asm_response = str(request.body)
	try:
		if asm_response['EVENT_TYPE'] == 'finishTest':
			logger.info('assesment_engine.finish_asm_notification >> asm_response[EVENT_TYPE] == finishTest '+str(asm_response['email']))
			asm_reg_user = AssesmentRegisterdUser.objects.get(student_email = asm_response['email'], schedule_key = asm_response['test_key'])
			assert asm_reg_user,'AssertError: AssesmentRegisterdUser not avail with {0} {1}'.format(asm_response['email'], asm_response['test_key'])
			asm_reg_user.test_status = TEST_STATUS[1]
			asm_reg_user.save()
	except Exception as e:
		print e.args		

	return HttpResponse(json.dumps(True), content_type = "application/json")
	

@csrf_exempt
def grade_asm_notification(request):
	try:
		# asm_response = json.loads(
		# 	'''
		# 	{
		# 	"test_key": "fn8jmwq6df", 
		# 	"username": "anshul02", 
		# 	"quiz_name": "Maths", 
		# 	"notification_url": "http://localhost:8001/grade/asm_notification/", 
		# 	"EVENT_TYPE": "gradeTest", 
		# 	"total_questions": 47, 
		# 	"result_status": "Pass", 
		# 	"finish_mode": "NormalSubmission", 
		# 	"start_time_IST": "2016-03-29 11:26:48.294887+00:00", 
		# 	"total_marks": 47, 
		# 	"email": "ansh.vengaboyz@gmail.com", 
		# 	"attempt_no": 1, 
		# 	"sitting_id": 148, 
		# 	"timestamp_IST": "2016-03-29 11:27:56.049465+00:00", 
		# 	"test_user_id": "103", 
		# 	"incorrect_questions_score": 8.0, 
		# 	"end_time_IST": "2016-03-29 11:27:55.081703+00:00", 
		# 	"quiz_id": 13,
		# 	"htmlReport":'example.com' 
		# 	"correct_questions_score": 48, 
		# 	"passing_percentage": 0,
		# 	"marks_scored": 24
		# 	}
		# 	''')
		status = 'failed'
		logger.info('assesment_engine.grade_asm_notification >> ........Start')
		try:
			asm_response = json.loads(request.body)
			if asm_response['EVENT_TYPE'] == 'gradeTest':
				
				logger.info('assesment_engine.grade_asm_notification >> asm_response[EVENT_TYPE] == gradeTest '+str(asm_response['email']))

				asm_reg_user = AssesmentRegisterdUser.objects.get(student_email = asm_response['email'], schedule_key = asm_response['test_key'])
				assert asm_reg_user,'AssertError: AssesmentRegisterdUser not avail with {0} {1}'.format(asm_response['email'], asm_response['test_key'])
				asm_reg_user.assessment_name = asm_response['quiz_name']

				asm_reg_user.test_status = TEST_CHECK_FOR[1]
				asm_reg_user.candidate_instance_id = int(asm_response['test_user_id'])
				
				max_marks = float(asm_response['total_marks'])
				max_marks_scored = float(asm_response['marks_scored'])
				
				percentage = max_marks_scored/max_marks
				user_result = UserResult.objects.create(assesmentRegisterdUser = asm_reg_user,
					percentile = float(0), max_marks = max_marks, attempt_no = asm_response['attempt_no'],
					marks_scored = max_marks_scored, finish_mode = asm_response['finish_mode'], report_link = asm_response['htmlReport'])

				logger.info('assesment_engine.grade_asm_notification >> user_result save SUCCESS'+str(asm_response['email']))
				asm_reg_user.remaning_attempts = asm_reg_user.remaning_attempts - 1
				
				if percentage < 0.75:
					logger.info('assesment_engine.grade_asm_notification >> percentage < 0.75  User >>> FAIL'+str(asm_response['email']))
					if not asm_reg_user.result_status == TEST_CHECK_FOR[0]:
						asm_reg_user.result_status = TEST_CHECK_FOR[2]
					user_result.result_status = TEST_CHECK_FOR[2]
				
				elif percentage >= 0.75:
					status = 'passed'
					logger.info('assesment_engine.grade_asm_notification >> percentage > 0.75  User >>> PASS'+str(asm_response['email']))
					asm_reg_user.result_status = TEST_CHECK_FOR[0]
					user_result.result_status = TEST_CHECK_FOR[0]
				
				asm_reg_user.save()
				user_result.save()

				test = Tests.objects.filter(schedule_key = asm_response['test_key'])
				msg = 'There is no re-attempt chance.'
				if test:
					if test[0].test_type == 'E':
						enrollcourse = EnrolledCourses.objects.get(course = test[0].course, user = User.objects.get(email = asm_response['email']))
						enrollcourse.is_complete = True
						enrollcourse.save()
						if percentage >= 0.75:
							html = PROFESSIONAL_CERTIFICATE_HTML.format(course = test[0].course)
							send_mail(html, asm_response['email'], subject = 'Please register for taking the Professional Certificate')
						html = CERTIFICATE_MAIL_HTML.format(link = str(SITE_NAME)+'/download/certificate/'+test[0].course.course_uuid+'/', course = test[0].course.course_name)
						send_mail(html, asm_response['email'], subject = 'Congratulations on completing the course')
					elif test[0].test_type == 'I':
						msg = 'If you have failed then you must retake the test on the same module.'
					if status == 'failed':
						msg = msg + 'If there is no re-attempt chance left then you must re-register to take the course.'
					test_finish_mail(to_email = asm_response['email'], module_name = asm_response['quiz_name'], \
									full_name = asm_response['username'], pdf_link = str(SITE_NAME)+'/download/report/test/' + asm_response['test_key'] + '/' + asm_response['attempt_no'] + '/',\
									status = status, marks=(max_marks, max_marks_scored, round(percentage*100,2),), msg = msg)
		        
		        return HttpResponse(json.dumps(True), content_type = "application/json")
		except Exception as e:
			logger.info('assesment_engine.grade_asm_notification >> '+str(e.args))
			print e.args
	except Exception as e:
			print e.args
	return HttpResponse(json.dumps(False), content_type = "application/json")		


def can_take_test(user, course):
	return EnrolledCourses.objects.is_student_enrolled(user, course)

# Currently not in use ..
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
		eyJ1c2VybmFtZSI6ImdhdXJhdiIsInVzZXJfaWQiOjEsImVtYWlsIjoiZ3J2dHlhZ2kyMkBnbWFpbC5
		jb20iLCJleHAiOjE3NTkyMzM2NDl9.lH_Q3qu8lKVs5j4k6paYkA3MB8zECy4XmqB4vzEKxXk",
		"test":
			{"test_key":"c3vsg3jcp7","sectionNoWhereLeft":null,
				"existingAnswers":{"answers":{}},
				"status":"ToBeTaken","sectionsRemaining":[],"isTestNotCompleted":false
			}
		}
	'''
	logger.info('assesment_engine.assessment_inline >> User Take test for >>>'+str(course))
	enr_course = can_take_test(request.user, course)
	if enr_course:
		logger.info('assesment_engine.assessment_inline >> Under True << can_take_test(request.user, course) >>>'+str(course)+' UID:'+str(request.user.id))
		json_output = json.loads(register_user(request.user.username,request.user.email,test_key))
		print json_output
		reg_status = json_output['status']
		if reg_status == 'SUCCESS':
			logger.info('assesment_engine.assessment_inline >> Under  True << reg_status == SUCCESS UID:'+str(request.user.id))
			try:
				test_status = json_output['test']['status']
				test = Tests.objects.get(schedule_key = test_key)
				
				logger.info('assesment_engine.assessment_inline >> test_status>> '+str(test_status)+' UID:'+str(request.user.id))
				
				if test_status == 'ToBeTaken':
					assessment_reg_user,created = AssesmentRegisterdUser.objects.get_or_create(student = request.user, enr_course=enr_course, 
						test = test, schedule_key = test_key, defaults = {'student_email':request.user.email})
					assessment_reg_user.remaning_attempts = json_output['test']['remaining_attempts']
					test_url =  json_output['test']['testURL']
					assessment_reg_user.save()
					logger.info('assesment_engine.assessment_inline >> markes as ToBeTaken UID:'+str(request.user.id))
					return HttpResponseRedirect(test_url)
				
				elif test_status == 'NOT_REMAINING':
					assment_reg_user = AssesmentRegisterdUser.objects.get(student = request.user, enr_course=enr_course, test = test)
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
	enr_course = can_take_test(request.user, course)

	logger.info('assesment_engine.assesment_end_test >> Under .......UID: '+str(request.user.id)+str(course))
	if enr_course:
		if all([ UserCourseProgress.objects.get(course_week = course_week, enrolled_courses = enr_course).progress_status == PROGRESS_STATUSES[2] for course_week in course_weeks]):
			json_output = register_student(request.user.username,request.user.email,schedule_key)
			reg_status = json_output['status']
			test_taken_status =  json_output['registrationStatus'][0]['status']

			if reg_status == 'SUCCESS':
				logger.info('assesment_engine.assesment_end_test >>Under  reg_status == SUCCESS UID:'+str(request.user.id)+str(course))
				try:
					test_status = (json_output['registrationStatus'][0])['status']
					test = Tests.objects.get(schedule_key = schedule_key)
					if test_status == 'ToBeTaken':
						logger.info('assesment_engine.assesment_end_test >>Under  test_status == ToBeTaken UID:'+str(request.user.id)+str(course))
						assessment_reg_user = AssesmentRegisterdUser.objects.initiate(student = request.user, enr_course = enr_course,schedule_key=schedule_key,student_email = request.user.email,
						registrationStatus_status = test_status, test = test)
						test_url =  (json_output['registrationStatus'][0])['url']
						return HttpResponseRedirect(test_url)
					elif test_status == 'Completed':
						assment_reg_user = AssesmentRegisterdUser.objects.get(student = request.user, enr_course = enr_course, schedule_key = schedule_key, test = test)
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
