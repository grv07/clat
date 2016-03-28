from django.conf.urls import include, url
from django.contrib import admin
from user_login import urls as user_login
from teacher import urls as teacher_url
from student import urls as student_url
from assesment_engine import urls as assesment_url
from course_mang import urls as course_url
from rating_managment import urls as rating_url
from course_test_handling import urls as course_test_handling_url
from payment import urls as payment_url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import patterns, include, url, handler500,handler404


# from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^account/verification/(?P<uuid>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$',
        student_url.views.user_account_verification),
    url(r'^account/verification/(?P<uuid>[a-q0-9]{10})/$', student_url.views.user_account_verification),
    url(r'', include(user_login)),
    url(r'', include(teacher_url)),
    url(r'', include(assesment_url)),
    url(r'', include(student_url)),
    url(r'', include(course_url)),
    url(r'', include(rating_url)),
    url(r'^order/', include(payment_url)),
    url(r'',include(course_test_handling_url)),
    # url(r'^api-auth/$', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^account/verification/$', user_login.views.account_verification_msg),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT, 'show_indexes': settings.DEBUG}),
    url(r'^lms/media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }), 
]

# urlpatterns = format_suffix_patterns(urlpatterns)
urlpatterns += staticfiles_urlpatterns()
handler404 = user_login.views.error404
handler500 = user_login.views.error500
