from django.conf.urls import patterns, include, url
from . import views
from tmpviews import AddNode, ConnectNodes

from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.home, name='home'),
    
    # NON META API
    url(r'^addNode', AddNode.AddNode.as_view(), name='addNode'),
    url(r'^addRelationshipBetweenNodes', ConnectNodes.ConnectNodes.as_view(), name="addRelationshipBetweenNodes"),
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
