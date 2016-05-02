from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from student.models import EnrolledCourses
from course_test_handling.models import Tests


'''
AssesmentRegisterdUser model & manager
'''
class AssesmentRegisterManger(models.Manager):

	def initiate(self, student, enr_course, schedule_key, student_email, registrationStatus_status, test, remaning_attempts):
		try:
			assment_reg_user = AssesmentRegisterdUser.objects.get(
				student = student, enr_course = enr_course, schedule_key = schedule_key, test = test)
		except Exception as e:
			print e.args
			assment_reg_user = None
		if not assment_reg_user:
			student_registered = AssesmentRegisterdUser.objects.create(
				student = student, enr_course = enr_course, schedule_key = schedule_key, remaning_attempts = remaning_attempts, student_email = student_email, registrationStatus_status = registrationStatus_status, test = test)
			return student_registered
		else:
			print 'object EXIST'
			return assment_reg_user

'''
Table for storing test related details
'''
class AssesmentRegisterdUser(models.Model):
	student = models.ForeignKey(User)
	enr_course = models.ForeignKey(EnrolledCourses)
	test = models.ForeignKey(Tests, null=True)

	test_status = models.CharField(max_length = 10, default = 'NA')

	student_email = models.EmailField(unique = False)
	registrationStatus_status = models.TextField(max_length = 50)
	schedule_key = models.CharField(max_length = 100)
	assessment_name = models.CharField(max_length = 100, default = 'NA')
	result_status = models.CharField(max_length=10, default = 'WAITING')

	remaning_attempts = models.IntegerField(default='0')

	finish_mail = models.BooleanField(default = False)
	
	added_date = models.DateTimeField(auto_now_add = True)
	updated_date = models.DateTimeField(auto_now = True)

	objects = AssesmentRegisterManger()

	class Meta:
		verbose_name = _('Assesment Registerd User')
		ordering = ['updated_date']

	def __unicode__(self):
		return "RegisterdUser  " + unicode(self.student.username)


'''Save total percentage marks of AssesmentRegisterdUser - used in displaying test progress'''
class UserResult(models.Model):
	assesmentRegisterdUser = models.ForeignKey(AssesmentRegisterdUser)
	percentile = models.FloatField(default=0)
	attempt_no = models.IntegerField(default=0)
	result_status = models.CharField(max_length=10, default = 'WAITING')
	candidate_instance_id = models.IntegerField(default='111111')

	max_marks = models.FloatField()
	marks_scored = models.FloatField()
	
	finish_mode = models.CharField(max_length=100)
	report_link = models.CharField(max_length=200)
	
	added_date = models.DateTimeField(auto_now_add=True)
	updated_date = models.DateTimeField(auto_now=True)


# Create your models here.
