from django.db import models
from django.forms import ModelForm
from course_mang.models import CourseDetail
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _




'''
Rating model & manager
'''
class RatingManager(models.Manager):
    def list_all_reviews(self, course):
        """ Return a list of all ratings/reviews made"""
        qs = Rating.objects.filter(course=course).all()
        return qs

    def total_reviews(self,course):
        return len(Rating.objects.filter(course=course).all())

    def is_review_posted(self,course,user):
        if Rating.objects.filter(course=course,user=user).count() != 0:
            return True
        return False

    def post_review(self, user, course, ratings, content):
        review_created = Rating.objects.create(user=user, course=course, review_text=content,ratings=ratings)
        return review_created

    def remove_review(self, user, course):
        try:
            review = Rating.objects.get(user=user, course=course)
            review.delete()
            return True
        except Rating.DoesNotExist:
            return False


'''
Model for Rating/Review section
'''
class Rating(models.Model):
    user = models.ForeignKey(User)
    course = models.ForeignKey(CourseDetail)
    ratings = models.IntegerField(default=0)
    max_allow_rating = models.IntegerField(default=5)
    review_text = models.CharField(max_length=150,default='Must for a beginner.Very good course!')
    added_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    objects = RatingManager()

    def __unicode__(self):
        return unicode('User rated course %s as %s' % (self.course.id, self.ratings))

    class Meta:
        verbose_name = _('Rating')
        ordering = ['-updated_date']

    def save(self, *args, **kwargs):
        super(Rating, self).save(*args, **kwargs)



class RatingModel(ModelForm):
    class Meta:
        model = Rating
        fields = '__all__'

