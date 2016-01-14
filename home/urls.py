from django.conf.urls import patterns, include, url
from . import views

from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^addNode', views.addNode, name='addNode'),
    url(r'^addRelationship', views.addRelationshipToNodes, name="addRelationship"),
    url(r'^addPropertyToNode', views.addPropertyToNode, name='addPropertyToNode'),
    url(r'^admin/', include(admin.site.urls)),

    #Node Lookup URL with label and id variables
    url(r'^viewNode/(?P<label>[\w| ]+)/(?P<name>[\w| ]+)/', views.viewNode, name='viewNode'),
    url(r'^addMetaNode', views.addMetaNode, name='addMetaNode'),
]
