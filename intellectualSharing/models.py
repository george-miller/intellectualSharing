from neo4django.db import models

# We are essentially creating a graph where each idea/object is a Node and relationships are edges
# I think we maybe could find a more efficient way to do this, I want to say graph databases but I don't know enough about them to know if they would work.

class Node(models.NodeModel):
	title = models.StringProperty()
	description = models.StringProperty()
	edges = models.Relationship('Edge', rel_type='relationship', related_name='edges')
	
	def __str__(self):
		return self.title + "  " + self.id 

class Edge(models.NodeModel):
	title = models.StringProperty()
	description = models.StringProperty()
	nodes = models.Relationship(Node, rel_type='realtionship', related_name='nodes')

	def __str__(self):
		return self.title + "  " + self.id

