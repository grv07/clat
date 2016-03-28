from models import TestStatus,Result,AssesmentRegisterdUser,SectionMarks
from django.contrib.auth.models import User
from student.models import Student

def update_assesment_test_db(out_json):
	pass
	# registration = out_json['registration']
	# testStatus = out_json['testStatus']
	# print testStatus 
	# if testStatus:
	# 	# print '---------->>>>>>>>>>>'+str(testStatus['result'])
	#     try:
	#        test_status_obj = None
	#        student = Student.objects.get(email = registration['Email Address'],username = registration['First Name'])
	#        registered_user = AssesmentRegisterdUser.objects.get(student_email = registration['Email Address'],student = student)
	#        print 'get register user'
	#        if registered_user:
	#            test_status_obj = TestStatus.objects.get(assesmentRegisterdUser = registered_user) 
	#        	   print 'aftre get'
	#        	   print test_status_obj
	#        	   if not  test_status_obj: 
	# 	           test_status_obj = TestStatus.objects.create_test_status_obj(testStatus,registered_user)
	# 	           print '............'
	#            if test_status_obj:
	#               result = Result.objects.create_test_result_obj(testStatus['result'],test_status_obj)
	#        	      # SectionMarks.objects.save() 
	#     except Exception as e:
	#        print e.args
