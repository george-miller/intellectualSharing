from django.http import HttpResponse
from .models import Node, Route

def findNode(request, nodeTitle):
	possibleNodes = Node.objects.filter(title=nodeTitle)
	if possibleNodes.count() < 1:
		return HttpResponse("Couldn't find node with name " + str(nodeTitle))
	elif possibleNodes.count() == 1:
		return possibleNodes[0]
	else:
		return HttpResponse("Multiple Nodes found with name " + str(nodeTitle))
	
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


def connectNodes(request):
	nodeFrom = request.GET.get('nodeFrom')
	nodeTo = request.GET.get('nodeTo')
	relationship = request.GET.get('relationship')
	if isinstance(nodeFrom, basestring) and isinstance(nodeTo, basestring) and isinstance(relationship, basestring):
		nodeFrom = findNode(request, nodeFrom)
		nodeTo = findNode(request, nodeTo)
		relationship = findNode(request, relationship)
		nodeFrom.nodes.add(relationship)
		r = Route.objects.create(nodeFrom=nodeFrom.id, nodeTo=nodeTo)
		relationship.routes.add(r)
		return HttpResponse("Nodes successfully connected")
	else:
		return HttpResponse("Invalid Arguments: nodeFrom, nodeTo, and relationship must all be strings")

def getRouteRelationships(request):
	title = request.GET.get('title')
	if isinstance(title, basestring):
		node = findNode(request, title)
		routeRelationships = node.routeRelationships()
		return HttpResponse(str(len(routeRelationships)))

	else:
		return HttpResponse('Invalid Arguments: title must be a string')
