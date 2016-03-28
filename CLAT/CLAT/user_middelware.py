import re
from CLAT.services import tracking_engine
import datetime
from django.utils.timezone import now
from django.contrib.auth.models import User
from student.models import Student



class TimeToVideo(object):
	def process_request(self, request):
		return None

	def process_response(self, request, response):
		referer_path = str(request.META.get('HTTP_REFERER',None))
		request_path = str(request.path)		
		match_pattern = r"[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}"
		
		if re.search(match_pattern, request_path) and request_path.__contains__('/lms/media/video/articulate/') and response.status_code == 200:
			if not request.session.get('vide_time',None):
			   request.session['vide_time'] = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
			   # print 'Video request ........'
			   return response
			else:
			   return response
		else:
			# print '************** NOT a video request path .............//////////'
			if request.session.get('vide_time',None): 
			   from CLAT.services import tracking_engine	
			   start_time = request.session['vide_time']
			   if start_time and re.search(match_pattern, referer_path) and referer_path.__contains__('/lms/media/video/articulate/'):
				  tracking_engine.start_tracking(request.user,referer_path,start_time)
				  del request.session['vide_time']  
			return response
		 
''' Save a user(Student) last_login time when user login '''
class SetLastVisitMiddleware(object):
	def process_request(self, request):
		if request.user.is_authenticated():
			# Update last visit time after request finished processing.
			Student.objects.filter(student = request.user).update(last_visit=now())
		return None
