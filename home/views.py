from django.http import HttpResponse
from django.shortcuts import render
import db

#TODO Allow creation of typeTo, rel, typeFrom simulataniously also with arbitrary number of relationships
#TODO Edit worldfromscratch

def home(request):
    return render(request, 'index.html')

# POST data must contain 'typeName', 'name', and 'description'
def addNode(request):
	typeName = request.POST.get('typeName')
	if not isinstance(typeName, basestring):
		return HttpResponse("Typename must be a string")
	if typeName == 'TypeNode':
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
			
def addPropertyToNode(request):
	nodeType = request.POST.get('type')
	name = request.POST.get('name')
	propName = request.POST.get('propName')
	propValue = request.POST.get('propValue')
	if areElementsString(nodeType, name, propName):
		node = db.getNode(nodeType, name)
		if node == None:
			return HttpResponse('No node found')
		else:
			node[propName] = propValue
			node.push()
			return HttpResponse('Property Added Sucessfully')
	else:
		return HttpResponse("type, name, and propName must be strings")

# POST data must contain 'nodeToType', 'nodeToName',
# 'nodeFromType', 'nodeFromName', relationshipName
def addRelationshipToNodes(request):
	if not areElementsString(request.POST.get('nodeToType'), 
		request.POST.get('nodeToName'), request.POST.get('nodeFromType'), 
		request.POST.get('nodeFromName')):
		return HttpResponse('nodeToType, nodeToName, nodeFromType, nodeFromName must be strings')
	nodeTo = db.getNode(request.POST.get('nodeToType'), request.POST.get('nodeToName'))
	nodeFrom = db.getNode(request.POST.get('nodeFromType'), request.POST.get('nodeFromName'))
	if nodeTo != None and nodeFrom != None:
		relationshipName = request.POST.get('relationshipName')
		if isinstance(relationshipName, basestring):
			if db.isRelationshipOnTypeNode(relationshipName, request.POST.get('nodeFromType'), request.POST.get('nodeToType')):
				db.createRelationship(nodeFrom, relationshipName, nodeTo)
				return HttpResponse("Relationship created successfully")
			else:
				# TODO make render page
				# What do we do if the relationship wasn't on the type node?
				return HttpResponse("Relationship wasn't on central typeNode, would you like to add it to the meta?")

		else:
			return HttpResponse("relationshipName must be a string")
	
	else:
		return HttpResponse("Nodes couldn't be found" + str(nodeTo) + str(nodeFrom))

def addMetaNode(request):
    rels = db.getRelationshipNames()
    types = db.getTypeNames()
    if request.method == 'POST':
        newTypeName = request.POST.get('typeName')
        numberOfRels = int(request.POST.get('numberOfRels'))
        if newTypeName != "":
            # if a type already exists that's fine, maybe we want to add relatinships to it
            if db.getTypeNode(newTypeName) == None:
                db.createTypeNode(newTypeName)
        else:
            return render(request, 'addMetaNode.html', 
                {"rels":rels, "types":types, "error":"Node must have a name"})

        if numberOfRels == 0:
            return render(request, 'addMetaNode.html', 
                {"rels":rels, "types":types, "error":"Node created successfully!"})
        for i in range(numberOfRels):
            relName = request.POST.get('rel'+str(i))
            typeName = request.POST.get('type'+str(i))
            typeNode = db.getTypeNode(typeName)
            if typeNode == None:
                db.createTypeNode(typeName)
            relType = db.getRelationshipType(relName)
            if relType == None:
                db.createRelationshipType(newTypeName, relName, typeName)
            else:
                db.connectTypeNodes(newTypeName, relName, typeName)

        return render(request, 'addMetaNode.html', 
            {"rels":rels, "types":types, "error":"Nodes and Relationships created successfully!"})
    else:
        return render(request, 'addMetaNode.html', {"rels":rels, "types":types})

def viewNode(request, label, name):
    node = db.getNode(label, name)
    if node != None:
        return render(request, 'node.html', {"node": node})
    else:
        return HttpResponse('Node not found.')

def areElementsString(*args):
	for i in args:
		if not str(i).isalpha():
			return False
	return True

