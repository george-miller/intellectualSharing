from django.conf.urls import patterns, include, url
from . import views
from tmpviews import AddNode, ConnectNodes, AddPropToNode, CreateTypeNode, CreateRelationshipType, ConnectTypeNodes, GetRelationshipDict, ViewNode

from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.home, name='home'),
    
    # NON META API
    url(r'^addNode', AddNode.AddNode.as_view(), name='addNode'),
    url(r'^addRelationshipBetweenNodes', ConnectNodes.ConnectNodes.as_view(), name="addRelationshipBetweenNodes"),
    url(r'^addPropertyToNode', AddPropToNode.AddPropToNode.as_view(), name='addPropertyToNode'),

    #Node Lookup URL with label and id variables
    url(r'^viewNode$', ViewNode.ViewNode.as_view(), name='viewNode'),
    url(r'^viewNodeType$', views.viewNodeType, name='viewNodeType'),

    # META API
    url(r'^typeNodeEditor', views.typeNodeEditor, name='typeNodeEditor'),
    url(r'^createTypeNode', CreateTypeNode.CreateTypeNode.as_view(), name='createTypeNode'),
    url(r'^createRelationshipType', CreateRelationshipType.CreateRelationshipType.as_view(), name='createRelationshipType'),
    url(r'^connectTypeNodes', ConnectTypeNodes.ConnectTypeNodes.as_view(), name='connectTypeNodes'),
    url(r'^getRelationshipDict', GetRelationshipDict.GetRelationshipDict.as_view(), name='getRelationshipDict'),
]
