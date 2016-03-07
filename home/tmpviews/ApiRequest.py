from django.views.generic import View
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils.decorators import method_decorator
from .. import db

@method_decorator(csrf_exempt, name='dispatch')
class ApiRequest(View):
	def __init__(self, sampleRequest):
		self.sampleRequest = sampleRequest
		self.namesToCheck = []

		for key in sampleRequest.keys():
			if sampleRequest[key] == 'checkName':
				self.namesToCheck.append(key)


	def get(self, request):
		return HttpResponse("Only POST requests supported", status=400)

	def post(self, request):
		result = self.parsePostRequest(request)
		if result != None:
			return result

		itemsToCheck = []
		for name in self.namesToCheck:
			itemsToCheck.append(self.requestJson[name])
		result = self.checkNames(itemsToCheck)
		if result != None:
			return result

		return None

	def getNodes(self, *nodes):
		nodesToReturn = []
		for node in nodes:
			nodeResult = None
			if node[0] == 'TypeNode':
				nodeResult = db.getTypeNode(node[1])
			elif node[0] == 'RelationshipType':
				nodeResult = db.getRelationshipType(node[1])
			else:
				nodeResult = db.getNode(node[0], node[1])
			nodesToReturn.append(nodeResult)
		return nodesToReturn

	# Generate differentiators and requiredKeys from a post request
	def parsePostRequest(self, request):
		self.requestJson = json.loads(request.body)

		for key in self.sampleRequest:
			if key not in self.requestJson:
				return HttpResponse("You must specify these keys: " + str(self.sampleRequest.keys()), status=400)
			if isinstance(self.sampleRequest[key], dict):
				for innerKey in self.sampleRequest[key]:
					if innerKey not in self.requestJson[key]:
						return HttpResponse("You must specify these inner keys: " + str(self.sampleRequest[key]) + " for this key: "+key, status=400)
		
		return None

	def checkNames(self, names):
		for name in names:
			if not self.isValidTypeOrRelTypeName(name):
				return HttpResponse(self.typeRuleMessage(name), status=400)
		return None

	def isValidTypeOrRelTypeName(self, typeName):
		letters = list(typeName)
		for letter in letters:
			if not letter.isalnum() and not letter == '_':
				return False
		return True

	def typeRuleMessage(self, typeName):
		return "Invalid Type Name: "+typeName+".  Types must only contain letters, numbers, and underscores"

	def nodeString(self, typeName, properties):
	    return "Node - " + typeName + " : " + str(properties)

	def relString(self, relName, fromType, fromProps, toType, toProps):
	    return "Relationship - " + relName + " from " + self.nodeString(fromType, fromProps) + " to " + self.nodeString(toType, toProps)
