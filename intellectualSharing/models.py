from neo4django.db import models

class Route(models.NodeModel):
	nodeFrom = models.IntegerProperty()
	nodeTo = models.Relationship('Node', single=True, rel_type='route', related_name='nodeTo')

	def __str__(self):
		return "Route from " + str(self.nodeFrom) + " to " + str(self.nodeTo)

class Node(models.NodeModel):
	title = models.StringProperty()
	description = models.StringProperty()
	routes = models.Relationship(Route, rel_type='route', related_name='routes')
	nodes = models.Relationship('Node', rel_type='relationship', related_name='nodes')
	
	def __str__(self):
		return self.title + "  " + str(self.id) 

	def route(self, node):
		if not(isinstance(node, Node)):
			return "Input node not a node"
		for route in self.routes.all():
			if route.nodeFrom == node.id:
				return route.nodeTo

		return "No routes found"

	def getRelationships(self):
		return self.nodes.all()

	def routeRelationships(self):
		routeRels = []
		for node in self.nodes.all():
			routeRels.append([node, node.route(self)])

		return routeRels

