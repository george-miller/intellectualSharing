from django.http import HttpResponse
from .models import Node, Edge

def home(request):
	return HttpResponse("Hello!")

def insertNode(request):
	title = request.GET.get("title")
	description = request.GET.get("description")
	if isinstance(title, basestring) and isinstance(description, basestring):
		sameTitleNodes = Node.objects.filter(title=request.GET.get("title"))
		if len(sameTitleNodes) > 0:
			return HttpResponse("Already Nodes with this title, choose another title")
		Node.objects.create(title=title, description=description)
		return HttpResponse("Successfully created Node")
	else:
		return HttpResponse("Invalid Arguments, title and description must be strings")


#def insertEdge(request):

def getNodeId(request):
	title = request.GET.get("title")
	if isinstance(title, basestring):
		nodesFound = Node.objects.filter(title=title)
		if len(nodesFound) > 1:
			return HttpResponse("Server Error, there is two nodes of the same name: " + title)
		elif len(nodesFound) == 1:
			return HttpResponse(str(nodesFound[0].id))
		else:
			return HttpResponse("No nodes found")
	else:
		return HttpResponse("Invalid Arguments")

def getEdgeIdsFromNode(request):
	nodeId = request.GET.get("nodeId")
	if isinstance(nodeId, basestring):
		nodesFound = Node.objects.filter(id=nodeId)
		if len(nodesFound) > 1:
			return HttpResponse("Server Error, there is two nodes of the same name: " + title)
		elif len(nodesFound) == 1:
			return HttpResponse(str(nodesFound[0].edge_set.all()))
		else:
			return HttpResponse("No nodes found")
	else:
		return HttpResponse("Invalid Arguments")
