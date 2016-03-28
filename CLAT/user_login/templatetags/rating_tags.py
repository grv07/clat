from django import template
from rating_managment.models import Rating

register = template.Library()


def get_rating_class(rating_list):
    class_list = []
    total_rater = len(rating_list)
    if total_rater > 0:
        total_rating = 0
        for rate in rating_list:
            total_rating += rate.ratings
        total_rating = int(total_rating / total_rater)
        for num_rate in range(0, 5):
            if num_rate < total_rating:
                class_list.append('goldstar.png')
            else:
                class_list.append('star_empty.png')
        return class_list
    else:
        return class_list


@register.filter(name='is_course_rated')
def is_course_rated(value):
    try:
        rating_list = Rating.objects.filter(course_id=value)
        if rating_list:
            return get_rating_class(rating_list=rating_list)
        return []
    except Exception as e:
        print e.args
        return []


@register.filter(name='course_ratings')
def course_ratings(value):
    try:
        rating_list = Rating.objects.filter(course_id=value)
        if rating_list:
         return get_rating_class(rating_list=rating_list)
        return []
    except Exception as e:
        print e.args
        return []


@register.filter(name='rate_stars') 
def rate_stars(rating):
    return range(rating)