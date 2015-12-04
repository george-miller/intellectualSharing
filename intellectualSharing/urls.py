from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'intellectualSharing.views.home', name='home'),
    url(r'^insertNode', 'intellectualSharing.views.insertNode', name='insertNode'),
    url(r'^getNodeId', 'intellectualSharing.views.getNodeId', name='getNodeId'),
    url(r'^getEdgeIdsFromNode', 'intellectualSharing.views.getEdgeIdsFromNode', name='getEdgeIdsFromNode'),
    url(r'^admin/', include(admin.site.urls)),
)
