import testData
import unittest
import requests
from .. import requestRules
from .. import db

class RequestRulesTest(unittest.TestCase):
	def runTest(self):
		db.createTypeNode("Movie")
		self.twoNodes = db.getTypeNode("Movie")
		self.twoNodes[0]['helper'] = 'Fucntion'
		self.twoNodes[0].push()
		self.testTwoNodesFound()
		thirdMovie = db.createTypeNode("Movie")
		self.threeNodes = self.twoNodes
		self.threeNodes.append(thirdMovie)
		self.threeNodes[2]['example'] = 'property'
		self.threeNodes[2].push()
		self.testThreeNodesFound()

	def testTwoNodesFound(self):
		result = requestRules.multipleNodesFound(testData.multipleNodesRequestDict, self.twoNodes)
		self.assertEqual(result, None)
		testData.multipleNodesRequestDict['helper'] = 'Fucntion'
		result = requestRules.multipleNodesFound(testData.multipleNodesRequestDict, self.twoNodes)
		self.assertEqual(result, self.twoNodes[0])
		del testData.multipleNodesRequestDict['helper']

	def testThreeNodesFound(self):
		result = requestRules.multipleNodesFound(testData.multipleNodesRequestDict, self.twoNodes)
		self.assertEqual(result, None)
		testData.multipleNodesRequestDict['example'] = 'property'
		result = requestRules.multipleNodesFound(testData.multipleNodesRequestDict, self.twoNodes)
		self.assertEqual(result, self.threeNodes[2])