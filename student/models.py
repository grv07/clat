from django.db import models
from django.forms import ModelForm
from user_login.models import Address
from teacher.validators import phone_regex
from django.contrib.auth.models import User
import math
from datetime import datetime
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from PIL import Image as img
from course_mang.models import CourseDetail, CourseWeek
from course_mang import utilities

"""
Student profile table and other info.
"""
class Student(models.Model):
    student = models.OneToOneField(User, related_name='student_profile')
    last_visit = models.DateTimeField(default=timezone.now)

    uuid_key = models.TextField(max_length=100)
    full_name = models.TextField(max_length=100)
    address = models.OneToOneField(Address)
    otp_code = models.TextField(max_length=10,null=True)
    phone_number = models.CharField(validators=[phone_regex],max_length = 10)

    gender = models.CharField(max_length=10, null=True)
    d_o_b = models.DateField(null=True)
    higher_education = models.TextField(max_length = 100,null = True)
    is_verified = models.BooleanField(default=False)
    fblink = models.URLField(default = '')
    glink = models.URLField(default = '')
    i_agree = models.BooleanField(default = False)
    registration_reminder_count = models.IntegerField(default = 0)
    added_date = models.DateTimeField(auto_now_add = True)
    updated_date = models.DateTimeField(auto_now = True)
    

    def __unicode__(self):
        print 'Student id: '
        return unicode(self.id)

class StudentModel(ModelForm):
    class Meta:
        model = Student
        fields = ['gender', 'd_o_b', 'full_name','phone_number','i_agree','higher_education']


'''
EnrolledCourses model & manager
'''
class EnrolledCoursesManager(models.Manager):

    def all_underprocess_courses(self, user):
        """ Return a list of all total courses under-process for user those are not older then"""
        return EnrolledCourses.objects.filter(user = user, is_complete = False)

    def list_all_courses_enrolled(self, user, start = 0, end = 3):
        """ Return a list of all total courses enrolled """
        qs = EnrolledCourses.objects.filter(user = user)[start:end]
        #total_courses_enrolled = [u.course for u in qs]
        return qs

    def list_all_students_enrolled(self, course):
        qs = EnrolledCourses.objects.filter(course = course).all()
        return qs

    def is_student_enrolled(self, user, course):
        try:
            enr_course = EnrolledCourses.objects.get(user = user, course = course)
            return enr_course
        except Exception as e:
            return []

    def all_enrolled_by_student(self, user):
        enr_courses = EnrolledCourses.objects.filter(user = user)
        if enr_courses:
            return enr_courses
        else:
            return []

    def enroll_student(self, user, course, want_notifications = False):
        student_enrolled = EnrolledCourses.objects.create(user = user, course = course, want_notifications = want_notifications)
        return student_enrolled

    def unenroll_student(self, user, course):
        try:
            rel = EnrolledCourses.objects.get(user = user, course = course)
            rel.delete()
            return True
        except EnrolledCourses.DoesNotExist:
            return False

class EnrolledCourses(models.Model):
    """ Model to represent Enrolled Courses Database """
    user = models.ForeignKey(User, related_name = 'student_courses_enrolled')
    course = models.ForeignKey(CourseDetail, related_name = 'course_enrolled_detail')
    want_notifications = models.BooleanField(default = False)
    is_pass = models.BooleanField(default = False)
    is_complete = models.BooleanField(default = False)

    added_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    objects = EnrolledCoursesManager()

    class Meta:
        verbose_name = _('EnrolledCourses Section')
        ordering = ['-updated_date']
        unique_together = ("course", "user",)

    def __unicode__(self):
        return unicode("Course: %s" % (self.course.course_name))

    def save(self, *args, **kwargs):
        super(EnrolledCourses, self).save(*args, **kwargs)



class Certificate(models.Model):
    """ Model to represent Certificate Database """
    uuid_key = models.CharField(max_length = 20)
    enr_course = models.OneToOneField(EnrolledCourses, related_name = 'certified_course_enrolled_detail')
    status = models.CharField(max_length = 40, choices = utilities.CERTIFICATE_CHOICES, default = 'PARTICIPATE')
    max_marks = models.IntegerField(default = 0)
    marks_score = models.IntegerField(default = 0)

    added_date = models.DateTimeField(default = timezone.now)
    updated_date = models.DateTimeField(default = timezone.now)
    
    objects = EnrolledCoursesManager()

    class Meta:
        verbose_name = _('Certificate Section')
        ordering = ['-added_date']

    def __unicode__(self):
        return unicode("Certificate: "+self.uuid_key)

    def save(self, *args, **kwargs):
        super(Certificate, self).save(*args, **kwargs)


'''
User Course Progress - stores permission for access and progress status.
'''
class UserCourseProgress(models.Model):
    course_week = models.ForeignKey(CourseWeek, related_name = 'user_course_progress_week')
    access_status = models.CharField(max_length = 5, choices = utilities.ACCESS_STATUS, default = 'CLOSE')
    progress_status = models.CharField(max_length = 15, choices = utilities.PROGRESS_STATUS, default = 'WAITING')
    enrolled_courses = models.ForeignKey(EnrolledCourses, related_name = 'enroll_user_course_progress')

    added_date = models.DateTimeField(default = timezone.now)
    updated_date = models.DateTimeField(default = timezone.now)

    class Meta:
        verbose_name = _('UserCourseProgress Section')

    def __unicode__(self):
        return unicode("Progress for %s access %s progress %s" % (self.course_week.week_module_name,self.access_status,self.progress_status))

    def save(self, *args, **kwargs):
        super(UserCourseProgress, self).save(*args, **kwargs)



'''
ProfilePictureManger model & manager
'''
class ProfilePictureManger(models.Manager):
    def get_obj(self, user):
        try:
           return ProfilePicture.objects.get(user = user)    
        except Exception as e:
            print e.args
            return None
      
      
'''Profile Picture model'''
class ProfilePicture(models.Model):
    user = models.OneToOneField(User, related_name = "user_profile_picture")
    picture = models.ImageField(upload_to = 'profile_images', blank=True)

    added_date = models.DateTimeField(default = timezone.now)
    updated_date = models.DateTimeField(default = timezone.now)
    
    objects = ProfilePictureManger()

    def __unicode__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        '''
        Resize the image when size it is greater than 200x180 using Python Imaging Library.
        After resizing, save it with super-sampling done using ANTIALIAS filter.
        '''
        if self.picture:
            super(ProfilePicture, self).save()
            present_width = self.picture.width
            present_height = self.picture.height
            max_width = 200
            max_height = 180
            if(present_width>max_width) or (present_height>max_height):
                filename = str(self.picture.path)
                imageObj = img.open(filename)
                ratio = 1
                if(present_width>max_width):
                    ratio = max_width/float(present_width)
                    present_width = max_width
                    present_height = int(math.floor(float(present_height)*ratio))
                if(present_height>max_height):
                    ratio = ratio*(max_height/float(present_height))
                    present_height = max_height
                    present_width = int(math.floor(float(present_height)*ratio))

                imageObj = imageObj.resize((present_width,present_height),img.ANTIALIAS)
                imageObj.save(filename)

"""
Model for student interests. Categories separated by ; .
"""
class StudentInterests(models.Model):
    """ Model to represent Comments Database """
    user = models.OneToOneField(User, related_name = 'student_interests')
    category = models.TextField(max_length = 500, default = '')

    added_date = models.DateTimeField(default = timezone.now)
    updated_date = models.DateTimeField(default = timezone.now)

    class Meta:
        verbose_name = _('StudentInterests Section')
        ordering = ['-added_date']

    def __unicode__(self):
        return unicode("User %s is interested in %s" % (self.user.username, self.category))

    def save(self, *args, **kwargs):
        super(StudentInterests, self).save(*args, **kwargs)
