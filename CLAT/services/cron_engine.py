from course_test_handling.models import Tests
from django.contrib.auth.models import User
from student.models import Student
from datetime import datetime
import pytz
from user_login.tasks import send_mail, send_bulk_mail
from course_mang.utilities import LOGIN_REMINDER, DEACTIVATE_REMINDER, NO_ACTION_AFTER_REGISTRATION_REMINDER, COURSE_TIME_ABOUT_TO_OVER_MAIL_HTML, COURSE_TIME_OVER_MAIL_HTML
# from assessment_engine import test_finish_mail

from student.models import EnrolledCourses
from datetime import datetime, timedelta
from django.template import Context, loader



def create_or_update_the_sql_dump():
	import os
	from CLAT.settings import BASE_DIR
	os.system('mysqldump -u root -proot edxlms > '+BASE_DIR+'/edxlms_backup.sql')


'''
returns the no.of days user has not logged-in.
'''
def get_last_login_days(stud):
	return abs((datetime.now(pytz.utc) - stud.student.last_login).days)


def login_reminder():
	try:
		for stud in Student.objects.all():
			if stud.student.last_login:
				enrolled_courses_list = EnrolledCourses.objects.all_underprocess_courses(stud.student)
				if enrolled_courses_list:
					last_login_days = get_last_login_days(stud)
					if last_login_days >= 7:
						enrolled_courses = ', '.join([str(enroll_course.course.course_name.capitalize()) for enroll_course in enrolled_courses_list])
						html = LOGIN_REMINDER.format(courses = enrolled_courses, days = last_login_days)
						send_bulk_mail.delay(html, stud.student.email, 'Gentle Reminder for Completing your eQuest Course')
			else:
				if stud.registration_reminder_count < 6:
					html = NO_ACTION_AFTER_REGISTRATION_REMINDER.format(fullname = stud.full_name.capitalize(), link = "http://equest.co.in/account/verification/" + stud.uuid_key )
					stud.registration_reminder_count  = stud.registration_reminder_count + 1
					stud.save()
					send_bulk_mail.delay(html, stud.student.email, 'e-Quest Account no login after registration alert.')
	except Exception as e:
		print e.args


def half_course_over_reminder():
	try:
		for stud in Student.objects.all():
			if stud.student.last_login:
				last_login_days = get_last_login_days(stud)
				enrolled_courses_list = EnrolledCourses.objects.all_underprocess_courses(stud.student)
				for enroll_course in enrolled_courses_list:
					duration = int(enroll_course.course.course_durations)
					remaining_days =  week_time_over(duration, enroll_course.added_date,(duration*7)//2)
					if remaining_days:
						html = COURSE_TIME_ABOUT_TO_OVER_MAIL_HTML.format(login_days = last_login_days , course = enroll_course.course.course_name)
						send_bulk_mail.delay(html, stud.student.email, 'Gentle Reminder for Completing your eQuest Course')
	except Exception as e:
		print e.args



def deactivation_reminder():
	try:
		for stud in Student.objects.all():
			if stud.student.last_login:
				if get_last_login_days(stud) >= 20:
					html = DEACTIVATE_REMINDER % stud.full_name.capitalize()
					send_bulk_mail.delay(html, stud.student.email)
	except Exception as e:
		print e.args


# '''Helper: All students who not login since day(default = 1) '''
# def get_lt_day_visitor(day = 1):
# 	_date_range = datetime.today() - timedelta(days = day)
# 	return Student.objects.filter(last_visit__lte = _date_range)


'''Helper: If course week time getting over '''
def week_time_over(course_durations, enrolled_date, alert_days = 10):
	duration_days = course_durations*7
	
	total_time_since_enr = enrolled_date + timedelta(days =  duration_days)
	
	_diff = datetime.strptime(total_time_since_enr.strftime('%Y-%m-%d'), '%Y-%m-%d') - datetime.strptime(datetime.today().strftime('%Y-%m-%d'), '%Y-%m-%d')
	
	if _diff.days <= alert_days:
		return _diff.days
	return False


''' In case learner does not visit the site and the over-all time is over '''
def all_time_over(days = 1/4):
	try:
		for stud in Student.objects.all():
			for enr in EnrolledCourses.objects.all_underprocess_courses(stud.student):
				duration = int(enr.course.course_durations)
				_diff_days = week_time_over(duration, enr.added_date, duration)
				if _diff_days:
					html = COURSE_TIME_OVER_MAIL_HTML.format(course = enr.course.course_name.capitalize())
					send_bulk_mail.delay(html, enr.user.email, 'Please register for taking the eQuest course')
	except Exception as e:
		#f.write(str(e.args)+'\n')
		print e.args


''' Mail for sending the course details after enrolling in a course '''
def enroll_success(enrolled, txnid, total_modules):
	try:
		data = { 'enrolled': enrolled, 'total_modules': total_modules,'txnid': txnid }
		template = loader.get_template('enroll_success.html')
		context = Context(data)
		html = template.render(context)
		send_mail(html, enrolled.user.email.replace(' ','+'), subject='Congratulatory Message on Successfully getting enrolled')
		return True
	except Exception as e:
		print e.args
		return False


