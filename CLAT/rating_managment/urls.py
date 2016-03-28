from django.conf.urls import include, url, patterns
from rating_managment import views

urlpatterns = patterns('',
                       url(r'^add_rating/$',views.add_rating_action, name="add-rating"),                        
                       url(r'^remove_rating/$',views.remove_rating_action, name="remove-rating"),
                       )
