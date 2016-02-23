from django.http import HttpResponse, JsonResponse
import db

# Can only have letters, numbers and '_'
def isValidTypeOrRelTypeName(typeName):
	letters = list(typeName)
	for letter in letters:
		if not letter.isalnum() and not letter == '_':
			return False
	return True

# All typeNames and relTypes are title case
def fixTypeOrRelTypeNameCases(typeName):
	return typeName.title()

def typeRuleMessage(typeName):
	return "Invalid Type Name: "+typeName+".  Types must only contain letters, numbers, and underscores"

def parsePostRequest(request, *keys):
	if request.method != 'POST':
		return (False, HttpResponse("Only POST requests supported", status=400))
	differentiators = {}
	keyValues = []
	keysFound = 0
	for key in request.POST.keys():
		key = str(key)
		if key not in keys:
			differentiators[key] = request.POST.get(key)
		else:
			keyValues.append(request.POST.get(key))
			keysFound += 1

	if len(keys) > keysFound:
		keyValues = (False, HttpResponse("You must specify these keys: " + str(keys), status=400))

	return (keyValues, differentiators)	

def checkNames(*names):
	for name in names:
		if not isValidTypeOrRelTypeName(name):
			return HttpResponse(typeRuleMessage(name), status=400)
	return True

def multipleNodesFound(requestDict, nodeList):
	hitsPerNode = []
	for i in range(len(nodeList)):
		hitsPerNode.append(0)
		for key in nodeList[i].properties.keys():
			if key in requestDict:
				if nodeList[i].properties[key] == requestDict[key]:
					hitsPerNode[i] += 1

	maxHit = max(hitsPerNode)
	maxPositions = [i for i,j in enumerate(hitsPerNode) if j==maxHit] # generates list of positions of maxes
	if len(maxPositions) == 1:
		return nodeList[maxPositions[0]]
	else:
		nodesWithSameHits = []
		for position in maxPositions:
			nodesWithSameHits.append(nodeList[position])
		#return HttpResponse("Couldn't differentiate between nodes: " + str(nodesWithSameHits), status=409)
		return None


def getNodes(onlySuperset, differentiators, *nodes):
	nodesToReturn = []
	for node in nodes:
		if node[0] == 'TypeNode':
			nodesToReturn.append(db.getTypeNode(node[1]))
		elif node[0] == 'RelationshipType':
			nodesToReturn.append(db.getRelationshipType(node[1]))
		else:
			nodesToReturn.append(getNonMetaNode(onlySuperset, differentiators, db.getNode(node[0], node[1])))
	return nodesToReturn

def getNonMetaNode(onlySuperset, differentiators, node):
	if type(node) == type([]):
		return multipleNodesFound(differentiators, node)
	elif onlySuperset and node != None and isDifferent(differentiators, node):
		print differentiators
		print node
		return None
	else:
		return node

def isDifferent(differentiators, node):
	for key in differentiators.keys():
		if key not in node.properties.keys():
			return True
	return False