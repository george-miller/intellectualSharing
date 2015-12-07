from intellectualSharing.models import Node, Route

Node.objects.all().delete()
Route.objects.all().delete()

actor = Node.objects.create(title='actor', description='actor')
playedAs = Node.objects.create(title='playedAs', description='playedAs')
character = Node.objects.create(title='character', description='character')
In = Node.objects.create(title="in", description="in")
movie = Node.objects.create(title='movie', description='movie')

actor.nodes.add(playedAs)
playedAs.routes.add(Route.objects.create(nodeFrom=actor.id, nodeTo=character))
character.routes.add(Route.objects.create(nodeFrom=playedAs.id, nodeTo=In))
In.routes.add(Route.objects.create(nodeFrom=character.id, nodeTo=movie))

print Node.objects.all()
print Route.objects.all()

print actor.routeRelationships()
