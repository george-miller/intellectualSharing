from ApiRequest import ApiRequest
from .. import db
from django.http import HttpResponse

class CreateRelationshipType(ApiRequest):
	def __init__(self):
		super(CreateRelationshipType, self).__init__(
			{
				'relName' : 'checkName'
			}
		)

	def post(self, request):
		result = super(CreateRelationshipType, self).post(request)
		if result != None:
			return result
			
		relName = self.requestJson['relName']
		[relType] = self.getNodes(['RelationshipType', relName])
		if relType == None:
			db.createRelationshipType(relName)
			return HttpResponse("Relationship Type "+relName+" created", status=201)
		else:
			return HttpResponse("Relationship Type "+relName+" exists", status=200)