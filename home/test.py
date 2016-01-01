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
RelHadRole = db.createRelationshipType('actor', 'HAD_ROLE', 'role')
RelInProductionOf = db.createRelationshipType('role', 'IN_PRODUCTION_OF', 'movie')
RelHasGenre = db.createRelationshipType('movie', 'HAS_GENRE', 'genre')
RelPlayed = db.createRelationshipType('role', 'PLAYED', 'character')
RelActorAwarded = db.createRelationshipType('actor', 'AWARDED', 'award')
RelMovieAwarded = db.createRelationshipType('movie', 'AWARDED', 'award')

#CREATE instance of meta
actor = db.createNode('actor', 'Daniel Craig', "He has blue eyes and blond hair")
role = db.createNode("role", "Daniel Craig", "Daniel Craig played a role")
character = db.createNode("character", 'James Bond', "A british mi6 spy who fights evil across the world!  He also gets tons of ridiculously hot girls")
movie = db.createNode("movie", "Skyfall", "This movie is about James Bond's return to his old home.")

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

	def testGetCentralRelationshipName(self):
		self.assertEqual(db.getCentralRelationshipName(TypeActor, TypeRole), 'HAD_ROLE')
	
	def testIsRelationshipOnTypeNode(self):
		self.assertEqual(db.isRelationshipOnTypeNode('HAD_ROLE', 'actor', 'role'), True)


for rel in db.g.match():
	print rel

print db.g.cypher.execute("MATCH (n) RETURN n")

if __name__ == '__main__':
	unittest.main()
