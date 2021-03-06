import testData
import unittest
from .. import db
import requests
import json

class MetaGet(unittest.TestCase):
	def runTest(self):
		self.testTypeNodes()
		self.testGetRelTypes()
		self.testGetRelTypes()
		self.testGetRelationshipDict()

	def testTypeNodes(self):
		for t in testData.types:
			t = t.title()
			self.assertEqual(db.getTypeNode(t)['name'], t)

	def testGetRelTypes(self):
		for r in testData.relTypes:
			r = r.title()
			self.assertEqual(db.getRelationshipType(r)['name'], r)

	def testGetRelBetweenTypes(self):
		for c in testData.connections:
			typeFrom = db.getTypeNode(c[0].title())
			typeTo = db.getTypeNode(c[2].title())
			self.assertIn(
				c[1].title(),
				db.getRelationshipTypeNamesBetweenTypeNodes(typeFrom, typeTo)
			)

	def testGetRelationshipDict(self):
		response = requests.post(testData.baseurl+'getRelationshipDict', json.dumps({'typeName': 'Movie'}))
		json_response = json.loads(response.text)
		self.assertDictEqual(json_response, testData.movieRelationshipDict)