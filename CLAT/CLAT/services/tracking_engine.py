from tracker.models import StudentTracker,Progress
from course_mang.models import CourseDetail,CourseWeek
from student.models import EnrolledCourses, UserCourseProgress
import datetime
import uuid
from course_mang.utilities import check_progress_time
from CLAT.services.constants import PROGRESS_STATUSES, ACCESS_STATUSES, ROOT_PATH_FOR_VIDEOS, COURSE_VIDEO_INITIAL_PATH

import logging
logger = logging.getLogger(__name__)


'''Call to save user tracking'''
def start_tracking(user, request_url, total_seconds):
	# To get diff. between start and end time in secunds
	# import datetime
	# stu_tracker = None
	# end_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	# total_diff = time_diff(total_seconds, end_time)
	# print total_diff

    # Update via ajax call's
	total_diff = total_seconds

	data_dict = fetch_url_data(request_url)
	course_uuid_key = data_dict.get('course_uuid_key',None)
	module_uuid_key = data_dict.get('module_uuid_key',None)
	try:
		logger.info('START-TRACKING: under tracking .......')
		if course_uuid_key:
			co_details = CourseDetail.objects.get(course_uuid = course_uuid_key)
		if module_uuid_key:
			co_module = CourseWeek.objects.get(week_uuid = module_uuid_key,week_module_name=data_dict.get('module_name',None))
		try:
		   g_stu_tracker,c_stu_tracker = StudentTracker.objects.get_or_create(student = user, module_name = data_dict.get('module_name', None), defaults={'uuid_key':uuid.uuid4(), 'module':co_module})
		   progress = Progress.objects.get(tracker = g_stu_tracker)
		except Exception as e:
		   print e.args
		   logger.info('START-TRACKING: '+str(e.args))
		   progress = None

		if progress:
			progress.time_progress += int(total_diff)
			progress.save()
		   # Progress.objects.update_or_create(tracker=g_stu_tracker,defaults={'uuid_key':uuid.uuid4(),'time_progress':total
		else:
			progress = Progress.objects.create(tracker = g_stu_tracker, uuid_key = uuid.uuid4(), time_progress = int(total_diff))


		enrollcourse = EnrolledCourses.objects.get(user = user, course = co_details)	
		assert enrollcourse,'AssertError: Not enrolled'  
		# A nested function for call two time in same block. H.A.N.D
		def get_user_progress(course_week, enrolled_courses):
			return UserCourseProgress.objects.get(course_week = course_week, enrolled_courses = enrolled_courses)
		# Hello self this code is for update UserCourseProgress if prev. module is completed. H.A.N.D
		try:
			userprogress = get_user_progress(course_week = co_module, enrolled_courses = enrollcourse)
			_time = int(check_progress_time(progress.time_progress))
			if _time >= 100:
				userprogress.progress_status = PROGRESS_STATUSES[2]
				userprogress.save()
				next_module = CourseWeek.objects.get(course = co_details, module_number = int(co_module.module_number)+1)
				userprogress = get_user_progress(course_week = next_module, enrolled_courses = enrollcourse)
				userprogress.access_status = ACCESS_STATUSES[0]
				userprogress.save()

			else:
				# userprogress.progress_status = 'UNDER_PROCESS'
				userprogress.save()
			enrollcourse.updated_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")	
			enrollcourse.save()
		except Exception as e:
			logger.info('START-TRACKING: '+str(e.args))
			print "Can't change the progress status"

	except Exception as e:
		logger.info('START-TRACKING: '+str(e.args))
		return None


# '''get time diff b/w two dates in sec. '''
# def time_diff(start_time,end_time):
# 	start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
# 	end_time = datetime.datetime.strptime(str(end_time), "%Y-%m-%d %H:%M:%S")
# 	return (end_time-start_time).total_seconds()


'''Helper: Fetch data from url like course_uuid_key, module_uuid_key, module_name, video_name >> return data-dict'''
def fetch_url_data(url):
	s = url.split(ROOT_PATH_FOR_VIDEOS + COURSE_VIDEO_INITIAL_PATH[1] + '/')[1].strip('/').split('/')
	if len(s) > 4:
		import urllib2
		data = {}
		data['course_uuid_key'] = urllib2.unquote(s[0])
		data['module_uuid_key'] = urllib2.unquote(s[1])
		data['module_name'] = urllib2.unquote(s[2])
		data['video_name'] = urllib2.unquote(s[3])
		return data
	   
# fetch_url_data('dddddddddddd/video/CLAT_videos/media/test/video/articulate/e0528222-6c11-11e5-a6e9-0025ab72e38b/604857c0-6e4e-11e5-9925-0025ab72e38b/hello%20test%20module/NABH_10_Mod1_SP01_EVI/story.html/')
