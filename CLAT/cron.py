import kronos
from .services import cron_engine

# '''A cron job function for sql edxlms  backup '''
# @kronos.register('*/120 * * * *')
# def create_or_update_the_sql_dump():
# 	cron_engine.create_or_update_the_sql_dump()


# '''
# Reminder for login - every day at 3:00 AM
# '''
@kronos.register('* 3 * * *')
def login_reminder():
 	cron_engine.login_reminder()


# '''
# Reminder for deactivation - after 6 days at 3:00 
#'''

'''
Reminder for course time over in 10 days- after 7 days at 11:00 PM
'''
@kronos.register('* 1 7 * *')
def course_time_over():
	'''In case learner does not visit the site and the over-all time is over '''
	cron_engine.all_time_over()


# '''
# Reminder for half time over for course completion - after 6 days at 1:00 AM
# '''
# @kronos.register('* 1 6 * *')
# def half_course_over_reminder():
# 	'''In case learner does not visit the site and the half-time is getting over '''
# 	cron_engine.half_course_over_reminder()




