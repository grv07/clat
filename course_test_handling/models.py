from django.db import models
from course_mang import utilities
from django.contrib.auth.models import User
from django.forms import ModelForm
from course_mang.models import CourseDetail


''' A table for all types of test -
    I - Inline
    M - Mid Term
    E - End Term
'''
class Tests(models.Model):

    course = models.ForeignKey(CourseDetail, related_name = 'tests_for_course')
    schedule_key = models.CharField(max_length = 10, unique = True)
    module_name  = models.CharField(max_length = 100)
    test_type = models.CharField(max_length = 1)
    test_number = models.IntegerField(default = 0)

    added_date = models.DateTimeField(auto_now_add = True)
    updated_date = models.DateTimeField(auto_now = True)

class Testform(ModelForm):
    class Meta:
        model = Tests
        fields = '__all__'       


# '''
# Model for Course InlineTest section
# '''
# class InlineTest(models.Model):
#     module_name  = models.CharField(max_length=100)   
#     added_date = models.DateTimeField(auto_now_add = True)
#     updated_date = models.DateTimeField(auto_now = True)

#     def __unicode__(self):
#         return unicode('Course  %s InlineTest' % self.id)

#     def save(self, *args, **kwargs):
#         super(InlineTest, self).save(*args, **kwargs)


# class InlineTestModel(ModelForm):
#     class Meta:
#         model = InlineTest
#         fields = '__all__'        


# '''
# Model for Course MidTermTest section
# '''
# class CaseStudyTest(Test):
#     module_name  = models.CharField(max_length=100,unique=True)
#     added_date = models.DateTimeField(auto_now_add = True)
#     updated_date = models.DateTimeField(auto_now = True)

#     def __unicode__(self):
#         return unicode('Course  %s CaseStudyTest' % self.id)

#     class Meta:
#         ordering = ['-updated_date']

#     def save(self, *args, **kwargs):
#         super(CaseStudyTest, self).save(*args, **kwargs)


# class CaseStudyTestModel(ModelForm):
#     class Meta:
#         model = CaseStudyTest
#         fields = '__all__'



# '''
# Model for Course MidTermTest section
# '''
# class MidTermTest(Test):
#     module_name  = models.CharField(max_length=100)
#     added_date = models.DateTimeField(auto_now_add = True)
#     updated_date = models.DateTimeField(auto_now = True)

#     def __unicode__(self):
#         return unicode('Course  %s MidTermTest' % self.id)

#     class Meta:
#         ordering = ['-updated_date']

#     def save(self, *args, **kwargs):
#         super(MidTermTest, self).save(*args, **kwargs)


# class MidTermTestModel(ModelForm):
#     class Meta:
#         model = MidTermTest
#         fields = '__all__' 


# '''
# Model for Course QuizUrls section
# '''
# class QuizUrls(Test):
#     inline = models.ForeignKey(InlineTest,related_name='inlinequiz_quizurls')
#     is_full = models.CharField(max_length=40, choices=utilities.STATUS_CHOICES,default = 'PENDING')
#     quiz_no = models.IntegerField(default=1,unique=True)
#     added_date = models.DateTimeField(auto_now_add = True)
#     updated_date = models.DateTimeField(auto_now = True)

#     def save(self, *args, **kwargs):
#         super(QuizUrls, self).save(*args, **kwargs)


# class TestDetailsModel(ModelForm):
#     class Meta:
#         model = QuizUrls
#         fields = '__all__'        
