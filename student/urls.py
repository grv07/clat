from django.conf.urls import include, url, patterns
from student import views

urlpatterns = patterns('',
			url(r'^register/$', views.register_student_form, name="register-student"),
			url(r'^register/student/$', views.user_action, name="register-students-action"),
			url(r'^verify_email/$', views.user_email_verification, name="register-students-verfiy-email"),
			url(r'^verify/certificate/$', views.verify_certificate, name="students-certi-verfiy-email"),
			url(r'^db_email/$', views.email_in_db, name="db-verfiy-email"),
			url(r'^verify_username/$', views.username_verification, name="register-students-verfiy-username"),
			url(r'^account/verifications/(?P<uuid_key>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$', views.user_account_verification, name="students-verify-account-url"),
			url(r'^account/verifications/(?P<uuid_key>[a-f0-9]{10})/$', views.user_account_verification, name="students-verify-account-url"),

			url(r'^verify_phone_number/$', views.user_phone_number_verification, name="register-students-verfiy-phone-number"),
			url(r'^profile/$',views.profile,name='profile'),
			url(r'^profile/picture/$',views.save_profile_picture,name='save-profile-picture'),
			url(r'^remove_profile_picture/$',views.remove_profile_picture,name='remove-profile-picture'),
			url(r'^dashboard/$',views.dashboard,name='dashboard'),
			url(r'^enroll/student/$',views.enroll,name='enroll-student'),
			# url(r'^unenroll/student/(?P<course_uuid>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$',views.unenroll_student,name='unenroll-student'),
			url(r'^fetchmore/enrolledcourses/$',views.fetch_enrolled_courses,name='fetch-enroll-courses'),
			url(r'^(?P<course_uuid>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/progress/$',views.test_progress,name='test-progress'),
			url(r'^download/report/(?P<test_type>[a-z]+)/(?P<schedule_key>[A-Za-f0-9]{4,10})/$',views.download_test_report,name='download-test-report'),
			url(r'^download/certificate/(?P<course_uuid>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$',views.download_certificate,name='download-certificate'),
				url(r'^certificates/$',views.certificates,name='certificates'),

)