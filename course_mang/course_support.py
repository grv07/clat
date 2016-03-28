import zipfile

import os



'''This method return a course details object'''
def set_course_deatils_obj(course_detail_model, request, req_post_data):
    import uuid
    import datetime
    from teacher.models import Teacher

    course_detail_obj = course_detail_model.save(commit=False)
    course_detail_obj.teacher = Teacher.objects.get(user_ptr_id=request.user.id)
    course_detail_obj.course_uuid = uuid.uuid4()
    text_start_date = req_post_data.get('course_start_time','0:0').split(':')
    text_end_date = req_post_data.get('course_end_time','0:0').split(':')

    if text_start_date and text_end_date:
       start_time = datetime.time(int(text_start_date[0]),int(text_start_date[1]))
       end_time = datetime.time(int(text_end_date[0]),int(text_end_date[1])) 
       course_detail_obj.course_start_time =  start_time
       course_detail_obj.course_end_time =   end_time
       course_detail_obj.course_durations = datetime.time(abs(int(end_time.hour - start_time.hour)),abs(int(end_time.minute - start_time.minute))) 
    else:
        return None
    return course_detail_obj

'''This method use for return course video obj '''
def set_course_video_obj(video_form, video_file_name, course,week, video_url, module_name, video_type):
    
    course_video_obj = video_form.save(commit = False)
    course_video_obj.course = course
    course_video_obj.week = week
    course_video_obj.video_url = video_url
    course_video_obj.module_name = module_name
    course_video_obj.video_file_name = video_file_name 
    course_video_obj.video_type = video_type
    
    return course_video_obj

def get_demo_course_url(course_type, course_uuid, course_name):
    if course_type and course_uuid:
        try:
            return '/' + str(course_type) + '/' + str(course_name) + '/' + str(course_uuid) + '/'
        except Exception as e:
            print e.args
            return False
    else:
        return None

def get_video_course_url(course_type, course_uuid, week_uuid,module_name):
    if course_type and course_uuid:
        try:
            return '/' + str(course_type) + '/' + str(course_uuid) + '/' + str(week_uuid) + '/' + str(module_name) + '/'
        except Exception as e:
            print e.args
            return False
    else:
        return None


def get_you_tube_url(you_tube_url):
    try:
        yut_url_id = you_tube_url.split('?v=')[1]
        return str(yut_url_id)
    except Exception as e:
        print e.args
        return False

'''NOT IN USE >>>>>>>'''
def save_video_file(path):
    from django.conf import settings

    import io
    if video_file is not None:
            zf = zipfile.ZipFile(video_file, 'r')
            if zf.__sizeof__() > 5:
                zf.extractall(path = str(path))
                return True
            else:
                return False

def save_uploaded_file (fileitem,file_dir_path):
    import io
    from django.conf import settings

    """This saves a file uploaded by an HTML form.
       The form_field is the name of the file input field from the form.
       For example, the following form_field would be "file_1":
           <input name="file_1" type="file">
       The upload_dir is the directory where the file will be written.
       If no file was uploaded or if the field does not exist then
       this does nothing.
    """
    if not os.path.exists(file_dir_path):
                os.makedirs(file_dir_path)
    fout  = io.open(file_dir_path + '' + fileitem.name, 'wb+')
    while 1:
        chunk = fileitem.file.read(1024)
        if not chunk: break
        fout.write (chunk)
    fout.close()
