from django.conf.urls import patterns, include, url
from payment import views
from student.views import enroll_student
urlpatterns = patterns('',
    url(r'^checkout/$', views.checkout, name='order.checkout'),
    url(r'^success/$', views.success, name='order.success'),
    url(r'^failure/$', views.failure, name='order.failure'),
    url(r'^cancel/$', views.cancel, name='order.cancel'),
    #url(r'^check/payment/(?P<txnid>[a-z0-9]+)/$', views.check_payment, name='order.check-payment'),	
)
