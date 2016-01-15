from django.http import HttpResponse
from django.shortcuts import render
import db

#TODO Save name with input cases, then when trying to access a node, match to any node with with the same letters regardless of case
#TODO Edit worldfromscratch

def home(request):
    return render(request, 'index.html')

# ------ NON-META API ------

# POST data must contain 'typeName', 'name', and 'description'
def addNode(request):
    typeName = request.POST.get('typeName').lower()
    if typeName == 'TypeNode':
        return HttpResponse("You may not create a meta node with this API call")
    typeNode = db.getTypeNode(typeName)
    if typeNode != None:
        name = request.POST.get('name')
        description = request.POST.get('description')
        if name == "" or description == "":
            return HttpResponse("name and description must not be empty")
        else:
            db.createNode(typeName, name, description)
            return HttpResponse("Node created")
    else:
        return HttpResponse("Type node not found with typeName " + typeName + ".  The type must be in the meta before adding an instance of it")
            
# required POST data: 'type', 'name', 'propName', 'propValue'           
def addPropertyToNode(request):
    node = db.getNode(request.POST.get('type').lower(), request.POST.get('name'))
    if node != None:
        node[request.POST.get('propName')] = request.POST.get('propValue')
        node.push()
        return HttpResponse('Property Added Sucessfully')
    else:
        return HttpResponse('No node found or other error occurred')


# POST data must contain 'nodeToType', 'nodeToName', 'nodeFromType', 'nodeFromName', 'relationshipName'
def addRelationshipBetweenNodes(request):
    nodeTo = db.getNode(request.POST.get('nodeToType').lower(), request.POST.get('nodeToName'))
    nodeFrom = db.getNode(request.POST.get('nodeFromType').lower(), request.POST.get('nodeFromName'))
    if nodeTo != None and nodeFrom != None:
        relationshipName = request.POST.get('relationshipName').upper()
        if relationshipName == "":
            return HttpResponse("relationshipName must not be empty")
        else:
            # Is a realtionship with this name in the meta?
            if db.getRelationshipTypeNameBetweenTypeNodes(
                db.getTypeNode(request.POST.get('nodeToType').lower()),
                db.getTypeNode(request.POST.get('nodeFromType').lower())
                ):
                db.createRelationship(nodeFrom, relationshipName, nodeTo)
                return HttpResponse("Relationship created successfully")
            else:
                # TODO make render page
                # What do we do if the relationship wasn't in the meta?
                return HttpResponse("Relationship wasn't on TypeNode, would you like to add it to the meta?")
    else:
        return HttpResponse("Nodes couldn't be found, their results were: " + str(nodeTo) + str(nodeFrom))


# ----- META API ------

# Required POST data: 'typeName'
def createTypeNode(request):
    if request.method == 'POST':
        typeName = request.POST.get('typeName').lower()
        typeNode = db.getTypeNode(typeName)
        if typeNode == None:
            db.createTypeNode(typeName)
            return HttpResponse("Type Node created")
        else:
            return HttpResponse("Type Node exists")
    else:
        rels = db.getRelationshipTypeNames()
        types = db.getTypeNames()
        return render(request, 'addMetaNode.html', {"rels":rels, "types":types})

# Required POST data: 'relName'
def createRelationshipType(request):
    if request.method == 'POST':
        relName = request.POST.get('relName').upper()
        relType = db.getRelationshipType(relName)
        if relType == None:
            db.createRelationshipType(relName)
            return HttpResponse("Relationship Type created")
        else:
            return HttpResponse("Relationship Type exists")
    else:
        return HttpResponse("Only POST requests supported")

# Required POST data: 'typeFromName', 'relName', 'typeToName'
def connectTypeNodes(request):
    if request.method == 'POST':
        typeFromName = request.POST.get('typeFromName').lower()
        relName = request.POST.get('relName').upper()
        typeToName = request.POST.get('typeToName').lower()
        typeFrom = db.getTypeNode(typeFromName)
        typeTo = db.getTypeNode(typeToName)
        relType = db.getRelationshipType(relName)
        if typeFrom == None:
            return HttpResponse("Couldn't find typeFrom")
        elif typeTo == None:
            return HttpResponse("Couldn't find typeTo")
        elif relType == None:
            return HttpResponse("Couldn't find relType")
        else:
            db.connectTypeNodes(typeNode, relType, otherTypeNode)
    else:
        return HttpResponse("Only POST requests supported")

def viewNode(request, typeName, name):
    node = db.getNode(typeName, name)
    if node != None:
        return render(request, 'node.html', {"node": node})
    else:
        return HttpResponse('Node not found.')



# KEEPING THIS FOR REFRENCE WHEN I MAKE FRONT END

        # numberOfRels = int(request.POST.get('numberOfRels'))
        # if newTypeName != "":
        #     # if a type already exists that's fine, maybe we want to add relationships to it
        #     typeNode = db.getTypeNode(newTypeName)
        #     if typeNode == None:
        #         typeNode = db.createTypeNode(newTypeName)
        # else:
        #     return render(request, 'addMetaNode.html', 
        #         {"rels":rels, "types":types, "error":"Node must have a name"})

        # if numberOfRels == 0:
        #     return render(request, 'addMetaNode.html', 
        #         {"rels":rels, "types":types, "error":"Node created successfully!"})
        # for i in range(numberOfRels):
        #     relName = request.POST.get('rel'+str(i)).lower()
        #     otherTypeName = request.POST.get('type'+str(i)).lower()
        #     otherTypeNode = db.getTypeNode(otherTypeName)
        #     if otherTypeNode == None:
        #         otherTypeNode = db.createTypeNode(otherTypeName)
        #     relType = db.getRelationshipType(relName)
        #     if relType == None:
        #         relType = db.createRelationshipType(typeNode, relName, otherTypeNode)
        #     else:
        #         db.connectTypeNodes(typeNode, relType, otherTypeNode)

        # return render(request, 'addMetaNode.html', 
        #     {"rels":rels, "types":types, "error":"Nodes and Relationships created successfully!"})

