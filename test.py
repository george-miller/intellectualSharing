# to run the tests, make sure you have a test db running on port 7475 
# and if you want to run both the main db and the test db att the same time, 
# you must change the HTTPS port to something that's not 7473

from py2neo import *
from intellectualSharing import db

db.g = Graph('http://neo4j:django@127.0.0.1:7475/db/data')
db.g.delete_all()

TypeActor = Node("TypeNode", name='actor')
actor = Node("actor", name='Daniel Craig')
role = Node("role")
__role = Node("__role")
character = Node("character", name='James Bond')
movie = Node("movie", name="Skyfall")

actorHasRole = Relationship(actor, "HAD_ROLE", role)
rolePlayed = Relationship(role, "PLAYED", character)
roleProduction = Relationship(role, "IN_PRODUCTION_OF", movie)

db.g.create(actor, role, character, movie, actorHasRole, rolePlayed, roleProduction, TypeActor, __role)


for rel in db.g.match():
	print rel

print db.g.cypher.execute("MATCH (n) RETURN n")

