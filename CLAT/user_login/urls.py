from django.conf.urls import url, patterns,include

from user_login import views
# from user_login import api
from django.contrib.auth.decorators import login_required

# from resumable.views import ResumableUploadView
from django.contrib import admin

urlpatterns = patterns('',
						 # Include API URLs
						 # url(r'^students/list/$', api.StudentViewSet.as_view()),
						 # url(r'^student/details/(?P<pk>[0-9]+)/$', api.StudentObject.as_view()),
						 # url(r'^student/create/$', api.CreateStudent.as_view()),
						 url(r'^home/$', views.home),
						 url(r'^$', views.home),
						 url(r'^login/$', views.user_login_form, name="login-url"),
						 url(r'^logout/$', views.user_logout, name="logout-url"),
						 url(r'^file/$', views.file_view),
						 url(r'^user/login/$', views.user_login_action, name="user-login-url"),
						 url(r'^account/verification/$', views.account_verification_msg, name="verify-account-url"),
						 # url(r'^is/verified/$', views.is_user_acc_verified, name="check-verification-url"),
						 url(r'^load_cities/$', views.get_cities, name="get-cities"),
						 url(r'^temp/$', views.paginate_action, name="paginate-action"),
						 url(r'^troubleshoot/(?P<_type>[a-z]+)/$', views.rescue_credentials, name="rescue-credentials"),
						 url(r'^account/reset/password/(?P<_uuid>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/(?P<_type>[a-z]+)/$',
							views.change_password,name="change-password"),
						 url(r'^account/reset/password/(?P<_uuid>[a-q0-9]{10})/(?P<_type>[a-z]+)/$',
							views.change_password,name="change-password-small-uuid"),
						 url(r'^skip/clear/$', views.clear_session),
						 url(r'^send/otp/$', views.send_otp_code),
						 url(r'^about/$', views.about_page),
						 url(r'^verify/user_otp/$', views.user_otp_verification),                       

						 url(r'^admin_resumable$', include('admin_resumable.urls')),
						 url(r'^faq_page/$', views.faq_page),
						 url(r'^privacy_policy/$', views.privacy_policy),
						 url(r'^contact/$', views.contact),
						 url(r'^termsandservices/$', views.terms_and_services),
						 url(r'^certification_policy/$', views.certification_policy),
						 url(r'^@temp@update/$', views.update),
						
						 url(r'^ask/question/(?P<course_uuid>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$',views.have_question),

											 )
admin.site.site_header = 'e-Quest admin'