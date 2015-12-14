# to run the tests, make sure you have a test db running on port 7475 
# and if you want to run both the main db and the test db att the same time, 
# you must change the HTTPS port to something that's not 7473

from py2neo import *
from intellectualSharing import db
import unittest

db.g = Graph('http://neo4j:django@127.0.0.1:7475/db/data')
db.g.delete_all()
	

TypeActor = Node("TypeNode", name='actor')
TypeRole = Node("TypeNode", name='role')
RelHadRole = Node("RelationshipType", name='HAD_ROLE')
actorToHadRole = Relationship(TypeActor, "HAS_RELATIONSHIP", RelHadRole)
actorToHadRole['nameOfRelated'] = 'role'
HadRoleToRole = Relationship(RelHadRole, 'HAS_RELATIONSHIP', TypeRole)

actor = Node("actor", name='Daniel Craig')
role = Node("role", name="Daniel Craig")
character = Node("character", name='James Bond')
movie = Node("movie", name="Skyfall")

actorHasRole = Relationship(actor, "HAD_ROLE", role)
rolePlayed = Relationship(role, "PLAYED", character)
roleProduction = Relationship(role, "IN_PRODUCTION_OF", movie)

db.g.create(actor, role, character, movie, actorHasRole, rolePlayed, roleProduction, 
	TypeActor, TypeRole, RelHadRole, actorToHadRole, HadRoleToRole)

class TestDbApi(unittest.TestCase):
	
	def testGetCentralType(self):
		self.assertEqual(db.getCentralType('actor'), TypeActor)
		self.assertEqual(db.getCentralType('role'), TypeRole)
	
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
