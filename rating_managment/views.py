from django.shortcuts import render, HttpResponse, HttpResponseRedirect
import json
from user_login.templatetags import rating_tags
from rating_managment.models import Rating
from course_mang.models import CourseDetail
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from student.models import EnrolledCourses
from CLAT.services.constants import RATING_INFO

import logging
logger = logging.getLogger(__name__)

def enroll_helper(request):
    return EnrolledCourses.objects.is_student_enrolled(request.user,CourseDetail.objects.get(id=request.POST.get('c_id')))

@login_required
def add_rating_action(request):
    if enroll_helper(request):
        logger.info('rating_managment.add_rating_action >> Student Enroll in course')
        if request.method == 'POST':
            rating_info = RATING_INFO
            rating = int(request.POST.get('rating'))
            review_text= request.POST.get('review_text')
            if 1<=rating<=5 and 10<=len(review_text.replace(' ',''))<=150:
                review_created = Rating.objects.post_review(request.user,CourseDetail.objects.get(id=request.POST.get('c_id')),rating,review_text)
                if review_created:
                    return HttpResponse(json.dumps(True), 'applications/json')
            return HttpResponse(json.dumps(False), 'applications/json')
    else:
        logger.info('rating_managment.add_rating_action >> Student NOT-Enroll in course')
        messages.error(request,'You are not enroll in that course.')
        return HttpResponse(json.dumps(False), 'applications/json')


@login_required
def remove_rating_action(request):
    if enroll_helper(request):
        logger.info('rating_managment.remove_rating_action >> Student Enroll in course')
        if request.method == 'POST':
            course_obj = CourseDetail.objects.get(id=request.POST.get('c_id'))
            if Rating.objects.remove_review(request.user,course_obj):
                messages.info(request,'Your review is deleted')
                return HttpResponse(json.dumps(True), 'applications/json')
            else:
                messages.error(request,'Not able to remove the review and rating.')
                return HttpResponse(json.dumps(False), 'applications/json')
    else:
        logger.info('rating_managment.remove_rating_action >> Student NOT-Enroll in course')
        messages.error(request,'You are not enroll in that course.')
        return HttpResponse(json.dumps(False), 'applications/json')

