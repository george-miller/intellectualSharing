from django.http import HttpResponse
import db

#def findNode(request, nodeTitle):

	
def home(request):
	print request.POST.getlist('a')
	return HttpResponse("heelo")

def addNode(request):
	result = attemptTypeSearch(request.POST.get('typeName'))
	if result == True:
		name = request.POST.get('name')
		description = request.POST.get('description')
		if isinstance(description, basestring) and isinstance(name, basestring):
			db.createNode(typeName, name, description)
			return HttpResponse("Node created")
		else:
			return HttpResponse("name and description must be strings")
	else:
		return result
			
def attemptTypeSearch(typeName):
	if not isinstance(typeName, basestring):
		return HttpResponse("Type name must be a string")
	if db.isDefinedType(typeName):
		return True
	else:
		# Send to page to create type node
		return HttpResponse("Type " + typeName + " is undefined.  Define it first")

#def addPropertyToNode(request):
	
	
	

def addRelationshipToNodes(request):
	nodeTo = db.getNode(request.POST.get('nodeToLabel'), request.POST.get('nodeToName'))
	nodeFrom = db.getNode(request.POST.get('nodeFromLabel'), request.POST.get('nodeFromName'))
	if nodeTo != None and nodeFrom != None:
		relationshipName = request.POST.get('relationshipName')
		if isinstance(relationshipName, basestring):
			db.createRelationship(nodeFrom, relationshipName, nodeTo)
			return HttpResponse("Relationship created successfully")
		else:
			return HttpResponse("relationshipName must be a string")
	
	else:
		return HttpResponse("Nodes couldn't be found" + str(nodeTo) + str(nodeFrom))



def areElementsString(array):
	for thing in array:
		if not isinstance(thing, basestring):
			return False
	return True
