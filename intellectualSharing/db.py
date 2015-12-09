from py2neo import *

authenticate('localhost:7474', 'neo4j', 'george')
g = Graph()

# Wrapping py2neo to give a domain-specific interface for our application

def addNode(typeName, name, description):
	# ensure that __central_typeName exists, if it doesn't return it must be created
	pass

def addRel():
	pass

def addDefaultType():
	pass

def enforceType():
	pass

def findType():
	pass
