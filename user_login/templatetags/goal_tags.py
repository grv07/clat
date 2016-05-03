from django import template
from user_login.models import Badges
from goal_mang.models import GoalBadge

register = template.Library()

@register.filter(name = 'get_class')
def get_class(value):
  return value.__class__.__name__

@register.filter(name = 'get_badges')
def get_badges(goal):
	badges = []
	try:
		goal_badge = GoalBadge.objects.get(goal = goal)
		badge_id_list = goal_badge.get_badge_list()
		for badge_id in badge_id_list:
			badges += [Badges.objects.get(pk = badge_id)]
	except Exception as e:
		print e.args
	return badges