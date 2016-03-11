from ApiRequest import ApiRequest
from .. import db
from django.http import HttpResponse


class CreateTypeNode(ApiRequest):
	def __init__(self):
		super(CreateTypeNode, self).__init__(
			{
				'typeName' : 'checkName'
			}
		)

	def post(self, request):
		result = super(CreateTypeNode, self).post(request)
		if result != None:
			return result

		typeName = self.requestJson['typeName']
		[typeNode] = self.getNodes(['TypeNode', typeName])
		
		if typeNode == None:
			db.createTypeNode(typeName)
			return HttpResponse("Type Node "+typeName+" created", status=201)
		else:
			return HttpResponse("Type Node "+typeName+" exists", status=200)