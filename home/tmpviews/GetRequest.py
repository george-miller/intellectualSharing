from django.views.generic import View
from django.http import HttpResponse
import json
from .. import db

class GetRequest(View):
	def __init__(self, sampleRequest):
		self.sampleRequest = sampleRequest
		self.namesToCheck = []

		for key in sampleRequest.keys():
			if sampleRequest[key] == 'checkName':
				self.namesToCheck.append(key)


	def post(self, request):
		return HttpResponse("Only GET requests supported", status=400)

	def get(self, request):
		result = self.parseGetRequest(request)
		if result != None:
			return result

		itemsToCheck = []
		for name in self.namesToCheck:
			itemsToCheck.append(self.request[name])
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
	def parseGetRequest(self, request):
		self.request = {}
		for key in request.GET.keys():
			self.request[key] = request.GET.get(key)

		print self.request
		for key in self.sampleRequest:
			if key not in self.request:
				return HttpResponse("You must specify these keys: " + str(self.sampleRequest.keys()), status=400)
			 
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
