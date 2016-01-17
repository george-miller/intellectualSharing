# to run the tests, make sure you have a test db running on port 7475 
# and if you want to run both the main db and the test db att the same time, 
# you must change the HTTPS port to something that's not 7473

from py2neo import *
import db
import unittest

db.g = Graph('http://neo4j:django@127.0.0.1:7474/db/data')
db.g.delete_all()
	
# TERMINOLOGY
# TypeNode - Node in the meta that centralizes the defenition of a signular idea (ex. object, place, person)
# RelationshipType - Node in the meta that centralizes the defenition of a singular relationship between TypeNodes

#CREATE META
TypeActor = db.createTypeNode('actor')
TypeRole = db.createTypeNode('role')
TypeMovie = db.createTypeNode('movie')
TypeGenre = db.createTypeNode('genre')
TypeCharacter = db.createTypeNode('character')
TypeAward = db.createTypeNode('award')

RelHadRole = db.createRelationshipType('HAD_ROLE')
RelInProductionOf = db.createRelationshipType('IN_PRODUCTION_OF')
RelHasGenre = db.createRelationshipType('HAS_GENRE')
RelPlayed = db.createRelationshipType('PLAYED')
RelAwarded = db.createRelationshipType('AWARDED')

db.connectTypeNodes(TypeActor, RelHadRole, TypeRole)
db.connectTypeNodes(TypeRole, RelInProductionOf, TypeMovie)
db.connectTypeNodes(TypeMovie, RelHasGenre, TypeGenre)
db.connectTypeNodes(TypeRole, RelPlayed, TypeCharacter)
db.connectTypeNodes(TypeActor, RelAwarded, TypeAward)
db.connectTypeNodes(TypeMovie, RelAwarded, TypeAward)

#CREATE instance of meta
actor = db.createNode('actor', 'Daniel Craig')
role = db.createNode("role", "Daniel Craig")
character = db.createNode("character", 'James Bond')
movie = db.createNode("movie", "Skyfall")

actorHasRole = db.createRelationship(actor, "HAD_ROLE", role)
rolePlayed = db.createRelationship(role, "PLAYED", character)
roleProduction = db.createRelationship(role, "IN_PRODUCTION_OF", movie)

db.g.create(actor, role, character, movie, actorHasRole, rolePlayed, roleProduction)

class TestDbApi(unittest.TestCase):
	
	def testGetTypeNode(self):
		self.assertEqual(db.getTypeNode('actor'), TypeActor)
		self.assertEqual(db.getTypeNode('role'), TypeRole)
	
	def testGetNode(self):
		self.assertEqual(db.getNode('actor', 'Daniel Craig'), actor)
		self.assertEqual(db.getNode('role', 'Daniel Craig'), role)
		self.assertEqual(db.getNode('character', 'James Bond'), character)
		self.assertEqual(db.getNode('movie', 'Skyfall'), movie)

	def testGetOutgoingRels(self):
		rels = db.getOutgoingRels(role)
		self.assertIn((u'IN_PRODUCTION_OF', u'movie', u'Skyfall'), rels)
		self.assertIn((u'PLAYED', u'character', u'James Bond'), rels)

	def testGetIncomingRels(self):
		self.assertIn((u'HAD_ROLE', u'actor', u'Daniel Craig'), db.getIncomingRels(role))



for rel in db.g.match():
	print rel

print db.g.cypher.execute("MATCH (n) RETURN n")

if __name__ == '__main__':
	unittest.main()
