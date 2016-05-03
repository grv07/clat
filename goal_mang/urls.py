from django.conf.urls import include, url

from goal_mang import  views


urlpatterns = [
		url(r'^set/goal/$',views.create_goal, name="create-goal"),
		url(r'^get/modules/$',views.get_module_name_list, name="get-module"),
		url(r'^goal/list/$',views.goal_list_actions, name="get-goal-list"),
		url(r'^goal/delete/(?P<goal_id>\d+)/$',views.goal_delete_action, name="delete-goal"),
]