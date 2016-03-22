from ApiRequest import ApiRequest
from .. import db
from django.http import HttpResponse, JsonResponse

class GetRelationshipDict(ApiRequest):
	def __init__(self):
		super(GetRelationshipDict, self).__init__(
			{
				'typeName' : 'checkName'
			}
		)

	def post(self, request):
		result = super(GetRelationshipDict, self).post(request)
		if result != None:
			return result

		typeName = self.requestJson['typeName']
		[typeNode] = self.getNodes(['TypeNode', typeName])
		if typeNode == None:
			return HttpResponse("TypeNode "+typeName+" couldn't be found", status=404)
		else:
			return JsonResponse(db.getRelationshipDict(typeNode), status=200)