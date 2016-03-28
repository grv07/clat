from django.contrib import admin
from user_login.models import Foo
from django.conf.urls import patterns, include, url

@admin.register(Foo)
class AuthorAdmin(admin.ModelAdmin):
    pass
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def export(self, request):
    print '... do your stuff ...'
    return HttpResponseRedirect(request.META["HTTP_REFERER"])

class YOUR_MODELAdmin(admin.ModelAdmin):
    '''... list def stuff ...'''
    def get_urls(self):
        urls = super(MenuOrderAdmin, self).get_urls()
        my_urls = patterns("",
            url(r"^export/$", export)
        )
        return my_urls + urls
# Register your models here.
