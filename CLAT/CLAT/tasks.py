# '''
# This file contains methods for sending mails using celery connection.
# '''
# from celery import shared_task
# from django.contrib.auth.models import User
# # import logging
# # logger = logging.getLogger(__name__)

# @shared_task
# def send_mail(html_part, to, subject = 'eQUEST account registration email'):
# 	if html_part and to:
# 		try:
# 			import smtplib
# 			from email.MIMEMultipart import MIMEMultipart
# 			from email.MIMEText import MIMEText
# 			server = smtplib.SMTP('smtp.gmail.com', 587, timeout=60)

# 			#Next, log in to the server
# 			server.ehlo()
# 			server.starttls()
# 			server.login("gaurav@madmachines.io", "@8447mm8447@")

# 			msg = MIMEMultipart('alternative')
# 			msg['Subject'] = subject
# 			msg['From'] = 'gaurav@madmachines.io'
# 			msg['To'] = str(to)
# 			if html_part:
# 			   part2 = MIMEText(html_part, 'html')
# 			   msg.attach(part2)
# 			BODY = msg.as_string()
# 			# msg = "\nHello!" # The /n separates the message from the headers
# 			print server.sendmail("gaurav@madmachines.io", str(to), BODY)
# 			server.quit()
# 		except Exception as e:
# 			# logger.error('under CLAT.tasks.send_mail '+str(e.args))
# 			print '/Exception in sendng email'
# 			# send_mail.retry(countdown = 2, exc = e, max_retries = 2)
# 	else:
# 		print 'E-Mail Body not define'


# @shared_task
# def send_bulk_mail(html_part, to, subject = 'eQUEST account registration email'):
# 	import mandrill
# 	if html_part and to:
# 		try:
# 			mandrill_client = mandrill.Mandrill('zY92ecqAVEhLSOP9k4dJJw')
# 			message = {
# 				# 'attachments': [{'content': 'ZXhhbXBsZSBmaWxl',
# 				#                  'name': 'myfile.txt',
# 				#                  'type': 'text/plain'}],
# 				'auto_html': None,
# 				'auto_text': None,
# 				# 'bcc_address': 'message.bcc_address@example.com',
# 				'from_email': 'grvtyagi22@gmail.com',
# 				'from_name': 'eQUEST',
# 				'headers': {'Reply-To': 'equest_support@email.com'},
# 				'html': str(html_part),
# 				'important': False,
# 				'inline_css': None,
# 				'merge': True,
# 				'merge_language': 'mailchimp',
# 				'merge_vars': [{'rcpt': 'talktous@equest.co.in',
# 								'vars': [{'content': 'merge2 content', 'name': 'merge2'}]}],
# 				'metadata': {'website': 'www.equest.co'},
# 				'preserve_recipients': None,
# 				'return_path_domain': None,
# 				'signing_domain': None,
# 				'subject': str(subject),
# 				'tags': ['eQUEST message'],
# 				'text': 'Example text content',
# 				'to': [{'email': str(to),
# 						'name': 'Recipient Name',
# 						'type': 'to'}],
# 				# 'track_clicks': None,
# 				# 'track_opens': None,
# 				# 'tracking_domain': None,
# 				'url_strip_qs': None,
# 				'view_content_link': None
# 				}
# 			result = mandrill_client.messages.send(message=message, async=True, ip_pool='Main Pool',
# 												   send_at=None)
# 			print result
# 		except mandrill.Error, e:
# 			# Mandrill errors are thrown as exceptions
# 			print 'A mandrill error occurred: %s - %s' % (e.__class__, e)