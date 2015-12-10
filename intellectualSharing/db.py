from py2neo import *

authenticate('localhost:7474', 'neo4j', 'django')
g = Graph()

# Wrapping py2neo to give a domain-specific interface for our application

def isDefinedType(typeName):
	if g.find_one("__" + typeName) == None:
		return False
	else:
		return True
	
def createNode(typeName, name, description):
	node = Node(typeName, name=name, description=description)
	g.create(node)


def createRelationship(nodeFrom, relationship, nodeTo):
	rel = Relationship(nodeFrom, relationship, nodeTo)
	g.create(rel)

def getNode(label, name):
	result = g.cypher.execute("MATCH (n:" + label + " {name:'" + name + "'}) RETURN n")
	order = result.to_subgraph().order
	if order == 0:
		return None
	elif order == 1:
		return result[0][0]
	else:
		return "Error multiple nodes found with name " + name + " and label " + label
		

def addDefaultType():
	pass

def enforceType():
	pass

def findType():
	pass
