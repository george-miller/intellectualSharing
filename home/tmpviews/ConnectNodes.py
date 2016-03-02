import ApiRequest
from .. import db
from django.http import HttpResponse, JsonResponse

# POST data must contain 'toType', 'toProperties', 'fromType', 'fromProperties', 'relName'
class ConnectNodes(ApiRequest.ApiRequest):
	def __init__(self):
		super(ConnectNodes, self).__init__(
			{
				'toType' : 'checkName',
				'toProperties' : ['name'],
				'fromType' : 'checkName',
				'fromProperties' : ['name'],
				'relName' : 'checkName'
			}
		)

	def post(self, request):
		result = super(ConnectNodes, self).post(request)
		if result != None:
			return result

		toType = self.requestJson['toType']
		toProperties = self.requestJson['toProperties']
		fromType = self.requestJson['fromType']
		fromProperties = self.requestJson['fromProperties']
		relName = self.requestJson['relName']
		relString = self.relString(relName, fromProperties, fromName, toType, toProperties)

		[nodeFrom, nodeTo,  fromTypeNode, toTypeNode] = self.getNodes(
			[fromType, fromProperties], [toType, toProperties], ['TypeNode', fromType], ['TypeNode', toType])

		if nodeTo != None and nodeFrom != None:
	        if fromTypeNode != None and toTypeNode != None:
	            # Is a realtionship with this name in the meta?
	            possibleRels = db.getRelationshipTypeNamesBetweenTypeNodes(
	                fromTypeNode,
	                toTypeNode
	                )
	            if relName in possibleRels:
	                if db.isRelationshipBetweenNodes(nodeFrom, relName, nodeTo):
	                    return HttpResponse(relString+" already exists", status=200)
	                else:
	                    db.createRelationship(nodeFrom, relName, nodeTo)
	                    return HttpResponse(relString+" created successfully!", status=201)
	            else:
	                # TODO make render page
	                # What do we do if the relationship wasn't in the meta?
	                return HttpResponse(relString+" wasn't in the meta. Possible relationships: "+str(possibleRels), status=404)
	        else:
	            return HttpResponse("TypeNodes couldn't be found for types: "+fromType+" and "+toType, status=404)
	    else:
	        return HttpResponse("Nodes couldn't be found: NodeFrom: "+
	            self.nodeString(fromType, fromProperties)+" NodeTo: "+
	            self.nodeString(toType, toProperties), status=404)