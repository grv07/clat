from user_login.tasks import send_mail
from course_mang.utilities import TEST_FINISH_MAIL_HTML

def test_finish_mail(to_email, full_name, module_name, pdf_link, status, marks, msg):
	#print TEST_FINISH_MAIL_HTML.format(full_name = full_name, module_name = module_name, pdf_link = pdf_link)
	send_mail.delay(html_part = TEST_FINISH_MAIL_HTML.format(full_name = full_name.capitalize(), module_name = module_name, pdf_link = pdf_link, status = status, \
			scored = marks[1], total = marks[0], percentage = marks[2], msg = msg), to = to_email, subject = 'Congrats for completing the test')
	print 'Mail sent on finish test'
	
