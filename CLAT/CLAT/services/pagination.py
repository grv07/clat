from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def get_paginated_list(size=7,obj_list=None,page=None):
    if len(obj_list) > 0:
        paginator = Paginator(obj_list, 7) # Show 25 contacts per page
        try:
            obj_list = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            obj_list = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            obj_list = paginator.page(paginator.num_pages)
        return obj_list   
    else:
        return []
        
