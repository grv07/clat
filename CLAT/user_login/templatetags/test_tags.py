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
		print e.args
		return None

def get_user_result(test, user):
		try:
			asm_reg_user = AssesmentRegisterdUser.objects.get(student = user, test = test)
			user_result = UserResult.objects.get(assesmentRegisterdUser = asm_reg_user)
			if float(user_result.marks_scored)/float(user_result.max_marks) < 0.75:
				return [True,'FAIL']
			return [True,'PASS']
		except Exception as e:
				print e.args
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
			print type(course_module)
			stu_tracker = StudentTracker.objects.get(student = user, module_name = course_module.week_module_name)
			print stu_tracker
			progress = Progress.objects.get(tracker = stu_tracker) 
			# print progress
			return check_progress_time(progress.time_progress)
		except Exception as e:
			print e.args
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
			if Tests.objects.filter(course = enroll_course, module_name = course_week.week_module_name, test_type = 'I'):
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
		print e.args
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
		return None


@register.filter(name = 'test_progress')
def test_progress(schedule_key, user):
	'''Get tests progress in percentile '''
	try:	
		assert schedule_key,'Schedule key is not given'
		asm_reg_user = AssesmentRegisterdUser.objects.get(schedule_key = schedule_key, student_email = user.email)
		userresult =  UserResult.objects.get(assesmentRegisterdUser = asm_reg_user)
		data = float(userresult.marks_scored)/float(userresult.max_marks)*100
		return round(data, 2)
	except Exception as e:
		print e.args
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
		print e.args
		return False


@register.filter(name='is_user_take_test')
def is_user_take_test(test, email):
	try:
		asm_reg_user = AssesmentRegisterdUser.objects.filter(test = test, student_email = email)
		
		if asm_reg_user.count() == 0:
			print 'Still not even register'
			return ['NOT_REG', True]
		
		elif asm_reg_user.filter(result_status = 'PASS'):
			return ['PASS', True]
		
		elif asm_reg_user.filter(result_status = 'WAITING'):
			return ['WAITING', True]
		
		else:
			# asm_reg_user.filter(result_status = 'FAILED')
			print 'Fail in this test' 
			return ['FAIL', False]
		
	except Exception as e:
		print e.args
		return False


@register.filter(name = 'take_test_key')
def take_test_key(module_name, user):
    test_result = 'FAIL'
    tests = Tests.objects.filter(module_name = module_name, test_type = 'I')
    for idx,test in enumerate(tests):
                    # print user.email
                    can_attempt = is_user_take_test(test, user.email)
                    #print '................'+str(can_attempt)
                    #print idx
                    if can_attempt[1]:
                            if can_attempt[0] == 'PASS':
                                    test_result = 'PASS'
                                    if idx < 2:
                                         continue
                                    else:
                                         return [None, test_result, idx]
                            else:
                                  return [test.schedule_key, test_result, idx+1]
                    elif idx == 2:
                            #print 'End condition'
                            return [None, test_result, idx]
					
			

@register.filter(name='get_all_inline_test')
def get_all_inline_test(course_module_name, course):
	'''Get all inline for a module and course ...... '''
	try:
			tests = Tests.objects.filter(course = course, module_name = course_module_name, test_type = 'I')
			return tests
	except Exception as e:
			print e.args
			return None


@register.filter(name='check_for_max_marks')
def check_for_max_marks(inline_tests_list, user):
	'''Check for maximum marks of user in INLINE test'''
	try:
		taken_test_list = []
		# print [i.schedule_key for i in inline_tests_list]
		assregusers = []
		asm_reg_user = None
		for test in inline_tests_list:
			asm_reg_user = AssesmentRegisterdUser.objects.filter(test = test, schedule_key= test.schedule_key, student = user).exclude(result_status = 'WAITING')
			# print test.id,asm_reg_user
			if asm_reg_user:
				taken_test_list.append(test) 
				assregusers.append(asm_reg_user[0])
		assert len(assregusers) > 0,'Assert Error: Not have a len(assregusers) > 0 with this Test'
		#print asm_reg_user[0].id
		userresults = [ UserResult.objects.get(assesmentRegisterdUser = asreguser) for asreguser in assregusers ]
		# print userresults
		max_marks_schedule_key = -1
		max_marks_userresult = None
		for userresult in userresults:
			marks = float(userresult.marks_scored)/float(userresult.max_marks)
			if marks > max_marks_schedule_key:
				max_marks_schedule_key = marks
				max_marks_userresult = userresult
				
		# print max_marks_userresult
		# print [i.schedule_key for i in taken_test_list]
		return max_marks_userresult.assesmentRegisterdUser.schedule_key
	except Exception as e:
		print e.args
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
		print e.args
		return False
