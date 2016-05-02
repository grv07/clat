from django.shortcuts import render, redirect
from course_mang.models import CourseDetail
from student.models import Student
from django.contrib.auth import authenticate, login, logout
from CLAT.services import pagination
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# from django.core.cache import cache
from course_mang.utilities import is_verified_user
from CLAT.services.constants import CACHE_KEYS


'''Login a user here'''
def login_user(request):
    user = None
    try:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password = password)
        student = Student.objects.get(student = user.id)
    except Exception as e:
        student = None
        user = None
    if student is not None:
        if user.is_active:
            if not is_verified_user(user):
                request.session['not_verify'] = True
                request.session['phone_number'] = student.phone_number
                request.session['email'] = user.email
                return redirect('/account/verification/')
            else:
                login(request, user)
                if request.POST.has_key('remembered') and request.POST['remembered'] == 'true' : 
                    request.session.set_expiry(604800)  # == 7*24*60*60 == 1 week
                messages.success(request,'You logged in successfully.')
            return redirect('/dashboard/')
        else:
            pass
    else:
        messages.error(request,'Please enter valid credentials')
        course_list = CourseDetail.objects.all()
        course_list = pagination.get_paginated_list(obj_list = course_list, page = request.GET.get('page'))
        return render(request, 'new_home.html', {'login_error': True, 'next': request.POST.get('next'), 'course_list':course_list})


''' Call when logout a user '''
@login_required
def logout_user(request):
    # cache.delete(CACHE_KEYS['d'] % request.user.id)
    # cache.delete(CACHE_KEYS['cvd'] % request.user.id)
    logout(request)
    messages.info(request,'You logged out successfully.')
    return redirect("/home/")


