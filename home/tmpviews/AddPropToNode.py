import ApiRequest
from django.http import HttpResponse, JsonResponse


# POST data must contain 'typeName' and 'name'
class AddPropToNode(ApiRequest.ApiRequest):
	def __init__(self):
		super(AddPropToNode, self).__init__(
			{
				'typeName' : 'checkName',
				'properties' : ['name'],
				'newProperties' : 'dontCheck'
			}
		)

	def post(self, request):
		result = super(AddPropToNode, self).post(request)
		if result != None:
			return result

		typeName = self.requestJson['typeName']
		properties = self.requestJson['properties']

		[typeNode, node] = self.getNodes(
			['TypeNode', typeName], 
			[typeName, properties]
			)

		if typeNode == None:
			return HttpResponse("Type node not found with typeName " + typeName, status=404)
		else:
			if node == None:
				return HttpResponse(self.nodeString(typeName, properties)+" not found", status=404)
			else:
				newProperties = self.requestJson['newProperties']
				for key in newProperties.keys():
					node[key] = newProperties[key]
				node.push()
				return HttpResponse("Added Properties: " + str(newProperties) + 
					" to " +self.nodeString(typeName, properties), status=201)