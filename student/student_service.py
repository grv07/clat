from CLAT.services.constants import ROOT_PATH_FOR_VIDEOS, DEFAULT_PROFILE_IMAGE

import json, requests, logging

from CLAT.settings import QNA_PATH

logger = logging.getLogger(__name__)

'''Func. call when try to update user profile'''
def update_user_profile(post_req_data,user):
	try:
		from user_login.models import City
		address = user.address
		city = City.objects.get(city_name = post_req_data.get('city'), city_state = post_req_data.get('state'))

		address.country = post_req_data.get('country')
		address.street1 = post_req_data.get('street1')
		address.street2 = post_req_data.get('street2')
		address.pincode = post_req_data.get('pincode')
		address.city_obj = city
		address.save()

		user.address = address
		user.gender = post_req_data.get('gender')
		user.higher_education = post_req_data.get('higher_education')
		user.full_name = post_req_data.get('full_name')
		user.phone_number = post_req_data.get('phone_number')
		user.fblink = post_req_data.get('fblink')
		user.glink = post_req_data.get('glink')
		p_date = post_req_data.get('d_o_b')
		if p_date:
			import datetime
			d_o_b = datetime.datetime.strptime(p_date, '%m/%d/%Y').date()
			user.d_o_b = d_o_b
		else:
			logger.error('under student.student_service.update_user_profile d_o_b error. UID-'+str(user.id))
			pass
		user.save()
		return user
	except Exception as e:
		logger.error('under student.student_service.update_user_profile '+str(e.args)+' UID-'+str(user.id))
		return None

def update_thumbnail(user,picture_name = None):
	try:
		import os
		from student.models import ProfilePicture

		profile_picture_obj = ProfilePicture.objects.get_obj(user=user)
		if profile_picture_obj.picture != DEFAULT_PROFILE_IMAGE:
			os.remove(ROOT_PATH_FOR_VIDEOS + str(profile_picture_obj.picture))
		if picture_name:
		   profile_picture_obj.picture = picture_name
		else:
		   profile_picture_obj.picture = DEFAULT_PROFILE_IMAGE
		
		profile_picture_obj.save()
		return profile_picture_obj
	except Exception as e:
		logger.error('under student.student_service.update_thumbnail '+str(e.args)+' UID-'+str(user.id))
		return None

'''Create a POST call to get users bookmark'''
def get_users_bookmark(username, email):
	try:
		d = requests.post(QNA_PATH+'get/bookmarks/', data = {'username':username, 'email':email})
		return json.loads(d.text)
	except Exception as e:
		print e.args
		return None	