from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'intellectualSharing.views.home', name='home'),
    url(r'^insertNode', 'intellectualSharing.views.insertNode', name='insertNode'),
    url(r'^connectNodes', 'intellectualSharing.views.connectNodes', name='connectNodes'),
    url(r'^getRouteRelationships', 'intellectualSharing.views.getRouteRelationships', name='getRouteRelationships'),
    url(r'^admin/', include(admin.site.urls)),
)
