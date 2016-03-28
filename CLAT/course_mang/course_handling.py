from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from course_mang import course_support
from teacher.models import Teacher
from django.contrib import messages
from django.template import Template
from django import template
from form import CourseWeekForm, CourseVideosForm, CourseDetailForm, CourseInformationForm
from models import CourseDetail, Comments, CourseVideos, CourseWeek, CourseImage
from django.contrib.auth.decorators import login_required
import os,json
from rating_managment.models import Rating
from utilities import admin_required, teacher_required, student_required, ADDED_VIDEO_MAIL_HTML, CACHE_KEYS
from student.models import EnrolledCourses, ProfilePicture, StudentInterests
from django.core.exceptions import ObjectDoesNotExist
from user_login.tasks import send_mail, send_bulk_mail
from CLAT.services import course_service, constants
from django.core.cache import cache
import logging
logger = logging.getLogger(__name__)

@login_required()
def file_select(request):
    return render(request, 'course_mang/upload_file.html')

@login_required()
def upload_you_tube(request):
    data = {}
    if request.method == 'POST':
        req_post_data = request.POST
        you_tube_form = YouTubeForm(data=req_post_data)
        if you_tube_form.is_valid():
            course_detail_model = CourseDetailModel(data=req_post_data)
            if course_detail_model.is_valid():
                course_detail_obj = course_support.set_course_deatils_obj(course_detail_model,request,req_post_data)
                
                course_detail_obj.course_url = course_support.get_you_tube_url(req_post_data.get('you_tube_url', None),
                                                                               course_detail_obj.course_uuid)
                course_detail_obj.course_type = 'YOU_TUBE'
                
                course_detail_obj.save()
                messages.success(request, 'Course uploaded successfully.')
            else:
                data = {'form': course_detail_model}

            return render(request, 'course_mang/upload_file.html', data)

        else:
            data = {'form': you_tube_form}
            return render(request, 'course_mang/upload_file.html', data)
    else:
        return render(request, 'course_mang/upload_file.html', data)


@login_required
@teacher_required
def create_course(request):
    # import time
    # k = time.time()
    import uuid
    import datetime
    data = {}
    if request.method == 'POST':
        req_post_data = request.POST
        req_files_data = request.FILES
        course_form = CourseDetailForm(req_post_data,req_files_data)
        course_info_form = CourseInformationForm(req_post_data)
        data['form']=course_form
        data['form_course_info'] = course_info_form
        file_bytes = None
        if course_form.is_valid() and course_info_form.is_valid():
	    try:
		course_detail_obj = course_support.set_course_deatils_obj(course_form,request,req_post_data)
            	course_detail_obj.course_durations = req_post_data.get('course_durations')
            	if req_post_data['demo_type'] == constants.DEMO_VIDEO_TYPE_BUTTON[0]:
                	req_files_data = request.FILES
                	demo_file = req_files_data.get('course_demo_file')
                	filename, file_extension = os.path.splitext(demo_file.name)
                	course_detail_obj.course_demo_file_url = course_support.get_demo_course_url('demo/mp4', course_detail_obj.course_uuid, str(course_detail_obj.course_name))
                
            	if req_post_data['demo_type'] == constants.DEMO_VIDEO_TYPE_BUTTON[1]:
                	course_detail_obj.course_demo_file_url = course_support.get_you_tube_url(req_post_data.get('course_demo_file_url', None))
                	course_detail_obj.course_demo_file = 'utb'
	    	if req_post_data.get('show_video') == None:
			course_detail_obj.course_demo_file = 'img'

                course_detail_obj.save()
                course_info_obj = course_info_form.save(commit=False)
                course_info_obj.course = course_detail_obj
                course_info_obj.course_description = req_post_data.get('course_description',' ')
                course_info_obj.course_objective = req_post_data.get('course_objective',' ')
                course_info_obj.save()
                students_to_notified = StudentInterests.objects.filter(category__icontains=course_detail_obj.course_sectors_and_associates)
                list_of_students_emails = [student.user.email for student in students_to_notified]
                filtered_courses = CourseDetail.objects.filter(course_sectors_and_associates=course_detail_obj.course_sectors_and_associates).all()
                html="Related courses you can view <br>"
                
                for course in filtered_courses:
                    link = "<a href='http://"+request.META['HTTP_HOST']+'/course/details/'+course.course_uuid+'/'+"'> "+course.course_name+" </a>"
                    html = html + "<br>" + link + "<br>"


                for email in list_of_students_emails:
                    send_bulk_mail(html, email,'eQUEST new course created.')

                if CourseImage.objects.create(course=course_detail_obj, picture=constants.DEFAULT_COURSE_IMAGE):
                    messages.success(request, 'Course created successfully.')
                    # print time.time() - k,'-------------'
                    return redirect('/teacher/')
            except Exception as e:
                print e.args
            data={'weeks':course_detail_obj.course_durations, 'course_id':course_detail_obj.id}
        else:
            data = {'form': course_form}
            data['form_course_info'] = course_info_form
            return render(request, 'course_mang/upload_file.html', data)
        data['course_week_form'] = CourseWeekForm()
        return render(request, 'course_mang/create_modules.html', data)
    data['form']= CourseDetailForm()
    data['form_course_info'] = CourseInformationForm()
    return render(request, 'course_mang/upload_file.html', data)


@login_required
@teacher_required
def create_modules(request, course_uuid):

    course_detail_obj = CourseDetail.objects.get(course_uuid = course_uuid)
    course_id = course_detail_obj.id
    num_of_weeks = course_detail_obj.course_durations

    if request.method == 'POST':
        import uuid
        req_post_data = request.POST

        course_week_form = CourseWeekForm(req_post_data)
        
        if course_week_form.is_valid():
            already_present = False
            module_name = req_post_data.get('week_module_name').strip()
            week = req_post_data.get('num_of_weeks')
            module_details = req_post_data.get('week_detail').strip()
            courseweek_len = CourseWeek.objects.filter(course=course_detail_obj)
            course_len = courseweek_len.filter(week_number=week).count()

            if course_len < 4:
                if course_len > 0:
                    _week_uuid = CourseWeek.objects.filter(week_number=week,course=course_detail_obj)[0].week_uuid
                else:
                    _week_uuid = uuid.uuid1()
                module_created = CourseWeek.objects.create(course = course_detail_obj, module_number = courseweek_len.count()+1, week_number = week, 
                    week_module_name = module_name, week_uuid =_week_uuid, week_detail = module_details)
                if not module_created:
                    messages.error(request, 'Course Module creation failed.')
                else:
                    all_enroll_courses = EnrolledCourses.objects.filter(course = course_detail_obj)
                    if all_enroll_courses:
                        from student.models import UserCourseProgress
                        for enroll_course in all_enroll_courses:
                            u_course_progrs = UserCourseProgress.objects.create(course_week = module_created, enrolled_courses = enroll_course)
                    messages.success(request, 'Course module for Week '+week+'  created successfully.')
                    already_present = True
                return HttpResponseRedirect('/course/details/'+course_uuid+'/')
            else:
                messages.error(request, 'A week can have 4 modules only.Delete old ones.')
                return redirect('/create/modules/'+course_uuid+'/')
        else:
            return render(request, 'course_mang/create_modules.html',{'course_uuid':course_uuid,'weeks':num_of_weeks,'course_week_form':course_week_form})
    else:
        course_week_form = CourseWeekForm()
        return render(request, 'course_mang/create_modules.html',{'course_uuid':course_uuid,'weeks':num_of_weeks,'already_present':False,'course_week_form':course_week_form})

@login_required
@teacher_required
def upload_course_video_file(request, course_uuid):
    import uuid
    import datetime

    data = {}

    course_detail_obj = CourseDetail.objects.get(course_uuid = course_uuid)
    course_id = course_detail_obj.id

    data['course_id'] = course_id
    data['course_uuid'] = course_uuid
    
    if request.method == 'POST':
        req_post_data = request.POST
        youtube_error = False
        video_type = req_post_data.get('video_type')
        module_name = req_post_data.get('module_name').strip().replace('%20',' ').replace("%3A",":").replace('%26','&').replace('%29',')').replace('%28','(').replace('%2C',',')
        

        my_course_uuid = course_uuid
        
        if video_type == constants.COURSE_VIDEO_TYPE[0] or video_type == constants.COURSE_VIDEO_TYPE[1]:
            req_files_data = request.FILES
            course_videos_form = CourseVideosForm(req_post_data ,req_files_data)
            data['course_videos_form'] = course_videos_form

            if course_videos_form.is_valid():
                video_file = req_files_data.get('video_file')
                file_bytes = None
                my_course_uuid = course_uuid
                course_week_obj = CourseWeek.objects.get(course = course_detail_obj, week_module_name = module_name)
                if course_week_obj.is_available == False:
                    messages.error(request,'This module has already 1 video.')
                    return HttpResponseRedirect('/upload/videos/'+course_uuid+'/')
                
                _week_uuid = course_week_obj.week_uuid
                filename, file_extension = os.path.splitext(video_file.name)
                if file_extension == constants.VIDEO_FILE_EXTENSIONS[1]:
                    video_url = course_support.get_video_course_url(constants.COURSE_VIDEO_INITIAL_PATH[1], my_course_uuid, _week_uuid, module_name)
                    course_video_obj = course_support.set_course_video_obj(video_form = course_videos_form, video_file_name=filename, course=course_detail_obj, week = course_week_obj, 
                        video_url = video_url, module_name = module_name, video_type = video_type)
                    # coursevideos=CourseVideos.objects.create(course=course_detail_obj,week=course_week_obj,video_url = video_url,video_file=filename,module_name=module_name,video_type=video_type)
                
                elif file_extension == constants.VIDEO_FILE_EXTENSIONS[0]:
                    video_url = course_support.get_video_course_url(constants.COURSE_VIDEO_INITIAL_PATH[0], my_course_uuid, _week_uuid, module_name)
                    course_video_obj = course_support.set_course_video_obj(video_form = course_videos_form, video_file_name = filename, course = course_detail_obj, 
                        week = course_week_obj, video_url = video_url, module_name = module_name, video_type = video_type)
                print video_url
                try:
                  course_video_obj.save()
                  course_week_obj.is_available = False
                  course_week_obj.save()
                  
                  import zipfile

                  if zipfile.is_zipfile(video_file) and file_extension == constants.VIDEO_FILE_EXTENSIONS[1]:
                    zf = zipfile.ZipFile(constants.ROOT_PATH_FOR_VIDEOS + str(video_url) + str(filename) + constants.VIDEO_FILE_EXTENSIONS[1])
                    if zf.__sizeof__() > 5:
                        # print('>>>>>>>>>>>>',str(video_url)+str(filename))
                        try:
                           zf.extractall(path = constants.ROOT_PATH_FOR_VIDEOS +str(video_url))
                           messages.success(request,'File uploaded Successfully.')
                        except Exception as e:
                           print e.args
                    os.remove(constants.ROOT_PATH_FOR_VIDEOS + str(video_url) + str(filename) + constants.VIDEO_FILE_EXTENSIONS[1])
                except Exception as e:
                    print e.args
                    messages.error(request,'Error in your course video saving action.')
                complete_link = 'http://' + str(request.META['HTTP_HOST']) + '/course/details/' + str(course_detail_obj.course_uuid) + '/'
                
                list_of_students_emails = [student.user.email for student in EnrolledCourses.objects.list_all_students_enrolled(course=course_detail_obj)]
                
                html = ADDED_VIDEO_MAIL_HTML.format(module_name = module_name, course_name = course_detail_obj.course_name, complete_link = complete_link,week_detail=
                    CourseWeek.objects.get(week_module_name=module_name).week_detail)

                for email in list_of_students_emails:
                    send_bulk_mail(html, email, subject='eQUEST new video added')

                return render(request, 'course_mang/upload_courses.html', data)
            else:
                return render(request, 'course_mang/upload_courses.html', data)
        else:
            course_videos_form = CourseVideosForm(req_post_data)
            if course_videos_form.is_valid():
                youtube_course_url = req_post_data.get('video_url')
                course_week_obj = CourseWeek.objects.get(course=course_detail_obj,week_module_name=module_name)
                _week_uuid = course_week_obj.week_uuid
                coursevideos=CourseVideos.objects.create(course=course_detail_obj,week=course_week_obj,video_url = course_support.get_you_tube_url(youtube_course_url),module_name=module_name,video_type=video_type)
                data['course_videos_form'] = CourseVideosForm(req_post_data,{})
            else:
                youtube_error  = True
                data['youtube_error']=youtube_error
                data['course_videos_form'] = CourseVideosForm()
                return render(request, 'course_mang/upload_courses.html', data)
        return HttpResponseRedirect('/course/details/'+my_course_uuid+'/')
    else:
        data['course_videos_form'] = CourseVideosForm() 
    return render(request, 'course_mang/upload_courses.html', data)



def handle_uploaded_file(fileName, filePath):
    with open(filePath, 'wb+') as destination:
        for chunk in fileName.chunks():
            destination.write(chunk)


def course_list_action(request):
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

    course_list = CourseDetail.objects.all()
    paginator = Paginator(course_list, 6)
    page = request.GET.get('page')
    try:
        course_list = paginator.page(page)
    except PageNotAnInteger:
        course_list = paginator.page(1)
    except EmptyPage:
        course_list = paginator.page(paginator.num_pages)

    return render(request, 'course_mang/my_courses.html', {'course_list': course_list})

def course_details_action(request, uuid):
    data = {}
    try:
        course_detail_obj = CourseDetail.objects.get(course_uuid=uuid)
        is_student_enrolled = False
        are_videos_present = False
        user = request.user

        '''
        If user is not logged in then no need to fetch enroll courses details.
        '''

        rating = None
        if user.is_authenticated():
            if EnrolledCourses.objects.is_student_enrolled(user,course_detail_obj) :
                is_student_enrolled=True
            else:
                from uuid import uuid4
                data['txnid'] = uuid4().hex
            if Rating.objects.is_review_posted(course_detail_obj,user):
                rating = Rating.objects.get(course=course_detail_obj,user=user)
            filtered_reviews = Rating.objects.filter(course=course_detail_obj).exclude(user=user)[:4]
        else:
            filtered_reviews = Rating.objects.filter(course=course_detail_obj)[:4]

        from collections import Counter

        total_rating_dict = Counter([review.ratings for review in Rating.objects.list_all_reviews(course_detail_obj)])
        total_reviews = Rating.objects.total_reviews(course_detail_obj)
        for key in total_rating_dict.keys():
            total_rating_dict[str(key)] = total_rating_dict[key]*100/total_reviews
        data['course'] = course_detail_obj
        data['course_id'] = uuid
        data['rating'] = rating
        data['is_student_enrolled'] = is_student_enrolled

        data['total_rating_dict'] = total_rating_dict
        data['filtered_reviews'] = filtered_reviews
        data['is_student_enrolled'] = is_student_enrolled

        if course_detail_obj.course_durations == '01':
            data['course_duration'] = abs(course_service.duration_of_course(course_detail_obj.course_start_date,course_detail_obj.course_end_date))
        else:
            data['course_duration'] = course_detail_obj.course_durations

        if course_detail_obj.course_uploaded_videos.filter(course = course_detail_obj):
            are_videos_present = True
        data['are_videos_present'] = are_videos_present
    except Exception as e:
        logger.error('under course_mang.course_handling.course_details_action '+str(e.args))
    return render(request, 'course_mang/new_course_details.html',data)


@login_required
def course_videos_display(request,course_uuid):
    try:
        course_detail_obj = CourseDetail.objects.get(course_uuid=course_uuid)
        if EnrolledCourses.objects.is_student_enrolled(request.user,course_detail_obj):
            logger.info('under course_mang.course_handling.course_videos_display student is enrolled.'+' UID-'+str(request.user.id)) 
            course_weeks = CourseWeek.objects.filter(course=course_detail_obj).order_by('module_number')
            from collections import OrderedDict
            weeks = OrderedDict()
            weekly_details = {}
            for week_obj in course_weeks:
                weeks[week_obj.week_number] = OrderedDict()
                weekly_details[week_obj.week_number] = []

            for week in weeks.keys():
                course_week_objs=course_weeks.filter(week_number = week)
                weekly_details[week] = [i.week_detail for i in course_week_objs]
                for week_obj in course_week_objs:
                    values=[[i.video_file,i.video_type] for i in CourseVideos.objects.filter(course=course_detail_obj,week=week_obj,module_name=week_obj.week_module_name)]
                    weeks[week][week_obj.week_module_name]=values
            data =  {'course': course_detail_obj,'weeks':weeks}
            data['enrolledcourse'] = EnrolledCourses.objects.get(course=course_detail_obj,user=request.user)
            data['weekly_details'] = weekly_details  
            # cache.set(CACHE_KEYS['cvd'] % (request.user.id, course_detail_obj.id,), data)
            return render(request, 'course_mang/course_videos.html',data)
            # return render(request, 'course_mang/course_videos.html', cvd_cache)      
        else:
            messages.info(request,'Not allowed : First enroll in that course.')
            return HttpResponseRedirect('/home/')
    except Exception as e:
        logger.error('under course_mang.course_handling.course_videos_display '+str(e.args)+' UID-'+str(request.user.id))
        return render(request, 'course_mang/course_videos.html',{})


@login_required
@teacher_required
def course_videos_display_teacher(request, course_uuid):
    course_detail_obj = CourseDetail.objects.get(course_uuid = course_uuid, teacher = request.user.teacher)
    course_weeks = CourseWeek.objects.filter(course = course_detail_obj).order_by('module_number')

    weeks={}

    from collections import OrderedDict

    for week_obj in course_weeks:
        weeks[week_obj.week_number] = OrderedDict()

    for week in weeks.keys():
        course_week_objs=course_weeks.filter(week_number=week)

        for week_obj in course_week_objs:
            values=[[i.video_file,i.video_type] for i in CourseVideos.objects.filter(course=course_detail_obj,week=week_obj,module_name=week_obj.week_module_name)]
            weeks[week][week_obj.week_module_name]=values

    data =  {'course': course_detail_obj,'weeks':weeks}

    return render(request, 'course_mang/course_videos.html',data)

@login_required
@admin_required
def course_videos_display_admin(request, course_uuid):
    course_detail_obj = CourseDetail.objects.get(course_uuid = course_uuid)
    course_weeks = CourseWeek.objects.filter(course = course_detail_obj).order_by('module_number')
    print course_detail_obj
    weeks = {}

    from collections import OrderedDict

    for week_obj in course_weeks:
        weeks[week_obj.week_number] = OrderedDict()

    for week in weeks.keys():
        course_week_objs=course_weeks.filter(week_number=week)

        for week_obj in course_week_objs:
            values=[[i.video_file,i.video_type] for i in CourseVideos.objects.filter(course=course_detail_obj,week=week_obj,module_name=week_obj.week_module_name)]
            weeks[week][week_obj.week_module_name]=values

    data =  {'course': course_detail_obj,'weeks':weeks}

    return render(request, 'course_mang/course_videos.html',data)

@login_required
def load_comments(request,uuid):
    start=int(request.session['start'])
    count = int(request.GET['count'])
    end=count
    comments_list = Comments.objects.list_all(uuid=uuid,start=start,end=end)
    request.session['start']=count
    return HttpResponse(json.dumps(comments_list), content_type="application/json")


@login_required
def delete_course_file_action(request, uuid):
    import shutil

    course_details = None 
    try:
        from django.conf import settings

        course_detail_obj = CourseDetail.objects.get(course_uuid=uuid)
        course_week_objs = CourseWeek.objects.filter(course = course_detail_obj)
        course_videos_objs  = CourseVideos.objects.filter(course = course_detail_obj)

        video_url = constants.ROOT_PATH_FOR_VIDEOS + constants.COURSE_VIDEO_INITIAL_PATH[0] + '/' + course_detail_obj.course_uuid+'/'
        if os.path.exists(video_url):
            print 'present'
            shutil.rmtree(video_url)
        else:
            print 'no mp4 file provided'

        video_url = constants.ROOT_PATH_FOR_VIDEOS + constants.COURSE_VIDEO_INITIAL_PATH[1] + '/' + course_detail_obj.course_uuid+'/'
        if os.path.exists(video_url):
            print 'present'
            shutil.rmtree(video_url)
        else:
            print 'no articulate file provided'

        video_url = constants.ROOT_PATH_FOR_VIDEOS + constants.DEMO_VIDEO_INITIAL_PATH + course_detail_obj.course_name+'/'
        if os.path.exists(video_url):
            print 'present'
            shutil.rmtree(video_url)
        else:
            print 'no demo file provided'

        for course_video_obj in course_videos_objs:
            course_video_obj.delete()


        for course_week_obj in course_week_objs:
            course_week_obj.delete()

        course_detail_obj.delete()
        messages.success(request, 'Course '+ course_detail_obj.course_name +' deleted successfully.')

    except Exception as e:
        print e.args
        messages.error(request, 'Error in this request to delete a course.')
    return HttpResponse(json.dumps(True), content_type="application/json")


@login_required()   
def read_articulate_file(request):
    fileobject = open('/home/madmachines/pyprojects/CLAT/lms_videos/E_Lecture_and_assessment/story.html', 'r', 4)
    from django.template import engines

    django_engine = engines['django']
    t = django_engine.from_string(fileobject.read())
    c = template.Context({'dir_name': dir_name})
    return HttpResponse(t.render(c))


@login_required()
def course_comment_post(request,uuid):
    if request.method == 'GET':
        user = request.user
        comment = request.GET.get('comment')
        posted_comment=Comments.objects.post_comment(user=user,uuid=uuid,content=comment)        
        if posted_comment is None:
            return HttpResponse('error in posting comment')
        ajax_data={'user_id':posted_comment.user_id.username,'comment':posted_comment.comment}       
        return HttpResponse(json.dumps(ajax_data), content_type="application/json")
    return HttpResponseRedirect('/course/details/'+uuid)


def course_reviews(request,uuid):
    data={}
    try:
        user = request.user
        course = CourseDetail.objects.get(course_uuid=uuid)
        data['course'] = course
        if user.is_authenticated():
            data['total_reviews'] = Rating.objects.list_all_reviews(course).exclude(user=user)
        else:
            data['total_reviews'] = Rating.objects.list_all_reviews(course)
    except Exception as e:
        logger.error('under course_mang.course_handling.course_reviews '+str(e.args))
    return render(request, 'course_mang/course_reviews.html',data)
