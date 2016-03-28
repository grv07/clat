 import kronos

'''A cron job function for sql edxlms  backup '''

@kronos.register('*/1 * * * *')
def course_can_enroll():
	import os
	import datetime
 	from course_mang.models import CourseDetail

	course_list = CourseDetail.objects.filter(can_enroll = True)
	if course_list.count > 0:
		for course in course_list:
			day_diff = (course.enroll_end_date - datetime.date.today()).days
			if day_diff < 0:
				course.can_enroll = False
				course.save()
			else:
			   pass
	else:
	  pass	   	 
