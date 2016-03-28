import string
import random
import urllib2
import urllib
 
''' Use for send a sms to user's mobile ''' 
def sendSMS(phone_number, message):
	request = urllib2.Request("http://www.generatelead.in/api/sendhttp.php?authkey=101399ABRiGsKU55684e346&mobiles="+phone_number+"&message="+message+"&sender=QCIIND&route=4&country=91")
	f = urllib2.urlopen(request)
	return f.read()

''' Take a student and msg content and send it ''' 
def send_otp_msg(student, content):
	if not student.is_verified:
		resp = sendSMS(student.phone_number, content)

		if resp:
		    return {'status':True,'msg':'Otp send successfully.'}
		else:
			return {'status':False,'msg':'Message not send.'}
	else:
		return {'status':False,'msg':'User is verified'}


''' Generate an otp code fro verification take size = int and chars = string return 'string >>'' len(size) '''
def  id_generator(size = 6, chars = string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

# msg = "Hello @__123__@@__123__@, One Time Password (OTP) for your e-Quest account verification is @__123__@. Welcome to India's first e-quality platform."
# sendSMS('8447860079',msg)