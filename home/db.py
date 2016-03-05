from py2neo import *

g = Graph('http://neo4j:django@127.0.0.1:7474/db/data/')

class TemplateNode():
    def __init__(self, node):
        self.node = node
        self.properties = node.properties
        self.name = node['name']
        self.label = list(node.labels)[0]

# Wrapping py2neo to give a domain-specific interface for our application

# NOTE: Most methods take instances of Node as arguments, except for the ones that create new Nodes/Relationships

# Helpful method to parse a cypher result
def returnCypherResult(result):
    subGraph = result.to_subgraph()
    order = subGraph.order
    if order == 0:
        return None
    elif order == 1:
        return result[0][0]
    else:
        nodes = []
        for node in subGraph.nodes:
            nodes.append(node)
        return nodes

# --- META METHODS ---

def getTypeNode(typeName):
    typeName = typeName.title()
    result = g.cypher.execute("MATCH (n:TypeNode {name:'" + typeName + "'}) RETURN n")
    return returnCypherResult(result)

def getRelationshipType(relName):
    relName = relName.title()
    result = g.cypher.execute("MATCH (n:RelationshipType {name: '" + relName + "'}) RETURN n")
    return returnCypherResult(result)
   
def getRelationshipTypeNamesBetweenTypeNodes(fromType, toType):
    typeNames = []
    for rel in fromType.match("HAS_RELATIONSHIP"):
        if rel['forwardRelated'] == toType['name']:
            typeNames.append(rel.end_node['name'])
    return typeNames

def getRelationshipTypeNames():
    result = g.cypher.execute("MATCH (n:RelationshipType) RETURN n")
    relNames = []
    for rel in result:
        relNames.append(rel.n["name"])
    return relNames

def getTypeNames():
    result = g.cypher.execute("MATCH (n:TypeNode) RETURN n")
    typeNames = []
    for n in result:
        typeNames.append(n.n['name'])
    return typeNames

def createTypeNode(name):
    name = name.title()
    n = Node("TypeNode", name=name)
    g.create(n)
    return n

def createRelationshipType(relationshipName):
    relationshipName = relationshipName.title()
    relType = Node("RelationshipType", name=relationshipName)
    g.create(relType)
    return relType

def connectTypeNodes(typeFrom, relType, typeTo):
    fromToRel = Relationship(typeFrom, "HAS_RELATIONSHIP", relType)
    fromToRel['forwardRelated'] = typeTo['name']
    relToTo = Relationship(relType, "HAS_RELATIONSHIP", typeTo)
    relToTo['backwardRelated'] = typeFrom['name']
    g.create(fromToRel, relToTo)

def getRelationshipDict(typeNode):
    d = {
        'type' : typeNode['name'],
        'in' : {},
        'out' : {}
    }
    for rel in typeNode.match("HAS_RELATIONSHIP"):
        if type(rel['forwardRelated']) != type(None):
            if rel['forwardRelated'] in d['out'].keys():
                d['out'][rel['forwardRelated']].append(rel.end_node['name'])
            else:
                d['out'][rel['forwardRelated']]  = [rel.end_node['name']]
        else:
            if rel['backwardRelated'] in d['in'].keys():
                d['in'][rel['backwardRelated']].append(rel.start_node['name'])
            else:
                d['in'][rel['backwardRelated']] = [rel.start_node['name']]
    return d


# ----- NON META METHODS ------ 

def createNode(typeName, properties):
    typeName = typeName.title()
    node = Node(typeName)
    for prop in properties.keys():
        node[prop] = properties[prop]
    g.create(node)
    return node

def createRelationship(nodeFrom, relName, nodeTo):
    relName = relName.title()
    rel = Relationship(nodeFrom, relName, nodeTo)
    g.create(rel)
    return rel

def isRelationshipBetweenNodes(nodeFrom, relName, nodeTo):
    relName = relName.title()
    for rel in nodeFrom.match(relName):
        if rel.end_node == nodeTo:
            return True
    return False

def getNode(typeName, properties):
    typeName = typeName.title()
    match_string = "MATCH (n:" + typeName + " {"

    for prop in properties.keys():
        properties[prop] = properties[prop].replace("'", "\\'")
        match_string += prop+":'"+properties[prop]+"', "

    if len(properties.keys()) > 0:
        match_string = match_string[:len(match_string)-2] + "}) RETURN n LIMIT 100"
    else:
        match_string += "}) RETURN n LIMIT 100"

    result = g.cypher.execute(match_string)
    return returnCypherResult(result)

def getNodesByType(typeName, *props):
    typeName = typeName.title()

    match_string = "MATCH (n:" + typeName
    #for prop in props:
    #    match_string += " {name:'" + name + "'}"
    match_string += ") RETURN n LIMIT 100"

    result = g.cypher.execute(match_string)
    return returnCypherResult(result)

def getOutgoingRels(node):
    if 'TypeNode' in node.labels or 'RelationshipType' in node.labels:
        print "This method does not work for TypeNodes or RelationshipTypes"
        return None
    else:
        rels = []
        for i in node.match_outgoing():
            rels.append((i.type, i.end_node.labels.pop(), i.end_node['name']))
        return rels

def getIncomingRels(node):
    if 'TypeNode' in node.labels or 'RelationshipType' in node.labels:
        print "This method does not work for TypeNodes or RelationshipTypes"
        return None
    else:
        rels = []
        for i in node.match_incoming():
            rels.append((i.type, i.start_node.labels.pop(), i.start_node['name']))
        return rels
