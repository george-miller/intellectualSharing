import ApiRequest

# POST data must contain 'typeName' and 'name'
class AddPropToNode(ApiRequest):
	def __init__(self):
		super.__init__('typeName', 'name')

	def post(self, request):
		result = self.parsePostRequest(request)
		if result != None:
			return result

		result = self.checkNames(self.requiredKeys['typeName'])
		if result != None:
			return result

		[typeNode, node] = viewsHelper.getNodes(request, 
			['TypeNode', self.requiredKeys['typeName']], 
			[self.requiredKeys['typeName'], self.requiredKeys['name']])

	    if typeNode == None:
	        return HttpResponse("Type node not found with typeName " + typeName, status=404)
	    else:
	        if node == None:
	            db.createNode(typeName, name)
	            return HttpResponse(nodeString(typeName, name)+" created", status=201)
	        else:
	            return HttpResponse(nodeString(typeName, name)+" exists", status=200)