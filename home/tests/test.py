# TERMINOLOGY
# TypeNode - Node in the meta that centralizes the defenition of a signular idea (ex. object, place, person)
# RelationshipType - Node in the meta that centralizes the defenition of a singular relationship between TypeNodes

from py2neo import *
import unittest
import requests
from .. import db
from . import data, MetaCreate, MetaGet, NodeCreate
from colorama import init
from colorama import Fore, Back, Style
init()

def runTests():
	# Setup, making sure everything responds correctly
	if (raw_input("This will DELETE your WHOLE database.  Continue? (y/n): ") != 'y'):
		return 0

	try:
		result = requests.get(data.baseurl).status_code
	except:
		print "Server isn't responding at " + data.baseurl
		return 1
	else:
		if result != 200:
			print "Server didn't give 200 response " + data.baseurl
			return 1
	try:
		db.g = Graph('http://neo4j:django@127.0.0.1:7474/db/data')
		db.g.delete_all()
	except:
		print "Neo4j server isn't running, please start it on port 7474"
		return 1


	suite = unittest.TestSuite()
	suite.addTests((
		MetaCreate.MetaCreate(), 
		MetaGet.MetaGet(), 
		NodeCreate.NodeCreate(),
		RequestRulesTest.RequestRulesTest()
	))

	result = unittest.TestResult()
	suite.run(result)
	print result
	if result.wasSuccessful():
		print Back.GREEN, "All completed Successfully", Style.RESET_ALL
	for error in result.errors:
		print Fore.YELLOW,error
	for failure in result.failures:
		print Fore.RED, failure
	print Style.RESET_ALL
	return 0

if __name__ == "__main__":
	runTests()