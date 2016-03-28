from django.db import models
from teacher.models import Teacher
# from course_test_handling.models import InlineTest,MidTermTest
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
import utilities
from PIL import Image as img
import math


'''default model'''
AUTH_USER_MODEL = 'auth.User'

''' Get save directory for particular file at runtime'''
def user_directory_path(instance, filename):
    return '/lms/media{0}{1}'.format(instance.course_demo_file_url, filename)


'''Save details of course creation'''
class CourseDetail(models.Model):
    teacher = models.ForeignKey(Teacher)
    course_uuid = models.CharField(max_length = 200)
    course_name = models.CharField(max_length = 400)

    enroll_start_date = models.DateField(null = True)
    enroll_end_date = models.DateField(null = True)
    can_enroll = models.BooleanField(default = False)

    course_start_date = models.DateField(null = True) 
    course_end_date =  models.DateField(null = True)
    course_start_time = models.TimeField(null = True) 
    course_end_time = models.TimeField(null = True)

    course_durations = models.CharField(max_length = 2)
    
    course_sectors_and_associates = models.CharField(max_length = 100, choices = utilities.SECTORS_ASSOCIATES_CHOICES, default = 'others')
    course_demo_file = models.FileField(upload_to = user_directory_path, default = "utb")
    course_demo_file_url = models.URLField(max_length = 200, default = 'www.example.com')
    course_status = models.CharField(max_length = 40, choices = utilities.STATUS_CHOICES, default = 'PENDING')    
    
    amount = models.IntegerField(default = 0)
    language = models.CharField(max_length = 50, default = 'English')
    level = models.CharField(max_length = 50, default = 'Not-avail')
    effort = models.CharField(max_length = 50, default= 'Not-avail')
    
    added_date = models.DateTimeField(auto_now_add = True)
    updated_date = models.DateTimeField(auto_now = True)

    class Meta:
        ordering = ['-updated_date']

    def __unicode__(self):
        return unicode(self.course_name)

    def save(self, *args, **kwargs):
        super(CourseDetail, self).save()


'''
Course Image Model - related to CourseDetail
'''
class CourseImage(models.Model):
    course = models.OneToOneField(CourseDetail, related_name = "course_image")
    picture = models.ImageField(upload_to = 'course_demo_images', blank = True, default = 'EDX_demo_course_image.jpg')
    added_date = models.DateTimeField(default = timezone.now)
    updated_date = models.DateTimeField(default = timezone.now)    

    def __unicode__(self):
        return self.course.course_name

    def save(self, *args, **kwargs):
        '''
        Resize the image when size it is greater than 200x180 using Python Imaging Library.
        After resizing, save it with super-sampling done using ANTIALIAS filter.
        '''
        if self.picture:
            super(CourseImage, self).save()
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


'''
Course Information Model - related to CourseDetail
'''
class CourseInformation(models.Model):
    course = models.OneToOneField(CourseDetail, related_name='course_information')
    description = models.CharField(max_length=3000)
    short_description = models.CharField(max_length=500)
    objective =  models.CharField(max_length=3000)
    eligibility = models.CharField(max_length=3000)
    crt_benefits = models.CharField(max_length=3000)
    
    added_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    
    class Meta:
        verbose_name = _('Course Information')
        ordering = ['updated_date']

    def __unicode__(self):
        return "Course Information "+unicode(self.course.course_name)

    def save(self, *args, **kwargs):
        super(CourseInformation, self).save(*args, **kwargs)


'''
Course Videos Model - related to CourseDetail
'''
class CourseWeek(models.Model):
    
    course = models.ForeignKey(CourseDetail, related_name = 'course_week')
    week_module_name = models.CharField(max_length = 200, unique = True)
    week_number = models.IntegerField()
    module_number = models.IntegerField(default = 0)

    added_date = models.DateTimeField(auto_now_add = True)
    updated_date = models.DateTimeField(auto_now = True)
    week_uuid =  models.CharField(max_length = 200)
    week_detail = models.CharField(max_length = 900)
    is_available = models.BooleanField(default = True)
   
    class Meta:
        verbose_name = _('Course Week')
        # unique_together = ('course', 'module_number',)
        ordering = ['week_number']

    def __unicode__(self):
        return "Module: "+unicode(self.week_module_name)

    def save(self, *args, **kwargs):
        super(CourseWeek, self).save(*args, **kwargs)


''' Get save directory for particular file at runtime'''
def user_course_video_path(instance, filename):
    return '/lms/media{0}{1}'.format(instance.video_url, filename)


'''
Course Videos Model - related to CourseDetail
'''
class CourseVideos(models.Model):
    course = models.ForeignKey(CourseDetail, related_name = 'course_uploaded_videos')
    week =  models.ForeignKey(CourseWeek, related_name = 'course_week_uploaded_videos')
    video_file = models.FileField(upload_to = user_course_video_path, default = "utb", max_length=1000)
    # video_file_name = models.CharField(max_length = 100)
    # video_url = models.URLField(max_length = 200, default = 'www.example.com')
    module_name = models.CharField(max_length = 200)

    added_date = models.DateTimeField(auto_now_add = True)
    updated_date = models.DateTimeField(auto_now = True)
    video_type = models.CharField(max_length = 40, choices = utilities.TYPE_CHOICES, default = 'MP4')
    
    class Meta:
        verbose_name = _('Course Videos')
        ordering = ['-updated_date']

    def __unicode__(self):
        return unicode(self.module_name)

    def save(self, *args, **kwargs):
        super(CourseVideos, self).save(*args, **kwargs)


'''
Comments model & manager
'''
class CommentsManager(models.Manager):
    def list_all(self, uuid, start=0 , end=5):
        """ Return a list of all comments made , initially according to start-end slicing"""

        qs = Comments.objects.filter(course_uuid = uuid).all()
        comments = [(u.user_id.username, u.comment) for u in qs[start:end]]
        return comments

    def total_comments(self,uuid):
        return len(Comments.objects.filter(course_uuid=uuid).all())

    def post_comment(self, user, uuid, content):

        comment_created = Comments.objects.create(user_id=user, course_uuid=uuid, comment=content)
        return comment_created

    def remove_comment(self, user, uuid, content):

        try:
            rel = Comments.objects.get(user_id=user, course_uuid=uuid, comment=content)
            rel.delete()
            return True
        except Comments.DoesNotExist:
            return False


class Comments(models.Model):
    """ Model to represent Comments Database """
    user_id = models.ForeignKey(AUTH_USER_MODEL, related_name = 'user')
    course_uuid = models.CharField(max_length = 200)
    comment = models.TextField(max_length = 150)
    added_date = models.DateTimeField(default = timezone.now)
    updated_date = models.DateTimeField(default = timezone.now)
    objects = CommentsManager()

    class Meta:
        verbose_name = _('Comments Section')
        ordering = ['-added_date']

    def __unicode__(self):
        return unicode(self.id)

    def save(self, *args, **kwargs):
        super(Comments, self).save(*args, **kwargs)
