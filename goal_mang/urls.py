from django.conf.urls import include, url

from goal_mang import  views


urlpatterns = [
		url(r'^set/goal/$',views.create_goal, name="create-goal"),
		url(r'^get/modules/$',views.get_module_name_list, name="create-goal"),
		url(r'^goal/list/$',views.goal_list_actions, name="create-goal"),
]
