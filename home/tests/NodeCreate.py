import testData
import unittest
import json
import requests

class NodeCreate(unittest.TestCase):
	def runTest(self):
		self.TestAddNode()
		self.TestAddRelationshipBetweenNodes()

	def sendAddNodeRequest(self, url, n, expected_code):
		data = {'typeName': n[0], 'properties': n[1]}
		data = json.dumps(data)
		response = requests.post(url, data)
		self.assertEqual(response.status_code, expected_code)

	def TestBadPostData(self, url, data):
		postData = {}
		for d in data:
			postData[d[0]] = d[1]
		postData = json.dumps(postData)
		response = requests.post(url, postData)
		self.assertEqual(response.status_code, 400)

	def TestAddNode(self):
		url = testData.baseurl + 'addNode'
		self.assertEqual(requests.get(url).status_code, 400)
		for n in testData.nodes:
			self.sendAddNodeRequest(url, n, 201)
			self.sendAddNodeRequest(url, n, 200)
		for n in testData.badRequestNodes:
			self.sendAddNodeRequest(url, n, 400)
		for n in testData.notFoundNodes:
			self.sendAddNodeRequest(url, n, 404)
		for n in testData.badAddNodePostData:
			self.TestBadPostData(url, n)

	def sendAddRelRequest(self, url, r, expected_code):
		data = {
			'fromType': r[0],
			'fromProperties' : r[1],
			'relName' : r[2],
			'toType' : r[3],
			'toProperties' : r[4]
		}
		d = json.dumps(data)
		response = requests.post(url, d)
		self.assertEqual(response.status_code, expected_code)

			
	def TestAddRelationshipBetweenNodes(self):
		url = testData.baseurl + 'addRelationshipBetweenNodes'
		self.assertEqual(requests.get(url).status_code, 400)
		for r in testData.rels:
			self.sendAddRelRequest(url, r, 201)
			self.sendAddRelRequest(url, r, 200)
