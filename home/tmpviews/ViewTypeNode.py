from GetRequest import GetRequest
from .. import db
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render


class ViewTypeNode(GetRequest):
	def __init__(self):
		super(ViewTypeNode, self).__init__(
			{
				'typeName' : 'checkName'
			}
		)

	def get(self, request):
		result = super(ViewTypeNode, self).get(request)
		if result != None:
			return result

		typeName = self.request['typeName']

		nodes = db.getNodesByType(typeName)
		if nodes != []:
			return render(request, 'nodes.html',{'nodes': nodes, 'nodeType': typeName})
		else:
			return HttpResponse(nodeString(typeName, name)+' not found.', status=404)