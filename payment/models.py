from django.db import models
from course_mang.models import CourseDetail
from django.contrib.auth.models import User
from student.models import EnrolledCourses
# Create your models here.
class CoursePayment(models.Model):
    enrolledcourse = models.OneToOneField(EnrolledCourses, related_name='enrolled_course_payment', unique = True)
    txnid = models.CharField(unique = True, max_length = 50)

    added_time = models.DateTimeField(auto_now = True)
    extra_data = models.TextField()

    def __unicode__(self):
        return unicode(self.enrolledcourse.user.username + ' has paid for ' + self.enrolledcourse.course.course_name)


class FailedPayment(models.Model):
    course = models.ForeignKey(CourseDetail)
    user = models.ForeignKey(User)
    txnid = models.CharField(unique = True, max_length = 50)
    reason = models.TextField()
    added_time = models.DateTimeField(auto_now = True)
    extra_data = models.TextField()

    def __unicode__(self):
        return unicode(self.user.username + ' got an error while paying for ' + self.course.course_name)
