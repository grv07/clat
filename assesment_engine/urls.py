from django.conf.urls import include, url, patterns
import views

urlpatterns = patterns('',

                       url(r'^inline/test/(?P<course_uuid>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/(?P<test_key>[a-z0-9]{8,25})/$',views.assessment_inline, name="student-assessment-test"),
                       url(r'^end/test/(?P<course_uuid>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/(?P<schedule_key>[a-z0-9]{8,25})/$',views.assesment_end_test, name="student-ent-test"),
                       # url(r'^assessment/result/(?P<schedule_key>[a-f0-9]{4,8})/$',views.assessment_student_result, name="student-register-assessment"),
                       url(r'^assessment/all/$',views.get_all_assesments, name="all-assessment-details"),
                       url(r'^start/asm_notification/$',views.start_asm_notification,name='start-notify'),
                       url(r'^finish/asm_notification/$',views.finish_asm_notification,name='finish-notify'),
                       url(r'^grade/asm_notification/$',views.grade_asm_notification,name='grade-notify'),
                       
                       )
