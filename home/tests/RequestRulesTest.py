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
		testTwoNodesFound()

	def testTwoNodesFound(self):
		