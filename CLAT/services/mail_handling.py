# # import mandrill
# from student.models import Student
# from django.contrib.auth.models import User


# # def verify_account(student):
# #     import uuid

# #     if not student.is_verified:
# #         student.is_verified = True
# #         student.uuid_key = 'eq' + str(uuid.uuid4().fields[-1])[:8]
# #         student.save()
# #         return True
# #     else:
# #         return False        

    

# # def get_student_from_user(user):
# #     try:
# #         student = Student.objects.get(student=user.id)
# #         if student:
# #             return student
# #         else:
# #             return None
# #     except Exception as e:
# #         print e.args
# #         return None

# # ''' Check if user is verified or not '''
# # def is_verified_user(user):
# #     try:
# #         student = get_student_from_user(user)
# #         if student:
# #             return student.is_verified
# #         else:
# #             return False
# #     except Exception as e:
# #         print e.args
# #         return None

# # '''Call when user want to send verification mail '''
# # def verfiy_acc_mail():
# #     pass

# # '''Call when user want to send verification mail by default its a welcome mail to user if << msg is None >>'''
# # def verification_mail(user, domain,msg=None,**kwargs):
# #     # print kwargs 
# #     student = User.objects.get(id=user)
# #     if student:
# #         complete_link = "http://" + str(domain) + "/account/verification/" + str(kwargs['uuid_key'])
# #         # print complete_link
# #         if not msg:
# #             # msg = '<p>Please verify your e-quest account <a href="' + complete_link + '"\
# #             #  style= "-webkit-appearance: button;-moz-appearance: button;appearance: button;text-decoration: none;color: blue;">Click Here</a> </p>\
# #             #   </br><p>Your login user name is: <span style="color:red">'+kwargs['student_uname']+'</span></p></br>\
# #             #   <p>Your password is:  <span style="color:red">'+kwargs['student_pass']+'</span>\
# #             #   <p>Your account phone number is:  <span style="color:red">'+kwargs['phone_number']+'</span>\
# #             #   <b>In case if our button link not work please copy and paste in browser tab :<br>'+complete_link+'</b>\
# #             #   </p>'
# #             msg = '<img src="http://Clat.co/static/images/logo.png" alt="Clat logo image not available"><br><br>\
# #                     <h2>Dear '+ str(kwargs['full_name']).capitalize() +',</h2><p></p><h3>Welcome to Clat ( India\'s first Intelligent e-Quality Learning Management System ).</h3>\
# #                     <p><hr></p><h3>Your account details are as follows</h3>\
# #                     <div style="text-align:left;"><h4>Username    :    <span style="color:blue;">'+kwargs['student_uname'] +'</span></h4>\
# #                     <h4>Password    :    <span style="color:blue;">'+ kwargs['student_pass'] +'</span></h4>\
# #                     <h4>Contact Number    :    <span style="color:blue;">'+  kwargs['phone_number'] +'</span></h4></div><hr>\
# #                     <h3>Please visit this url to activate your account\
# #                     <a href="' + complete_link + '"style= "-webkit-appearance: button;-moz-appearance: button;appearance: button;text-decoration: none;color: blue;">Click Here</a></h3>\
# #                     <h3 style="color:red;">NOTE    :    In case if our button link is not working, please copy and paste following link in browser URL</h3>\
# #                     <p>'+ complete_link +'</p>'
# #         send_mail(msg, student.email)
# #     else:
# #         pass



# # def send_mail(html_part, to, subject = 'Clat Account Registration E-Mail'):
# #     if html_part and to:
# #         try:
# #             import smtplib
# #             from email.MIMEMultipart import MIMEMultipart
# #             from email.MIMEText import MIMEText
# #             server = smtplib.SMTP('smtp.gmail.com', 587, timeout=60)

# #             #Next, log in to the server
# #             server.ehlo()
# #             server.starttls()
# #             server.login("gaurav@madmachines.io", "@8447mm8447@")

# #             msg = MIMEMultipart('alternative')
# #             msg['Subject'] = subject
# #             msg['From'] = 'gaurav@madmachines.io'
# #             msg['To'] = str(to)
# #             if False:
# #                part1 = MIMEText(textBody, 'plain')
# #                msg.attach(part1)
# #             if html_part:
# #                part2 = MIMEText(html_part, 'html')
# #                msg.attach(part2)
# #             BODY = msg.as_string()
# #             # msg = "\nHello!" # The /n separates the message from the headers
# #             print server.sendmail("gaurav@madmachines.io", str(to), BODY)
# #             server.quit()
# #         except Exception as e:
# #             print e.args
# #             print '/Exception in sendng email'
# #     else:
# #         print 'E-Mail Body not define'
    # try:
    #     mandrill_client = mandrill.Mandrill('zY92ecqAVEhLSOP9k4dJJw')
    #     message = {
    #         # 'attachments': [{'content': 'ZXhhbXBsZSBmaWxl',
    #         #                  'name': 'myfile.txt',
    #         #                  'type': 'text/plain'}],
    #         'auto_html': None,
    #         'auto_text': None,
    #         # 'bcc_address': 'message.bcc_address@example.com',
    #         'from_email': 'grvtyagi22@gmail.com',
    #         'from_name': 'E-Quest',
    #         'headers': {'Reply-To': 'equest_support@email.com'},
    #         'html': str(html_part),
    #         'important': False,
    #         'inline_css': None,
    #         'merge': True,
    #         'merge_language': 'mailchimp',
    #         'merge_vars': [{'rcpt': 'recipient.email@example.com',
    #                         'vars': [{'content': 'merge2 content', 'name': 'merge2'}]}],
    #         'metadata': {'website': 'www.example.com'},
    #         'preserve_recipients': None,
    #         'return_path_domain': None,
    #         'signing_domain': None,
    #         'subject': 'Verify E-Quest Account',
    #         'tags': ['password-resets'],
    #         'text': 'Example text content',
    #         'to': [{'email': str(to),
    #                 'name': 'Recipient Name',
    #                 'type': 'to'}],
    #         # 'track_clicks': None,
    #         # 'track_opens': None,
    #         # 'tracking_domain': None,
    #         'url_strip_qs': None,
    #         'view_content_link': None
    #         }
    #     result = mandrill_client.messages.send(message=message, async=False, ip_pool='Main Pool',
    #                                            send_at=None)

    #     print result

    # except mandrill.Error, e:
    #     # Mandrill errors are thrown as exceptions
    #     print 'A mandrill error occurred: %s - %s' % (e.__class__, e)
    #     # A mandrill error occurred: <class 'mandrill.InvalidKeyError'> - Invalid API key
    #     # raise