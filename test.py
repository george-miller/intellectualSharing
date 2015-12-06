from intellectualSharing.models import Node, Route

Node.objects.all().delete()
Route.objects.all().delete()

brick = Node.objects.create(title='brick')
clay = Node.objects.create(title='clay', description='clay')
co = Node.objects.create(title='composedOf', description='composedOf')

brick.nodes.add(co)

bcoc = Route.objects.create(nodeFrom=brick.id, nodeTo=clay)
co.routes.add(bcoc)

print Node.objects.all()
print Route.objects.all()


