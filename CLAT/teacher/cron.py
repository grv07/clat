import kronos
from CLAT.services import cron_engine
# from CLAT.services.assesment_engine import test_finish_mail
# from assesment_engine.models import UserResult, AssesmentRegisterdUser
# from course_test_handling.models import Tests
# from django.contrib.auth.models import User
# from student.models import Student
# from datetime import datetime
# import pytz
# from CLAT.services.mail_handling import send_mail
# from course_mang.utilities import LOGIN_REMINDER, DEACTIVATE_REMINDER

'''A cron job function for sql edxlms  backup '''
@kronos.register('*/120 * * * *')
def create_or_update_the_sql_dump():
	cron_engine.create_or_update_the_sql_dump()


'''A cron job function for send a mail after user just graded'''
# @kronos.register('*/120 * * * *')
# def send_graded_mail():
# 	# Send a mail after test graded
# 	cron_engine.send_graded_mail()


'''
Reminder for login - every day at 3:00 AM
'''
@kronos.register('* * * * *')
def login_reminder():
	cron_engine.login_reminder()


'''
Reminder for deactivation - after 6 days at 3:00 AM
'''
@kronos.register('0 3 6 * *')
def deactivation_reminder():
	cron_engine.deactivation_reminder()


'''
Reminder for course time over in 10 days- after 7 days at 11:00 PM
'''
# @kronos.register('* * * * *')
@kronos.register('0 3 7 * *')
def course_time_over():
	'''In case learner does not visit the site and the over-all time is getting over '''
	cron_engine.all_time_getting_over()





