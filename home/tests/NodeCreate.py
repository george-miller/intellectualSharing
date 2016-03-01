import testData
import unittest
import requests

class NodeCreate(unittest.TestCase):
	def runTest(self):
		self.TestAddNode()
		self.TestAddRelationshipBetweenNodes()

	def sendAddNodeRequest(self, url, n, expected_code):
		data = {'typeName': n[0], 'name': n[1]}
		# If this node has properties, add them to the request
		if len(n) == 3:
			for key in n[2].keys():
				data[key] = n[2][key]
		response = requests.post(url, data)
		self.assertEqual(response.status_code, expected_code)

	def TestBadPostData(self, url, data):
		postData = {}
		for d in data:
			postData[d[0]] = d[1]
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
		for data in testData.badAddNodePostData:
			self.TestBadPostData(url, data)

	def sendAddRelRequest(self, url, r, expected_code):
		data = {
			'fromType': r[0],
			'fromName' : r[1],
			'relName' : r[2],
			'toType' : r[3],
			'toName' : r[4]
		}
		if len(r) == 6:
			for key in r[5].keys():
				data[key] = r[5][key]
		response = requests.post(url, data)
		self.assertEqual(response.status_code, expected_code)

			
	def TestAddRelationshipBetweenNodes(self):
		url = testData.baseurl + 'addRelationshipBetweenNodes'
		self.assertEqual(requests.get(url).status_code, 400)
		for r in testData.rels:
			self.sendAddRelRequest(url, r, 201)
			self.sendAddRelRequest(url, r, 200)
