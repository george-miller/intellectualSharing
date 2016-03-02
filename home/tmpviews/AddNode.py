import ApiRequest
from .. import db
from django.http import HttpResponse, JsonResponse

# POST data must contain 'typeName' and 'name'
class AddNode(ApiRequest.ApiRequest):
	def __init__(self):
		super(AddNode, self).__init__(['typeName'], ['name'], ['typeName'])

	def post(self, request):
		result = super(AddNode, self).post(request)
		if result != None:
			return result
		typeName = self.requiredKeys['typeName']
		if typeName == 'TypeNode' or typeName == 'RelationshipType':
			return HttpResponse("You cannot create meta nodes with this url, try /createTypeNode", status=400)

		[typeNode, node] = self.getNodes(
			['TypeNode', typeName], 
			[typeName, self.properties]
			)

		if typeNode == None:
			return HttpResponse("Type node not found with typeName " + typeName, status=404)
		else:
			if node == None:
				db.createNode(typeName, self.properties)
				return HttpResponse(self.nodeString(typeName, self.properties)+" created", status=201)
			else:
				return HttpResponse(self.nodeString(typeName, self.properties)+" exists", status=200)