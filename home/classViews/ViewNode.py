from GetRequest import GetRequest
from django.http import HttpResponse
from .. import db
from django.shortcuts import render


class ViewNode(GetRequest):
	def __init__(self):
		super(ViewNode, self).__init__(
			{
				'typeName' : 'checkName',
				'name' : 'dontCheck'
			}
		)

	def get(self, request):
		result = super(ViewNode, self).get(request)
		if result != None:
			return result

		typeName = self.request['typeName']
		properties = self.request
		del properties['typeName']

		[typeNode, node] = self.getNodes(['TypeNode', typeName], [typeName, properties])

		if typeNode == None:
			return HttpResponse("Type node not found with typeName " + typeName, status=404)
		else:
			if node != None:
				return render(request, 'node.html',
				{
					'node': node,
					"outgoingRels": db.getOutgoingRels(node),
					"incomingRels": db.getIncomingRels(node)
				})
			else:
				return HttpResponse(self.nodeString(typeName, properties)+' not found.', status=404)