from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'intellectualSharing.views.home', name='home'),
    url(r'^addNode', 'intellectualSharing.views.addNode', name='addNode'),
	url(r'^addRelationship', 'intellectualSharing.views.addRelationshipToNodes', name="addRelationship"),
    url(r'^admin/', include(admin.site.urls)),
)
