from django.views.generic import View
from django.http import HttpResponse, JsonResponse

class ApiRequest(View):
	def __init__(self, *postKeys):
		self.postKeys = postKeys

	def get(self, request):
		return HttpResponse("Only POST requests supported", status=400)

	# Generate differentiators and requiredKeys from a post request
	def parsePostRequest(self, request):
		self.differentiators = {}
		self.requiredKeys = {}
		requiredKeysFound = 0
		for key in request.POST.keys():
			key = str(key)
			if key not in self.postKeys:
				self.differentiators[key] = request.POST.get(key)
			else:
				self.requiredKeys[key] = request.POST.get(key)
				requiredKeysFound++
		if len(self.postKeys) > requiredKeysFound:
			return HttpResponse("You must specify these keys: " + str(self.postKeys), status=400)
		return None