from django.template import Library
from django.template.defaultfilters import stringfilter
from tracker.models import StudentTracker, Progress
from course_mang.models import CourseWeek
from course_test_handling.models import Tests

register = Library()

# @stringfilter
@register.filter(name = 'to_newline')
def to_newline(value):
    if '**' in value:
      value=value.replace('**','<br>')
    return value

@register.filter(name = 'get_img')
def get_img(user):
  from student.models import ProfilePicture
  try:
    p_pic = ProfilePicture.objects.get(user = user)
    return '/lms/media/'+str(p_pic.picture)
  except Exception as e:
    print e.args
    return '/lms/media/profile_images/CLAT_default_DP.png'

@register.filter(name = 'get_course_img')
def get_course_img(course):
  from course_mang.models import CourseImage
  try:
    c_pic = course.course_image
    assert c_pic,'AssertError: Not have course picture'
    return '/lms/media/'+str(c_pic.picture)
  except Exception as e:
    print e.args
    return '/lms/media/course_demo_images/EDX_demo_course_image.jpg'

@register.filter(name='str_m_time_progress')
def _module_time_progress(str_course_module,user):
    try:
      course_module = CourseWeek.objects.filter(week_module_name = str(str_course_module))
      stu_tracker = StudentTracker.objects.get(student=user,module=course_module)
      progress = Progress.objects.get(tracker = stu_tracker)
      data = round((float(progress.time_progress)/60)*100/40)
      if data > 100:
        data = 100
      return data    
    except Exception as e:
      return 0

@register.filter(name='cache_url')
def cache_url(url_str):
    from random import uniform
    return url_str+'?num='+str(uniform(0,1000))

@register.filter(name='module_list')
def module_list(enroll_course):
  try:
    course_module = CourseWeek.objects.filter(course = enroll_course)
    return course_module
  except Exception as e:
    return None

@register.filter(name='module_width')
def module_width(enroll_course):
  try:
    course_module = CourseWeek.objects.filter(course = enroll_course)
    return round(float(100/len(course_module)))
  except Exception as e:
    return 0

# @register.filter(name='have_inline_test')
# def have_inline_test(module_name):
#     tests = Tests.objects.get(module_name = course_module_name)

@register.filter(name = 'get_inline_url')
def get_inline_url(course_module_name, course):
  try:
    tests = Tests.objects.filter(course = course, module_name = course_module_name, test_type = 'I')[0]
    # print tests.schedule_key
    return tests.schedule_key
  except Exception as e:
    print e.args
    return None


@register.filter(name = 'get_midterm_url')
def get_midterm_url(course_module_name, course):
  try:
    tests = Tests.objects.get(course = course, module_name = course_module_name, test_type='M')
    return tests.schedule_key
  except Exception as e:
    print e.args
    return None


@register.filter(name = 'get_casestudy_url')
def get_casestudy_url(course_module_name, course):
  try:
    tests = Tests.objects.filter(course = course, module_name = course_module_name, test_type = 'C')[0]
    return tests.schedule_key
  except Exception as e:
    print e.args
    return None

@register.filter(name = 'get_endterm_url')
def get_endterm_url(course):
  try:
    tests = Tests.objects.get(course = course, test_type = 'E')
    return tests.schedule_key     
  except Exception as e:
    print e.args
    return None



# @register.filter(name='take_test_key')
# def take_test_key(course_module_name):
#   try:
#     course_module = CourseWeek.objects.get(week_module_name = course_module_name)
#     return course_module.schedule_key
#   except Exception as e:
#     print e.args
#     return None    
