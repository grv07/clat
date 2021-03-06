from django.conf.urls import url, patterns
from course_mang import course_handling, views


urlpatterns = patterns('',
                       url(r'^upload/videos/(?P<course_uuid>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$', course_handling.upload_course_video_file, name="upload-course-video-file"),
                       url(r'^inline/progress/(?P<course_uuid>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/(?P<module_name>.+)/$',views.inline_progress, name="inline_progress"),
                       url(r'^upload/art_course/$', course_handling.create_course, name="create-course"),
                       url(r'^create/modules/(?P<course_uuid>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$', course_handling.create_modules, name="create-modules-weekly"),
                       url(r'^upload/utb_course/$', course_handling.upload_you_tube, name="upload-youtube-course"),
                       url(r'^course/list/$', course_handling.course_list_action, name="courses-list"),
                       url(r'^read/$', course_handling.read_articulate_file, name="course-articulate-read"),
                       url(r'^video/articulate/(?P<course_uuid>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/(?P<week_uuid>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/(?P<module_name>.+)/(?P<folder_name>.+)/$',
                           views.articulate_video_action, name="course-articulate-action"),
                       url(r'^video/(?P<path>.+)/$',views.video_action, name="video-action"),
                       url(r'^teacher/video/(?P<path>.+)/$',views.video_action_teacher, name="video-action-teacher"),
                       url(r'^video/youtube/(?P<video_url>\w+)/$',views.utb_video_action, name="course-youtube-action"),
                       url(r'^video/mp4/(?P<course_uuid>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/(?P<week_uuid>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/(?P<module_name>.+)/(?P<video_file_name>.+)$',
                           views.mp4_video_action, name="course-mp4-action"),
                       url(r'^demo/MP4/(?P<uuid>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$',
                           views.mp4_demo_action, name="course-demo-mp4-action"),
                       url(r'^video/details/$', views.articulate_video_action, name="video-details"),
                       url(r'^verify-course-name/$', views.course_name_validation, name="verify-course-name"),
                       url(r'^states/india/$', views.state_india, name="states"),
                       url(r'^get_modules/$', views.get_modules, name="get-modules"),

                       url(r'^course/delete/(?P<uuid>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$',
                           course_handling.delete_course_file_action, name="course-action-file-delete"),
                       url(r'^course/details/(?P<uuid>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$',
                           course_handling.course_details_action, name="course-action-details"),
                       url(r'^course/details/(?P<uuid>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/postcomment/$',
                           course_handling.course_comment_post, name="course-comment-post"),
                      url(r'^course/details/(?P<uuid>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/loadcomments/$',course_handling.load_comments, name="course-comments-load"),
                      url(r'^course/videos/(?P<course_uuid>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$',
                           course_handling.course_videos_display, name="course-videos-display"),
                      url(r'^course/videos/teacher/(?P<course_uuid>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$',
                           course_handling.course_videos_display_teacher, name="course-videos-display-teacher"),
                      url(r'^course/admin/(?P<course_uuid>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$',
                           course_handling.course_videos_display_admin, name="course-videos-display-admin"),

                      url(r'^allcourses/$',views.all_courses,name="all-courses"),
                      url(r'^course/reviews/(?P<uuid>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$',
                           course_handling.course_reviews, name="course-reviews"),
                      url(r'^filter/courses/$',views.filter_courses, name="filter-courses"),
                      url(r'^filtermore/courses/$',views.more_courses, name="filter-more-courses"),
                      url(r'^get/course_names/$',views.get_course_names, name="get-course-names"),
                      url(r'check/module/$', views.check_module,name="check-module"),
                      url(r'check/week/$',views.check_module_under_week,name='check-module-under-week'),
                      url(r'^send/timespent/$',views.post_time_spent,name='post-time-spent'),
)
