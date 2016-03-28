from student.models import Student, EnrolledCourses, UserCourseProgress, StudentInterests
from django.contrib.auth.models import User
from course_mang.models import CourseDetail, CourseWeek


def update_for_enroll_users():
	users = User.objects.all()
	course = None
	# courses = CourseDetail.objects.all()
	for user in users:
		# all_enroll_student = EnrolledCourses.objects.list_all_students_enrolled(course)
		all_enroll_course = EnrolledCourses.objects.all_enrolled_by_student(user)
		print all_enroll_course
		if all_enroll_course:
			for enr_course in all_enroll_course:
					course = enr_course.course
					print course
					try:
						all_weeks = course.course_week.all().order_by('module_number')
						print all_weeks
						for week in all_weeks:
							print 'under create or get'
							user_cour_progress,created = UserCourseProgress.objects.get_or_create(course_week = week, enrolled_courses = enr_course)
						
						if created:
						   first_module = UserCourseProgress.objects.get(course_week = all_weeks[0], enrolled_courses = enr_course)
						else:
						   first_module = None
						   
						if first_module:
							first_module.access_status = 'OPEN'
							first_module.save()
						else:
							print 'Unable to open/find first module'
					except Exception as e:
						print e.args
						return HttpResponse('error while enrolling')
					
					print 'UPDATe>>: >>>>>>>>> course enroll now'
					
					if StudentInterests.objects.filter(user = user).count() == 1:
						interests_obj = StudentInterests.objects.get(user = user)
						if course.course_sectors_and_associates not in interests_obj.category:
							interests_obj.category = str(interests_obj.category)+";"+str(course.course_sectors_and_associates)
							interests_obj.save()
						print 'DONE ............//'
					else:
						interest_added = StudentInterests.objects.create(user = user, category = course.course_sectors_and_associates)
						# print interest_added
					print 'UPDATe>>: >>>>>>>>> student interest also now'
					# return HttpResponseRedirect('/dashboard/')
				# else:
					# messages.error(request,'Unable to enroll in '+course.course_name+' .')
					# return HttpResponse('/course/details/'+course_uuid+'/')
			else:
			    print 'not enroll any course yet'		
	# print 'Successfully update all users enroll courses data.'	            
