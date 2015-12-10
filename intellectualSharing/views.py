from django.http import HttpResponse
import db

def home(request):
	return HttpResponse("Welcome to intellectualSharing API!")

def addNode(request):
	typeName = request.POST.get('typeName')
	if not isinstance(typeName, basestring):
		return HttpResponse("Typename must be a string")
	if typeName[:2] == db.centralPrefix:
		return HttpResponse("You may not create a central node form this API")

	typeNode = db.getCentralType(db.centralPrefix + request.POST.get('typeName'))
	if typeNode != None:
		name = request.POST.get('name')
		description = request.POST.get('description')
		if isinstance(description, basestring) and isinstance(name, basestring):
			db.createNode(typeName, name, description)
			return HttpResponse("Node created")
		else:
			return HttpResponse("name and description must be strings")
	else:
		return HttpResponse("Type node not found " + typeNode + ".  Would you like to add it to the meta?")
			
#def addPropertyToNode(request):

def addRelationshipToNodes(request):
	nodeTo = db.getNode(request.POST.get('nodeToType'), request.POST.get('nodeToName'))
	nodeFrom = db.getNode(request.POST.get('nodeFromType'), request.POST.get('nodeFromName'))
	if nodeTo != None and nodeFrom != None:
		relationshipName = request.POST.get('relationshipName')
		if isinstance(relationshipName, basestring):
			if db.isRelationshipOnTypeNode(relationshipName, request.POST.get('nodeFromType'), request.POST.get('nodeToType')):
				db.createRelationship(nodeFrom, relationshipName, nodeTo)
				return HttpResponse("Relationship created successfully")
			else:
				# What do we do if the relationship wasn't on the type node?
				return HttpResponse("Relationship wasn't on central typeNode, would you like to add it to the meta?")

		else:
			return HttpResponse("relationshipName must be a string")
	
	else:
		return HttpResponse("Nodes couldn't be found" + str(nodeTo) + str(nodeFrom))

def viewNode(request):
	node = db.getNode(request.GET.get('type'), request.GET.get('name'))
	if node != None:
		# render a page, giving the page the node object to use
		return HttpResponse(str(node))
	else:
		return HttpResponse("nodeTitle and nodeName must be strings" + str(node))

