from django.conf.urls import patterns, include, url
from . import views

from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.home, name='home'),
    
    # NON META API
    url(r'^addNode', views.addNode, name='addNode'),
    url(r'^addRelationshipBetweenNodes', views.addRelationshipBetweenNodes, name="addRelationshipBetweenNodes"),
    url(r'^addPropertyToNode', views.addPropertyToNode, name='addPropertyToNode'),

    #Node Lookup URL with label and id variables
    url(r'^viewNode$', views.viewNode, name='viewNode'),
    url(r'^viewNodeType$', views.viewNodeType, name='viewNodeType'),

    # META API
    url(r'^typeNodeEditor', views.typeNodeEditor, name='typeNodeEditor'),
    url(r'^createTypeNode', views.createTypeNode, name='createTypeNode'),
    url(r'^createRelationshipType', views.createRelationshipType, name='createRelationshipType'),
    url(r'^connectTypeNodes', views.connectTypeNodes, name='connectTypeNodes'),
    url(r'^getRelationshipDict', views.getRelationshipDict, name='getRelationshipDict'),
]
