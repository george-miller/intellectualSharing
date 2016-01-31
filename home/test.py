# TERMINOLOGY
# TypeNode - Node in the meta that centralizes the defenition of a signular idea (ex. object, place, person)
# RelationshipType - Node in the meta that centralizes the defenition of a singular relationship between TypeNodes

from py2neo import *
import unittest
import requests
import db
import random

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

words = requests.get("http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain").content.splitlines()
def getRandomWord():
	return words[random.randint(0, len(words))]


types = ['actor', 'role', 'movie', 'genre', 'character', 'award']
badTypes = ['A C T', 'GG****', '[]', '|\|', ',..,']
relTypes = ['had_role', 'in_production_of', 'has_genre', 'played', 'awarded']
connections = [
	('actor', 'had_role', 'role'), 
	('role', 'in_production_of', 'movie'),
	('movie', 'has_genre', 'genre'),
	('role', 'played', 'character'),
	('actor', 'awarded', 'award'),
	('movie', 'awarded', 'award')
]

class MetaCreate(unittest.TestCase):
	def testAllWithOrder(self):
		self.TestCreateTypeNodes()
		self.TestCreateRelationshipTypes()
		self.TestConnectTypeNodes()

	def TestCreateTypeNodes(self):
		url = baseurl + 'createTypeNode'
		self.assertEqual(requests.get(url).status_code, 400)
		for t in types:
			data = {'typeName' : t}
			response = requests.post(url, data)
			self.assertEqual(response.status_code, 201)
		for t in types:
			data = {'typeName' : t}
			response = requests.post(url, data)
			self.assertEqual(response.status_code, 200)
		for t in badTypes:
			data = {'typeName' : t}
			response = requests.post(url, data)
			self.assertEqual(response.status_code, 400)

	def TestCreateRelationshipTypes(self):
		url = baseurl + 'createRelationshipType'
		self.assertEqual(requests.get(url).status_code, 400)
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
		self.assertEqual(requests.get(url).status_code, 400)
		for connection in connections:
			data = {
				'typeFrom' : connection[0],
				'relName' : connection[1],
				'typeTo' : connection[2]
			}
			response = requests.post(url, data)
			self.assertEqual(response.status_code, 201)
		for connection in connections:
			data = {
				'typeFrom' : connection[0],
				'relName' : connection[1],
				'typeTo' : connection[2]
			}
			response = requests.post(url, data)
			self.assertEqual(response.status_code, 200)

class MetaGet(unittest.TestCase):
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


nodes = [
	('actor', 'Daniel Craig'),
	('role', 'Daniel Craig In Skyfall'),
	('character', 'James Bond'),
	('movie', 'Skyfall'),
	('genre', 'action'),
	('award', 'Tony')
]
badRequestNodes = [
	('actor', '*)*#'),
	('$$', 'Moneyyy'),
	('TypeNode', 'Actor'),
	('acto r', '____')
]
notFoundNodes = [
	('poop', 'poop'),
	('actorr', 'Baddie')
]

badAddNodePostData = [
	[
		('typeName', getRandomWord()),
		(getRandomWord(), getRandomWord())
	],
	[
		(getRandomWord(), getRandomWord()),
		('name', getRandomWord())
	],
	[
		(getRandomWord(), getRandomWord()),
		(getRandomWord(), getRandomWord())
	]
]

rels = [
	('actor', 'Daniel Craig', 'had_role', 'role', 'Daniel Craig In Skyfall'),
	('role', 'Daniel Craig In Skyfall', 'played', 'character', 'James Bond'),
	('role', 'Daniel Craig In Skyfall', 'in_production_of', 'movie', 'Skyfall'),
	('movie', 'Skyfall', 'has_genre', 'genre', 'action'),
	('movie', 'Skyfall', 'awarded', 'award', 'Tony')
]
class NodeCreate(unittest.TestCase):
	def testAddNodesandRels(self):
		self.TestAddNode()
		self.TestAddRelationshipBetweenNodes()

	def sendAddNodeRequest(self, url, n, expected_code):
		data = {'typeName': n[0], 'name': n[1]}
		response = requests.post(url, data)
		self.assertEqual(response.status_code, expected_code)

	def TestBadPostData(self, url, data):
		postData = {}
		for d in data:
			postData[d[0]] = d[1]
		response = requests.post(url, postData)
		self.assertEqual(response.status_code, 400)

	def TestAddNode(self):
		url = baseurl + 'addNode'
		self.assertEqual(requests.get(url).status_code, 400)
		for n in nodes:
			self.sendAddNodeRequest(url, n, 201)
			self.sendAddNodeRequest(url, n, 200)
		for n in badRequestNodes:
			self.sendAddNodeRequest(url, n, 400)
		for n in notFoundNodes:
			self.sendAddNodeRequest(url, n, 404)
		for data in badAddNodePostData:
			self.TestBadPostData(url, data)

	def sendAddRelRequest(self, url, r, expected_code):
		data = {
			'fromType': r[0],
			'fromName' : r[1],
			'relName' : r[2],
			'toType' : r[3],
			'toName' : r[4]
		}
		response = requests.post(url, data)
		self.assertEqual(response.status_code, expected_code)

			
	def TestAddRelationshipBetweenNodes(self):
		url = baseurl + 'addRelationshipBetweenNodes'
		self.assertEqual(requests.get(url).status_code, 400)
		for r in rels:
			self.sendAddRelRequest(url, r, 201)
			self.sendAddRelRequest(url, r, 200)

if __name__ == '__main__':
	unittest.main()
