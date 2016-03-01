import ApiRequest

# POST data must contain 'typeName' and 'name'
class AddNode(ApiRequest):
	def __init__(self):
		super.__init__(('typeName'), ('typeName'))

	def post(self, request):
		result = super.post(request)
		if result != None:
			return result

		[typeNode, node] = viewsHelper.getNodes(
			['TypeNode', self.requiredKeys['typeName']], 
			[self.requiredKeys['typeName'], self.requiredKeys['name'], self.differentiators]
			)

	    if typeNode == None:
	        return HttpResponse("Type node not found with typeName " + typeName, status=404)
	    else:
	    	if type(node) == 'HttpResponse':
	    		return node
	        elif node == None:
	            db.createNode(typeName, name)
	            return HttpResponse(nodeString(typeName, name)+" created", status=201)
	        else:
	            return HttpResponse(nodeString(typeName, name)+" exists", status=200)