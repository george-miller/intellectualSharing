from django.http import HttpResponse
from django.shortcuts import render
import db
import nameRules

#TODO check if node/relationship is in DB before adding it.
#TODO TESTS
#TODO Strict input checking
#TODO allow reverse direction relationships

#TODO Save name with input cases, then when trying to access a node, match to any node with with the same letters regardless of case
#TODO Edit worldfromscratch

def nodeString(typeName, name):
    return "Node - " + typeName + " : " + name

def relString(relName, fromType, fromName, toType, toName):
    return "Relationship - " + relName + " from " + nodeString(fromType, fromName) + " to " + nodeString(toType, toName)

def home(request):
    return render(request, 'index.html')

# ------ NON-META API ------

# POST data must contain 'typeName' and 'name'
def addNode(request):
    if request.method != 'POST':
        return HttpResponse("Only POST requests supported", status=400)
    if not 'typeName' in request.POST or not 'name' in request.POST:
        return HttpResponse("You must specify a typeName and a name", status=400)
    typeName = request.POST.get('typeName')
    if not nameRules.isValidTypeOrRelTypeName(typeName):
        return HttpResponse(nameRules.typeRuleMessage(typeName), status=400)
    if typeName == 'TypeNode':
        return HttpResponse("You may not create a meta node with this API call, try /createTypeNode", status=400)
    typeNode = db.getTypeNode(typeName)
    if typeNode != None:
        name = request.POST.get('name')
        if not nameRules.isValidNodeName(name):
            return HttpResponse(nameRules.nodeRuleMessage(name), status=400)
        else:
            node = db.getNode(typeName, name)
            if node == None:
                db.createNode(typeName, name)
                return HttpResponse(nodeString(typeName, name)+" created", status=201)
            else:
                return HttpResponse(nodeString(typeName, name)+" exists", status=200)
    else:
        return HttpResponse("Type node not found with typeName " + typeName, status=404)

# required POST data: 'typeName', 'name', 'propName', 'propValue'           
def addPropertyToNode(request):
    if request.method != 'POST':
        return HttpResponse("Only POST requests supported", status=400)
    if (not 'typeName' in request.POST or 
        not 'name' in request.POST or
        not 'propName' in request.POST or 
        not 'propValue' in request.POST):
        return HttpResponse("You must specify a typeName, a name, a propName, and a propValue", status=400)
    typeName = request.POST.get('typeName')
    name = request.POST.get('name')
    if not nameRules.isValidTypeOrRelTypeName(typeName):
        return HttpResponse(nameRules.typeRuleMessage(typeName), status=400)
    if not nameRules.isValidNodeName(name):
        return HttpResponse(nameRules.nodeRuleMessage(name), status=400)
    node = db.getNode(typeName, name)
    if node != None:
        propName = request.POST.get('propName')
        propValue = request.POST.get('propValue')
        node[propName] = propValue
        node.push()
        return HttpResponse('Property '+propName+' : '+propValue+
            ' Added to '+nodeString(typeName, name)+' Sucessfully', status=201)
    else:
        return HttpResponse(nodeString(typeName, name)+" was not found", status=404)

# POST data must contain 'toType', 'toName', 'fromType', 'fromName', 'relName'
def addRelationshipBetweenNodes(request):
    if request.method != 'POST':
        return HttpResponse("Only POST requests supported", status=400)
    if (not 'toType' in request.POST or 
        not 'toName' in request.POST or
        not 'fromType' in request.POST or 
        not 'fromName' in request.POST or
        not 'relName' in request.POST):
        return HttpResponse("You must specify a toType, a toName, a fromType, a fromName, and a relName", status=400)
    toType = request.POST.get('toType')
    toName = request.POST.get('toName')
    fromType = request.POST.get('fromType')
    fromName = request.POST.get('fromName')
    relName = request.POST.get('relName')
    relName = relName.title()
    if not nameRules.isValidTypeOrRelTypeName(toType):
        return HttpResponse(nameRules.typeRuleMessage(toType), status=400)
    if not nameRules.isValidNodeName(toName):
        return HttpResponse(nameRules.nodeRuleMessage(toName), status=400)
    if not nameRules.isValidTypeOrRelTypeName(fromType):
        return HttpResponse(nameRules.typeRuleMessage(fromType), status=400)
    if not nameRules.isValidNodeName(fromName):
        return HttpResponse(nameRules.nodeRuleMessage(fromName), status=400)
    if not nameRules.isValidTypeOrRelTypeName(relName):
        return HttpResponse(nameRules.typeRuleMessage(relName), status=400)
    nodeTo = db.getNode(toType, toName)
    nodeFrom = db.getNode(fromType, fromName)
    if nodeTo != None and nodeFrom != None:
        # Is a realtionship with this name in the meta?
        possibleRels = db.getRelationshipTypeNamesBetweenTypeNodes(
            db.getTypeNode(fromType),
            db.getTypeNode(toType)
            )
        if relName in possibleRels:
            if db.isRelationshipBetweenNodes(nodeFrom, relName, nodeTo):
                return HttpResponse(relString(relName, fromType, fromName, toType, toName)+
                    " already exists", status=200)
            else:
                db.createRelationship(nodeFrom, relName, nodeTo)
                return HttpResponse(relString(relName, fromType, fromName, toType, toName)+
                    " created successfully!", status=201)
        else:
            # TODO make render page
            # What do we do if the relationship wasn't in the meta?
            return HttpResponse(relString(relName, fromType, fromName, toType, toName)+
                " wasn't in the meta. Possible relationships: "+str(possibleRels), status=404)
    else:
        return HttpResponse("Nodes couldn't be found: NodeFrom: "+
            nodeString(fromType, fromName)+" NodeTo: "+
            nodeString(toType, toName), status=404)

def viewNode(request, typeName, name):
    node = db.getNode(typeName, name)
    if not nameRules.isValidTypeOrRelTypeName(typeName):
        return HttpResponse(nameRules.typeRuleMessage(typeName), status=400)
    if node != None:
        return render(request, 'node.html', 
            {"nodeType": node.labels.pop(),
            "nodeName": node['name'], 
            "outgoingRels": db.getOutgoingRels(node), 
            "incomingRels": db.getIncomingRels(node)
            })
    else:
        return HttpResponse(nodeString(typeName, name)+' not found.')


# ----- META API ------

# Required POST data: 'typeName'
def createTypeNode(request):
    if request.method != 'POST':
        return HttpResponse("Only POST requests supported", status=400)
    if not 'typeName' in request.POST:
        return HttpResponse("You must specify a typeName", status=400)
    typeName = request.POST.get('typeName')
    if not nameRules.isValidTypeOrRelTypeName(typeName):
        return HttpResponse(nameRules.typeRuleMessage(typeName), status=400)
    typeNode = db.getTypeNode(typeName)
    if typeNode == None:
        db.createTypeNode(typeName)
        return HttpResponse("Type Node "+typeName+" created", status=201)
    else:
        return HttpResponse("Type Node "+typeName+" exists", status=200)

# Required POST data: 'relName'
def createRelationshipType(request):
    if request.method != 'POST':
        return HttpResponse("Only POST requests supported", status=400)
    if not 'relName' in request.POST:
        return HttpResponse("You must specify a relName", status=400)
    relName = request.POST.get('relName')
    if not nameRules.isValidTypeOrRelTypeName(relName):
        return HttpResponse(nameRules.typeRuleMessage(relName), status=400)
    relType = db.getRelationshipType(relName)
    if relType == None:
        db.createRelationshipType(relName)
        return HttpResponse("Relationship Type "+relName+" created", status=201)
    else:
        return HttpResponse("Relationship Type "+relName+" exists", status=200)

# Required POST data: 'typeFrom', 'relName', 'typeTo'
def connectTypeNodes(request):
    if request.method != 'POST':
        return HttpResponse("Only POST requests supported", status=400)
    if (not 'relName' in request.POST or
        not 'typeFrom' in request.POST or
        not 'typeTo' in request.POST):
        return HttpResponse("You must specify a relName, typeFrom, and typeTo", status=400)
    typeFrom = request.POST.get('typeFrom')
    relName = request.POST.get('relName')
    typeTo = request.POST.get('typeTo')
    if not nameRules.isValidTypeOrRelTypeName(typeFrom):
        return HttpResponse(nameRules.typeRuleMessage(typeFrom), status=400)
    if not nameRules.isValidTypeOrRelTypeName(relName):
        return HttpResponse(nameRules.typeRuleMessage(relName), status=400)
    if not nameRules.isValidTypeOrRelTypeName(typeTo):
        return HttpResponse(nameRules.typeRuleMessage(typeTo), status=400)
    typeFromNode = db.getTypeNode(typeFrom)
    typeToNode = db.getTypeNode(typeTo)
    relType = db.getRelationshipType(relName)
    if typeFromNode == None:
        return HttpResponse("Couldn't find typeFrom " + typeFrom, status=400)
    elif typeToNode == None:
        return HttpResponse("Couldn't find typeTo " + typeTo, status=400)
    elif relType == None:
        return HttpResponse("Couldn't find relType from name " + relName, status=400)
    else:
        if relType['name'] in db.getRelationshipTypeNamesBetweenTypeNodes(typeFromNode, typeToNode):
            return HttpResponse("Connection exists: " + typeFrom + " -> " + relName + " -> " + typeTo, status=200)
        else:
            db.connectTypeNodes(typeFromNode, relType, typeToNode)
            return HttpResponse("Connection created " + typeFrom + " -> " + relName + " -> " + typeTo, status=201)

def typeNodeEditor(request):
    rels = db.getRelationshipTypeNames()
    types = db.getTypeNames()
    return render(request, 'typeNodeEditor.html', {"rels":rels, "types":types})


