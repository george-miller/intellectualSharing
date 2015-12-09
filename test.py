from py2neo import *

authenticate('localhost:7474', 'neo4j', 'george')
g = Graph()
g.delete_all()

actor = Node("actor", name='Daniel Craig')
role = Node("role")
character = Node("character", name='James Bond')
movie = Node("movie", name="Skyfall")

actorHasRole = Relationship(actor, "HAD_ROLE", role)
rolePlayed = Relationship(role, "PLAYED", character)
roleProduction = Relationship(role, "IN_PRODUCTION_OF", movie)

g.create(actor, role, character, movie, actorHasRole, rolePlayed, roleProduction)

for rel in g.match():
	print rel

print g.cypher.execute("MATCH (n) RETURN n")
