# Can only have letters, numbers and '_'
def isValidTypeOrRelTypeName(typeName):
	letters = list(typeName)
	for letter in letters:
		if not letter.isalnum() and not letter == '_':
			return False
	return True

# Can only have letters, numbers, and spaces
def isValidNodeName(nodeName):
	letters = list(nodeName)
	for letter in letters:
		if not letter.isalnum() and not letter.isspace():
			return False
	return True

# All typeNames and relTypes are title case
def fixTypeOrRelTypeNameCases(typeName):
	return typeName.title()

def typeRuleMessage(typeName):
	return "Invalid Type Name: "+typeName+".  Types must only contain letters, numbers, and underscores"

def nodeRuleMessage(nodeName):
	return "Invalid Node Name: "+nodeName+".  Node names must only contain letters, numbers, and spaces"
