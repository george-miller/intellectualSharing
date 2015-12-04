from django.db import models

# We are essentially creating a graph where each idea/object is a Node and relationships are edges
# I think we maybe could find a more efficient way to do this, I want to say graph databases but I don't know enough about them to know if they would work.

class Node(models.Model):
	title = models.CharField()
	description = models.TextField()
	
	def __str__(self):
		return self.title + "  " + self.id 

class Edge(models.Model):
	# NodeFrom has a relationship (whose ObjectId=relationshipid) to NodeTo
	nodeFrom = models.ForeignKey(Node)
	# Points to the Node that contains info on the relationship ex 'composed of'
	relationshipId = models.CharField()
	nodeTo = models.CharField()

	def __str__(self):
		node = Node.objects.get(id=self.relationshipId)
		return node.title
