# from django.shortcuts import render
# from django.contrib.auth.models import User
# from course_mang.models import CourseWeek,CourseDetail
# from course_test_handling.models import TestDetails,Test

# import logging
# logger = logging.getLogger(__name__)


 
# def add_test(request,course_uuid):
# 		course = CourseDetail.objects.get(course_uuid = course_uuid)
# 		course_module = CourseWeek.objects.filter(course = course)
# 		if course.duration == 3:
# 			test_data = 3_week_course()
# 		if course.duration == 6:
# 			test_data = 6_week_course()

# 		return render(request, 'teacher/add_test.html', {'data': test_data,'course_module_list':course_module})	 	

# ''' Save a test for a module '''
# def save_test(request,course_uuid,module_uuid):
# 		course = CourseDetail.objects.get(course_uuid = course_uuid)
# 		course_module = CourseWeek.objects.get(module_uuid = module_uuid)
# 		test = Test.objects.get_or_create(defaults={'course':course,'teacher':request.user})
		
# 		if test_type == 'INLINE':
# 			 test_obj_list = TestDetails.objects.filter(test,test_type)
# 			 test_inline_count = len(test_obj_list)
# 			 if test_inline_count >= 3:
# 					for test_obj in test_obj_list:
# 							test_obj.is_full = 'done'
# 							test_obj.save()
# 					print 'Not able to create more test on this course for INLINE'
# 			 else:
# 					 test_obj = TestDetails.objects.create(test,test_type,is_full)
					 
# 		# if test_type == 'MIDTERM':
# 		test_obj = TestDetails.objects.create(teacher,course,test_type,is_full)	   
# # Create your views here.
