from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from course_mang import utilities
from course_mang.models import CourseDetail
from course_test_handling.models import Tests


'''
AssesmentRegisterdUser model & manager
'''
class AssesmentRegisterManger(models.Manager):

	def initiate(self, student, course, schedule_key, student_email, registrationStatus_status, test):
		try:
			assment_reg_user = AssesmentRegisterdUser.objects.get(
				student = student, course = course, schedule_key = schedule_key, test = test)
		except Exception as e:
			print e.args
			assment_reg_user = None
		if not assment_reg_user:
			student_registered = AssesmentRegisterdUser.objects.create(
				student = student, course = course, schedule_key = schedule_key, student_email = student_email, registrationStatus_status = registrationStatus_status, test = test)
			return student_registered
		else:
			print 'object EXIST'
			return assment_reg_user

'''
Table for storing test related details
'''
class AssesmentRegisterdUser(models.Model):
	student = models.ForeignKey(User)
	course = models.ForeignKey(CourseDetail)
	test = models.ForeignKey(Tests, null=True)
	test_status = models.CharField(max_length = 10, default = 'NA')

	student_email = models.EmailField(unique = False)
	registrationStatus_status = models.TextField(max_length = 50)
	schedule_key = models.CharField(max_length = 100)
	assessment_name = models.CharField(max_length = 100, default = 'NA')
	result_status = models.CharField(max_length=10, default = 'WAITING')
	candidate_instance_id = models.IntegerField(default='111111')
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
	assesmentRegisterdUser = models.OneToOneField(AssesmentRegisterdUser)
	percentile = models.FloatField()
	max_marks = models.FloatField()
	marks_scored = models.FloatField()
	finish_mode = models.CharField(max_length=100)
	
	added_date = models.DateTimeField(auto_now_add=True)
	updated_date = models.DateTimeField(auto_now=True)


'''Save total percentage marks of AssesmentRegisterdUser'''
class TestMarks(models.Model):
	assesmentRegisterdUser = models.ForeignKey(AssesmentRegisterdUser)
	quiz_marks = models.FloatField()
	total_marks = models.FloatField()
	test_type = models.CharField(
		max_length=40, choices=utilities.ASSESMENT_TEST_CHOICE, default='NOT Avail')


'''
AssesmentRegisterdUser model & manager
'''
class TestStatusManger(models.Manager):

	def create_test_status_obj(self, dict_obj, assesmentRegisterdUser):
		save_data = {}
		save_data['assesmentRegisterdUser'] = assesmentRegisterdUser
		save_data['status'] = dict_obj['status']
		save_data['htmlReport'] = dict_obj['htmlReport']
		save_data['startTime'] = dict_obj['startTime']
		save_data['endTime'] = dict_obj['endTime']
		save_data['completionMode'] = dict_obj['completionMode']
		save_data['pdfReport'] = dict_obj['pdfReport']
		# save_data['email'] = dict_obj['email']
		# print type(save_data['totalCorrectAnswers'])

		teststatus_saved = TestStatus(**save_data)
		teststatus_saved.save()
		return teststatus_saved


class TestStatus(models.Model):
	assesmentRegisterdUser = models.OneToOneField(AssesmentRegisterdUser)
	status = models.TextField(max_length=200)
	htmlReport = models.URLField(max_length=500)
	startTime = models.TextField(max_length=100)
	endTime = models.TextField(max_length=100)
	completionMode = models.TextField(max_length=200)
	pdfReport = models.URLField(max_length=500)

	added_date = models.DateTimeField(auto_now_add=True)
	updated_date = models.DateTimeField(auto_now=True)

	objects = TestStatusManger()

	class Meta:
		verbose_name = _('Test Status')
		ordering = ['startTime']

	def __unicode__(self):
		return "attemptTest " + unicode(self.id)

'''
AssesmentRegisterdUser model & manager
'''


class AssesmentResultManger(models.Manager):

	def create_test_result_obj(self, dict_obj, testStatus):
		save_data = {}
		save_data['testStatus'] = testStatus
		save_data['totalCorrectAnswers'] = dict_obj['totalCorrectAnswers']
		save_data['totalQuestion'] = dict_obj['totalQuestion']
		save_data['totalMarks'] = dict_obj['totalMarks']
		save_data['attemptTime'] = dict_obj['attemptTime']
		save_data['analysis'] = dict_obj['analysis']
		save_data['totalUnAnswered'] = dict_obj['totalUnAnswered']
		save_data['percentile'] = dict_obj['percentile']
		save_data['maxMarks'] = dict_obj['maxMarks']

		comment_created = Result(**save_data)
		# defaults_dict = {'registrationStatus_status':save_data}
		comment_created.save()

		return comment_created


class Result(models.Model):
	testStatus = models.OneToOneField(TestStatus)
	totalCorrectAnswers = models.FloatField()
	totalQuestion = models.FloatField()
	totalMarks = models.FloatField()
	attemptTime = models.FloatField()
	analysis = models.TextField(max_length=200, null=True)
	totalUnAnswered = models.FloatField()
	percentile = models.FloatField()
	maxMarks = models.FloatField()

	added_date = models.DateTimeField(auto_now_add=True)
	updated_date = models.DateTimeField(auto_now=True)

	objects = AssesmentResultManger()

	class Meta:
		verbose_name = _('Attemt Test')
		ordering = ['updated_date']

	def __unicode__(self):
		return "Result " + unicode(self.id)


class SectionMarks(models.Model):
	result = models.ForeignKey(Result)
	totalCorrectAnswers = models.FloatField()
	skillName = models.TextField(max_length=200)
	totalMarks = models.FloatField()
	totalQuestion = models.FloatField()
	timeTaken = models.FloatField()
	totalUnAnswered = models.FloatField()
	maxMarks = models.FloatField()
	questions = models.TextField(max_length=200, null=True)

	added_date = models.DateTimeField(auto_now_add=True)
	updated_date = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = _('Section Marks')
		ordering = ['updated_date']

	def __unicode__(self):
		return "SectionMarks " + unicode(self.skillName)


# Create your models here.
