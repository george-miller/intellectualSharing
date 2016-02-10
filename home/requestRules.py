from django.http import HttpResponse, JsonResponse

# Can only have letters, numbers and '_'
def isValidTypeOrRelTypeName(typeName):
	letters = list(typeName)
	for letter in letters:
		if not letter.isalnum() and not letter == '_':
			return False
	return True

# All typeNames and relTypes are title case
def fixTypeOrRelTypeNameCases(typeName):
	return typeName.title()

def typeRuleMessage(typeName):
	return "Invalid Type Name: "+typeName+".  Types must only contain letters, numbers, and underscores"

def parsePostRequest(request, *keys):
	if request.method != 'POST':
		return (False, HttpResponse("Only POST requests supported", status=400))
	keyValues = []
	for key in keys:
		if not key in request.POST:
			return (False, HttpResponse("You must specify these keys: " + str(keys), status=400))
		else:
			keyValues.append(request.POST.get(key))
	return keyValues	

def checkNames(*names):
	for name in names:
		if not isValidTypeOrRelTypeName(name):
			return HttpResponse(typeRuleMessage(name), status=400)
	return True