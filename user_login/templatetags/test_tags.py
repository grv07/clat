from __future__ import division
from django.template import Library
from django.template.defaultfilters import stringfilter
from tracker.models import StudentTracker,Progress
from course_mang.models import CourseWeek
from course_mang.utilities import check_progress_time
from course_test_handling.models import Tests
from student.models import UserCourseProgress, EnrolledCourses
from assesment_engine.models import AssesmentRegisterdUser, UserResult
from student.models import Student
register = Library()

@register.filter(name = 'divideby')
def divideby(divisor, dividend=100):
	return dividend/float(divisor)

@stringfilter
@register.filter(name = 'to_newline')
def to_newline(value):
		value = value.replace('**','<br>')
		return value


@register.filter(name = 'get_test')
def get_inline_test(schedule_key, module_name = None):
	'''Return Test object on module name and schedule key'''	
	try:
		test = None
		if module_name:
			test = Tests.objects.get(module_name = module_name, schedule_key = schedule_key)
		else:
			test = Tests.objects.get(schedule_key = schedule_key)
		assert test,'AssertError: Test is None'
		return test
	except Exception as e:
		print 'get_inline_test',e.args
		return None

def get_user_result(test, user):
		try:
			asm_reg_user = AssesmentRegisterdUser.objects.get(student = user, test = test)
			assesment_user_result = UserResult.objects.filter(assesmentRegisterdUser = asm_reg_user)
			result_data = None
			for user_result in assesment_user_result:
				if float(user_result.marks_scored)/float(user_result.max_marks) < 0.75:
					result_data = [True,'FAIL']
				return [True,'PASS']
		except Exception as e:
				print 'get_user_result >> ',e.args
				return [True,'']


@register.filter(name = 'check_for_inline_pass')
def check_for_inline_pass(test, user):
	return get_user_result(test, user)


@register.filter(name = 'check_for_pass')
def check_for_midendterm_pass(test, user):
	return get_user_result(test, user)


@register.filter(name = 'check_access_status')
def check_access_status(module_name, enrolledcourse):
	try:
		userprogress = UserCourseProgress.objects.get(enrolled_courses = enrolledcourse, course_week = CourseWeek.objects.get(week_module_name = module_name))
		assert userprogress.access_status == 'OPEN','AssertError: ON userprogress.access_status == "OPEN"'
		return True
	except Exception as e:
		return False


@register.filter(name = 'check_progress_status')
def check_progress_status(module_name, enrolledcourse):
	try:
		userprogress = UserCourseProgress.objects.get(enrolled_courses = enrolledcourse, course_week = CourseWeek.objects.get(week_module_name = module_name))
		assert userprogress.progress_status == 'COMPLETE','AssertError: ON userprogress.progress_status == "COMPLETE"'
		# if userprogress.progress_status == 'COMPLETE':
		return True
		# return False
	except Exception as e:
		return False

@register.filter(name = 'time_progress')
def time_progress(course_module, user):
		try:
			stu_tracker = StudentTracker.objects.get(student = user, module_name = course_module.week_module_name)
			progress = Progress.objects.get(tracker = stu_tracker) 
			# print progress
			return check_progress_time(progress.time_progress)
		except Exception as e:
			print 'time_progress',e.args
			return 0

@register.filter(name = 'module_list')
def module_list(enroll_course):
	try:
		course_module = CourseWeek.objects.filter(course = enroll_course).order_by("module_number")
		return course_module
	except Exception as e:
		print e.args
		return None

@register.filter(name = 'module_inline_list')
def module_inline_list(enroll_course):
	try:
		result = []
		course_module = module_list(enroll_course)  
		for course_week in course_module:
			if Tests.objects.get(course = enroll_course, module_name = course_week.week_module_name, test_type = 'I'):
				result.append(course_week)
		return result
	except Exception as e:
		return None


@register.filter(name = 'module_midterm_list')
def module_midterm_list(enroll_course):
	try:
		result=[]
		course_module = module_list(enroll_course)   
		for course_week in course_module:
			if Tests.objects.filter(course = enroll_course, module_name = course_week.week_module_name, test_type = 'M'):
				result.append(course_week)
		return result
	except Exception as e:
		print 'module_midterm_list',e.args
		return None


@register.filter(name = 'module_endterm_list')
def module_endterm_list(enroll_course):
	try:
		course_module = module_list(enroll_course)   
		if Tests.objects.filter(course = enroll_course, module_name = 'end',test_type = 'E'):
			return enroll_course
		else:
			return None
	except Exception as e:
		print 'module_endterm_list',e.args
		return None


@register.filter(name = 'test_progress')
def test_progress(schedule_key, user):
	'''Get tests progress in percentile '''
	try:
		assert schedule_key,'Schedule key is not given'
		asm_user = AssesmentRegisterdUser.objects.get(schedule_key = schedule_key, student_email = user.email)
		data = []
		# for asm_user in asm_reg_user:
		user_results =  UserResult.objects.filter(assesmentRegisterdUser = asm_user)
		for user_result in user_results:
			data += [round(float(user_result.marks_scored)/float(user_result.max_marks)*100, 2)]
		return data
	except Exception as e:
		print 'test_progress',e.args
		return -1

@register.filter(name = 'module_width')
def module_width(enroll_course):
	try:
		course_module = CourseWeek.objects.filter(course = enroll_course)
		return 100/len(course_module)
	except Exception as e:
		return 0

@register.filter(name='test_width')
def test_width(enroll_course, course_type = None):
	try:
		test_list = Tests.objects.filter(course = enroll_course)
		return 100/len(test_list)
	except Exception as e:
		return 0


@register.filter(name = 'is_user_pass')
def is_user_pass(user, schedule_key):
	try:
		asm_reg_user = AssesmentRegisterdUser.objects.get(student = user, schedule_key = schedule_key)
		# print asm_reg_user.schedule_key
		assert (asm_reg_user.result_status == 'FAIL'),'AssertError: asm_reg_user.result_status == "FAIL"'
		# if asm_reg_user.result_status == 'FAILED':
			# return False
		return True
	except Exception as e:
		print 'is_user_pass', e.args
		return False


@register.filter(name='is_user_take_test')
def is_user_take_test(test, email):
	try:
		asm_user = AssesmentRegisterdUser.objects.get(test = test, student_email = email)
		if not asm_user:
			print 'Still not even register'
			return ['NOT_REG', True, 0]
		else:
			# for asm_user in asm_reg_user:
			return_data = []
			return_data += [asm_user.result_status] if asm_user.result_status in ['PASS', 'WAITING'] else ['FAIL']
			
			if asm_user.remaning_attempts > 0:
				return_data += [True]
			else:
				print 'Fail in this test'
				return return_data+[False, asm_user.remaning_attempts]
		
		return return_data+[asm_user.remaning_attempts]
		
	except Exception as e:
		print 'is_user_take_test',e.args
		return ['NOT_REG', True, None]


@register.filter(name = 'get_inline_test_key')
def get_inline_test_key(module_name, user):
    test_result = 'FAIL'
    test = Tests.objects.get(module_name = module_name, test_type = 'I')
    can_attempt = is_user_take_test(test, user.email)
    if can_attempt[1]:
    	return [test.schedule_key, can_attempt[0], can_attempt[2]]
    else:
    	return [None, can_attempt[0], 0]	
    # for idx,test in enumerate(tests):
                    # print user.email
                    # can_attempt = is_user_take_test(test, user.email)
                    # #print '................'+str(can_attempt)
                    # #print idx
                    # if can_attempt[1]:
                    #         if can_attempt[0] == 'PASS':
                    #                 test_result = 'PASS'
                    #                 if idx < 2:
                    #                      continue
                    #                 else:
                    #                      return [None, test_result, idx]
                    #         else:
                    #               return [test.schedule_key, test_result, idx+1]
                    # elif idx == 2:
                    #         #print 'End condition'
                    #         return [None, test_result, idx]
					
			

@register.filter(name='inline_test_key')
def inline_test_key(course_module_name, course):
	'''Get all inline for a module and course ...... '''
	try:
			return Tests.objects.get(course = course, module_name = course_module_name, test_type = 'I').schedule_key
	except Exception as e:
			print 'inline_test_key >>',e.args
			return None


@register.filter(name='check_for_max_marks')
def check_for_max_marks(schedule_key, user):
	'''Check for maximum marks of user in INLINE test'''
	try:
		asm_reg_user = AssesmentRegisterdUser.objects.get(schedule_key= schedule_key, student = user)
		user_result = UserResult.objects.filter(assesmentRegisterdUser = asm_reg_user).order_by('-marks_scored')[0]
		return round(float(user_result.marks_scored)/float(user_result.max_marks)*100, 2)
	except Exception as e:
		print 'check_for_max_marks >>>>',e.args
		return None


''' Check for end test completion '''
@register.filter(name = 'isEndTestGraded')
def isEndTestGraded(course, user):
	try:
		end_test = Tests.objects.get(course = course,module_name='end',test_type='E')
		assreguser = AssesmentRegisterdUser.objects.get(course=course, student=user, test=end_test,schedule_key = end_test.schedule_key)
		if assreguser and assreguser.test_status == 'GRADED':
			return True
		return False
	except Exception as e:
		print 'isEndTestGraded',e.args
		return False
