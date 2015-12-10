from py2neo import *

authenticate('localhost:7474', 'neo4j', 'django')
g = Graph()
g.delete_all()

__actor = Node("__actor")
actor = Node("actor", name='Daniel Craig')
role = Node("role")
__role = Node("__role")
character = Node("character", name='James Bond')
movie = Node("movie", name="Skyfall")

__actorHasRole = Relationship(__actor, "HAD_ROLE", __role)
actorHasRole = Relationship(actor, "HAD_ROLE", role)
rolePlayed = Relationship(role, "PLAYED", character)
roleProduction = Relationship(role, "IN_PRODUCTION_OF", movie)

g.create(actor, role, character, movie, actorHasRole, rolePlayed, roleProduction, __actor, __role, __actorHasRole)

for rel in g.match():
	print rel

print g.cypher.execute("MATCH (n) RETURN n")
