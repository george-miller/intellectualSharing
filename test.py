from intellectualSharing.models import Node, Edge

brick = Node.objects.create(title="Brick", description="Brick")
clay = Node.objects.create(title="Clay", description="Clay")
relationship = Node.objects.create(title="ComposedOf", description="ComposedOf")
Edge.objects.create(nodeFrom=brick, relationshipId=relationship.id, nodeTo=clay.id)
