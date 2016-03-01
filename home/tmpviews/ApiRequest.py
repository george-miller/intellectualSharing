from django.views.generic import View
from django.http import HttpResponse, JsonResponse
import json

class ApiRequest(View):
	def __init__(self, postKeys, namesToCheck):
		self.postKeys = postKeys
		self.namesToCheck = namesToCheck

	def get(self, request):
		return HttpResponse("Only POST requests supported", status=400)

	def post(self, request):
		result = self.parsePostRequest(request)
		if result != None:
			return result

		result = self.checkNames(self.namesToCheck)
		if result != None:
			return result

		return None

	def getNodes(*nodes):
		nodesToReturn = []
		for node in nodes:
			nodeResult = None
			if node[0] == 'TypeNode':
				nodeResult = db.getTypeNode(node[1])
			elif node[0] == 'RelationshipType':
				nodeResult = db.getRelationshipType(node[1])
			else:
				nodeResult = db.getNode(node[0], node[1])
			if type(nodeResult) == type([]):
				nodesToReturn.append(multipleNodesFound(node[2], nodeResult))
			else:
				nodesToReturn.append(nodeResult)
		return nodesToReturn

	def multipleNodesFound(differentiators, nodeList):
		hitsPerNode = []
		for i in range(len(nodeList)):
			hitsPerNode.append(0)
			for key in nodeList[i].properties.keys():
				if key in differentiators:
					if nodeList[i].properties[key] == differentiators[key]:
						hitsPerNode[i] += 1

		maxHit = max(hitsPerNode)
		maxPositions = [i for i,j in enumerate(hitsPerNode) if j==maxHit] # generates list of positions of maxes
		if len(maxPositions) == 1:
			return nodeList[maxPositions[0]]
		else:
			nodesWithSameHits = []
			for position in maxPositions:
				nodesWithSameHits.append(nodeList[position])
			return HttpResponse("Couldn't differentiate between nodes: " + str(nodesWithSameHits), status=409)

	# Generate differentiators and requiredKeys from a post request
	def parsePostRequest(self, request):
		json = json.loads(request.body)

		self.differentiators = {}
		if 'differentiators' in json.keys():
			self.differentiators = json['differentiators']

		self.requiredKeys = {}
		requiredKeysFound = 0
		for key in json.keys():
			key = str(key)
			if key in self.postKeys:
				self.requiredKeys[key] = json[key]
				requiredKeysFound++
		if len(self.postKeys) > requiredKeysFound:
			return HttpResponse("You must specify these keys: " + str(self.postKeys), status=400)
		return None

	def checkNames(names):
		for name in names:
			if not self.isValidTypeOrRelTypeName(name):
				return HttpResponse(self.typeRuleMessage(name), status=400)
		return None

	def isValidTypeOrRelTypeName(typeName):
		letters = list(typeName)
		for letter in letters:
			if not letter.isalnum() and not letter == '_':
				return False
		return True

	def typeRuleMessage(typeName):
		return "Invalid Type Name: "+typeName+".  Types must only contain letters, numbers, and underscores"
