from django.conf.urls import patterns, include, url
from . import views

from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^addNode', views.addNode, name='addNode'),
	url(r'^addRelationship', views.addRelationshipToNodes, name="addRelationship"),
	url(r'^viewNode', views.viewNode, name='viewNode'),
    url(r'^admin/', include(admin.site.urls)),
]
