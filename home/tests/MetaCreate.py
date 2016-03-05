import testData
import unittest
import requests, json

class MetaCreate(unittest.TestCase):
	def runTest(self):
		self.TestCreateTypeNodes()
		self.TestCreateRelationshipTypes()
		self.TestConnectTypeNodes()

	def TestCreateTypeNodes(self):
		url = testData.baseurl + 'createTypeNode'
		self.assertEqual(requests.get(url).status_code, 400)
		for t in testData.types:
			data = {'typeName' : t}
			data = json.dumps(data)
			response = requests.post(url, data)
			self.assertEqual(response.status_code, 201)
		for t in testData.types:
			data = {'typeName' : t}
			data = json.dumps(data)
			response = requests.post(url, data)
			self.assertEqual(response.status_code, 200)
		for t in testData.badTypes:
			data = {'typeName' : t}
			data = json.dumps(data)
			response = requests.post(url, data)
			self.assertEqual(response.status_code, 400)

	def TestCreateRelationshipTypes(self):
		url = testData.baseurl + 'createRelationshipType'
		self.assertEqual(requests.get(url).status_code, 400)
		for r in testData.relTypes:
			data = {'relName' : r}
			data = json.dumps(data)
			response = requests.post(url, data)
			self.assertEqual(response.status_code, 201)
		for r in testData.relTypes:
			data = {'relName' : r}
			data = json.dumps(data)
			response = requests.post(url, data)
			self.assertEqual(response.status_code, 200)

	def TestConnectTypeNodes(self):
		url = testData.baseurl + 'connectTypeNodes'
		self.assertEqual(requests.get(url).status_code, 400)
		for connection in testData.connections:
			data = {
				'typeFrom' : connection[0],
				'relName' : connection[1],
				'typeTo' : connection[2]
			}
			data = json.dumps(data)
			response = requests.post(url, data)
			self.assertEqual(response.status_code, 201)
		for connection in testData.connections:
			data = {
				'typeFrom' : connection[0],
				'relName' : connection[1],
				'typeTo' : connection[2]
			}
			data = json.dumps(data)
			response = requests.post(url, data)
			self.assertEqual(response.status_code, 200)
