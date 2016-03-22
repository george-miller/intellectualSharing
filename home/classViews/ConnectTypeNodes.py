from ApiRequest import ApiRequest
from .. import db
from django.http import HttpResponse

class ConnectTypeNodes(ApiRequest):
	def __init__(self):
		super(ConnectTypeNodes, self).__init__(
			{
				'typeFrom' : 'checkName',
				'relName' : 'checkName',
				'typeTo' : 'checkName'
			}
		)

	def post(self, request):
		result = super(ConnectTypeNodes, self).post(request)
		if result != None:
			return result

		typeFrom = self.requestJson['typeFrom']
		typeTo = self.requestJson['typeTo']
		relName = self.requestJson['relName']
		[typeFromNode, typeToNode, relType] = self.getNodes(['TypeNode', typeFrom], ['TypeNode', typeTo], ['RelationshipType', relName])

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