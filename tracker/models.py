from django.db import models
from django.contrib.auth.models import User
from course_mang.models import CourseWeek


"""
StudentTracker for tracking user and course modules.
"""
class StudentTracker(models.Model):
    student = models.ForeignKey(User)
    module = models.ForeignKey(CourseWeek)
    uuid_key = models.TextField(max_length = 100)
    module_name = models.TextField(max_length = 100)
    
    added_date = models.DateTimeField(auto_now_add = True)
    updated_date = models.DateTimeField(auto_now = True)


    def __unicode__(self):
        print 'StudentTracker id: '
        return unicode(self.id)


"""
This contains progress info. - time spent (in seconds).
"""
class Progress(models.Model):
    tracker = models.ForeignKey(StudentTracker)
    uuid_key = models.TextField(max_length = 100)  
    time_progress = models.IntegerField()
    # module_progress = models.IntegerField(null=True)
    # total_progress = models.IntegerField()
    
    added_date = models.DateTimeField(auto_now_add = True)
    updated_date = models.DateTimeField(auto_now = True)

    def __unicode__(self):
        print 'Progress id: '
        return unicode(self.id)

