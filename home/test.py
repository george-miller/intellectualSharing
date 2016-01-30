# TERMINOLOGY
# TypeNode - Node in the meta that centralizes the defenition of a signular idea (ex. object, place, person)
# RelationshipType - Node in the meta that centralizes the defenition of a singular relationship between TypeNodes

from py2neo import *
import unittest
import requests
import db

# Setup, making sure everything responds correctly
if (raw_input("This will DELETE your WHOLE database.  Continue? (y/n): ") != 'y'):
	exit()

baseurl = "http://localhost:8000/"

try:
	result = requests.get(baseurl).status_code
except:
	print "Server isn't responding at " + baseurl
	exit()
else:
	if result != 200:
		print "Server didn't give 200 response " + baseurl
		exit()
try:
	db.g = Graph('http://neo4j:django@127.0.0.1:7474/db/data')
	db.g.delete_all()
except:
	print "Neo4j server isn't running, please start it on port 7474"
	exit()


types = ['actor', 'role', 'movie', 'genre', 'character', 'award']
relTypes = ['had_role', 'in_production_of', 'has_genre', 'played', 'awarded']
connections = [
	('actor', 'had_role', 'role'), 
	('role', 'in_production_of', 'movie'),
	('movie', 'has_genre', 'genre'),
	('role', 'played', 'character'),
	('actor', 'awarded', 'award'),
	('movie', 'awarded', 'award')
]

class TestMetaCreate(unittest.TestCase):
	def testAllWithOrder(self):
		self.TestCreateTypeNodes()
		self.TestCreateRelationshipTypes()
		self.TestConnectTypeNodes()

	def TestCreateTypeNodes(self):
		url = baseurl + 'createTypeNode'
		for t in types:
			data = {'typeName' : t}
			response = requests.post(url, data)
			self.assertEqual(response.status_code, 201)
		for t in types:
			data = {'typeName' : t}
			response = requests.post(url, data)
			self.assertEqual(response.status_code, 200)

	def TestCreateRelationshipTypes(self):
		url = baseurl + 'createRelationshipType'
		for r in relTypes:
			data = {'relName' : r}
			response = requests.post(url, data)
			self.assertEqual(response.status_code, 201)
		for r in relTypes:
			data = {'relName' : r}
			response = requests.post(url, data)
			self.assertEqual(response.status_code, 200)

	def TestConnectTypeNodes(self):
		url = baseurl + 'connectTypeNodes'
		for connection in connections:
			data = {
				'typeFrom' : connection[0],
				'relName' : connection[1],
				'typeTo' : connection[2]
			}
			response = requests.post(url, data)
			self.assertEqual(response.status_code, 201)

class TestMetaGet(unittest.TestCase):
	def testTypeNodes(self):
		for t in types:
			t = t.title()
			self.assertEqual(db.getTypeNode(t)['name'], t)

	def testGetRelTypes(self):
		for r in relTypes:
			r = r.title()
			self.assertEqual(db.getRelationshipType(r)['name'], r)

	def testGetRelBetweenTypes(self):
		for c in connections:
			typeFrom = db.getTypeNode(c[0].title())
			typeTo = db.getTypeNode(c[2].title())
			self.assertEqual(
				db.getRelationshipTypeNameBetweenTypeNodes(typeFrom, typeTo),
				c[1].title()
			)

# class testNodeCreate(unittest.TestCase)




#CREATE META

# TypeActor = db.createTypeNode('actor')
# TypeRole = db.createTypeNode('role')
# TypeMovie = db.createTypeNode('movie')
# TypeGenre = db.createTypeNode('genre')
# TypeCharacter = db.createTypeNode('character')
# TypeAward = db.createTypeNode('award')

# RelHadRole = db.createRelationshipType('HAD_ROLE')
# RelInProductionOf = db.createRelationshipType('IN_PRODUCTION_OF')
# RelHasGenre = db.createRelationshipType('HAS_GENRE')
# RelPlayed = db.createRelationshipType('PLAYED')
# RelAwarded = db.createRelationshipType('AWARDED')

# db.connectTypeNodes(TypeActor, RelHadRole, TypeRole)
# db.connectTypeNodes(TypeRole, RelInProductionOf, TypeMovie)
# db.connectTypeNodes(TypeMovie, RelHasGenre, TypeGenre)
# db.connectTypeNodes(TypeRole, RelPlayed, TypeCharacter)
# db.connectTypeNodes(TypeActor, RelAwarded, TypeAward)
# db.connectTypeNodes(TypeMovie, RelAwarded, TypeAward)

# #CREATE instance of meta
# actor = db.createNode('actor', 'Daniel Craig')
# role = db.createNode("role", "Daniel Craig")
# character = db.createNode("character", 'James Bond')
# movie = db.createNode("movie", "Skyfall")

# actorHasRole = db.createRelationship(actor, "HAD_ROLE", role)
# rolePlayed = db.createRelationship(role, "PLAYED", character)
# roleProduction = db.createRelationship(role, "IN_PRODUCTION_OF", movie)

# db.g.create(actor, role, character, movie, actorHasRole, rolePlayed, roleProduction)

# class TestDbApi(unittest.TestCase):
	
# 	def testGetTypeNode(self):
# 		self.assertEqual(db.getTypeNode('actor'), TypeActor)
# 		self.assertEqual(db.getTypeNode('role'), TypeRole)
	
# 	def testGetNode(self):
# 		self.assertEqual(db.getNode('actor', 'Daniel Craig'), actor)
# 		self.assertEqual(db.getNode('role', 'Daniel Craig'), role)
# 		self.assertEqual(db.getNode('character', 'James Bond'), character)
# 		self.assertEqual(db.getNode('movie', 'Skyfall'), movie)

# 	def testGetOutgoingRels(self):
# 		rels = db.getOutgoingRels(role)
# 		self.assertIn((u'IN_PRODUCTION_OF', u'movie', u'Skyfall'), rels)
# 		self.assertIn((u'PLAYED', u'character', u'James Bond'), rels)

# 	def testGetIncomingRels(self):
# 		self.assertIn((u'HAD_ROLE', u'actor', u'Daniel Craig'), db.getIncomingRels(role))



# for rel in db.g.match():
# 	print rel

# print db.g.cypher.execute("MATCH (n) RETURN n")

if __name__ == '__main__':
	unittest.main()
