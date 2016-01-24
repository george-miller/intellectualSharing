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
    typeName = str(request.POST.get('typeName')).title()
    if typeName == 'TypeNode':
        return HttpResponse("You may not create a meta node with this API call")
    typeNode = db.getTypeNode(typeName)
    if typeNode != None:
        name = request.POST.get('name')
        if name == "":
            return HttpResponse("name must not be empty")
        else:
            db.createNode(typeName, name)
            return HttpResponse("Node created")
    else:
        return HttpResponse("Type node not found with typeName " + typeName + ".  The type must be in the meta before adding an instance of it")
            
# required POST data: 'type', 'name', 'propName', 'propValue'           
def addPropertyToNode(request):
    node = db.getNode(str(request.POST.get('type')).title(), request.POST.get('name'))
    if node != None:
        node[request.POST.get('propName')] = request.POST.get('propValue')
        node.push()
        return HttpResponse('Property Added Sucessfully')
    else:
        return HttpResponse('No node found or other error occurred')


# POST data must contain 'nodeToType', 'nodeToName', 'nodeFromType', 'nodeFromName', 'relationshipName'
def addRelationshipBetweenNodes(request):
    nodeTo = db.getNode(str(request.POST.get('nodeToType')).title(), request.POST.get('nodeToName'))
    nodeFrom = db.getNode(str(request.POST.get('nodeFromType')).title(), request.POST.get('nodeFromName'))
    if nodeTo != None and nodeFrom != None:
        relationshipName = str(request.POST.get('relationshipName')).title()
        if relationshipName == "":
            return HttpResponse("relationshipName must not be empty")
        else:
            # Is a realtionship with this name in the meta?
            if db.getRelationshipTypeNameBetweenTypeNodes(
                db.getTypeNode(str(request.POST.get('nodeToType')).title()),
                db.getTypeNode(str(request.POST.get('nodeFromType')).title())
                ) == relationshipName:
                db.createRelationship(nodeFrom, relationshipName, nodeTo)
                return HttpResponse("Relationship created successfully")
            else:
                # TODO make render page
                # What do we do if the relationship wasn't in the meta?
                return HttpResponse("Relationship wasn't on TypeNode, would you like to add it to the meta?")
    else:
        return HttpResponse("Nodes couldn't be found, their results were: " + str(nodeTo) + str(nodeFrom))

def viewNode(request, typeName, name):
    node = db.getNode(typeName, name)
    if node != None:
        return render(request, 'node.html', 
            {"nodeType": node.labels.pop(),
            "nodeName": node['name'], 
            "outgoingRels": db.getOutgoingRels(node), 
            "incomingRels": db.getIncomingRels(node)
            })
    else:
        return HttpResponse('Node of type '+typeName+' named '+name+' not found.')


# ----- META API ------

# Required POST data: 'typeName'
def createTypeNode(request):
    if request.method == 'POST':
        typeName = str(request.POST.get('typeName')).title()
        typeNode = db.getTypeNode(typeName)
        if typeName == "":
            return HttpResponse("You must specify a name for your Type Node")
        elif typeNode == None:
            db.createTypeNode(typeName)
            return HttpResponse("Type Node "+typeName+" created")
        else:
            return HttpResponse("Type Node "+typeName+" exists")
    else:
        return HttpResponse("Only POST requests supported")

# Required POST data: 'relName'
def createRelationshipType(request):
    if request.method == 'POST':
        relName = str(request.POST.get('relName')).title()
        relType = db.getRelationshipType(relName)
        if relName == "":
            return HttpResponse("You must specify a name for your Relationship Type")
        elif relType == None:
            db.createRelationshipType(relName)
            return HttpResponse("Relationship Type "+relName+" created")
        else:
            return HttpResponse("Relationship Type "+relName+" exists")
    else:
        return HttpResponse("Only POST requests supported")

# Required POST data: 'typeFrom', 'relName', 'typeTo'
def connectTypeNodes(request):
    if request.method == 'POST':
        typeFrom = str(request.POST.get('typeFrom')).title()
        relName = str(request.POST.get('relName')).title()
        typeTo = str(request.POST.get('typeTo')).title()
        typeFromNode = db.getTypeNode(typeFrom)
        typeToNode = db.getTypeNode(typeTo)
        relType = db.getRelationshipType(relName)
        if typeFrom == None:
            return HttpResponse("Couldn't find typeFrom " + typeFrom)
        elif typeTo == None:
            return HttpResponse("Couldn't find typeTo " + typeTo)
        elif relType == None:
            return HttpResponse("Couldn't find relType from name " + relName)
        else:
            response = db.connectTypeNodes(typeFromNode, relType, typeToNode)
            return HttpResponse(response + " " + typeFrom + " -> " + relName + " -> " + typeTo)
    else:
        return HttpResponse("Only POST requests supported")

def typeNodeEditor(request):
    rels = db.getRelationshipTypeNames()
    types = db.getTypeNames()
    return render(request, 'typeNodeEditor.html', {"rels":rels, "types":types})


