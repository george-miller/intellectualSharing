from py2neo import *

g = Graph('http://neo4j:django@127.0.0.1:7474/db/data/')


# Wrapping py2neo to give a domain-specific interface for our application

def getTypeNode(typeName):
    result = g.cypher.execute("MATCH (n:TypeNode {name:'" + typeName + "'}) RETURN n")
    return findSingleNodeFromCypherResult(result)

def getRelationshipType(relName):
    result = g.cypher.execute("MATCH (n:RelationshipType {name: '" + relName + "'}) RETURN n")
    return findSingleNodeFromCypherResult(result)

def findSingleNodeFromCypherResult(result):
    order = result.to_subgraph().order
    if order == 0:
        return None
    elif order == 1:
        return result[0][0]
    else:
        print "Error multiple nodes found when single node expected in " + str(result)
        return "Error multiple nodes found when single node expected in " + str(result)


def createNode(typeName, name, description):
    node = Node(typeName, name=name, description=description)
    g.create(node)
    return node

def createRelationship(nodeFrom, relationship, nodeTo):
    rel = Relationship(nodeFrom, relationship, nodeTo)
    g.create(rel)
    return rel

def getNode(nodeType, name):
    result = g.cypher.execute("MATCH (n:" + nodeType + " {name:'" + name + "'}) RETURN n")
    return findSingleNodeFromCypherResult(result)
   
def getCentralRelationshipName(fromType, toType):
    for rel in fromType.match("HAS_RELATIONSHIP"):
        if rel['forwardRelated'] == toType['name']:
            return rel.end_node['name']
    return None

def isRelationshipOnTypeNode(relationship, nodeFromType, nodeToType):
    fromType = getTypeNode(nodeFromType)
    toType = getTypeNode(nodeToType)
    if (fromType != None and toType != None):
        relName = getCentralRelationshipName(fromType, toType)
        if relationship == relName:
            return True
    return False

def createTypeNode(name):
    n = Node("TypeNode", name=name)
    g.create(n)
    return n

def createRelationshipType(nodeFromName, relationshipName, nodeToName):
    fromType = getTypeNode(nodeFromName)
    toType = getTypeNode(nodeToName)
    if (fromType != None and toType != None):
        relType = getRelationshipType(relationshipName)
        if relType == None:
            relType = Node("RelationshipType", name=relationshipName)

#TODO this method is too similar to the method after it.  Merge them into one
# It would make sense to change all methods to take Nodes instead of strings
        fromToRel = Relationship(fromType, "HAS_RELATIONSHIP", relType)
        fromToRel['forwardRelated'] = toType['name']
        relToTo = Relationship(relType, "HAS_RELATIONSHIP", toType)
        relToTo['backwardRelated'] = fromType['name']
        g.create(relType, fromToRel, relToTo)
        return relType
    else:
        return "Either couldn't find fromType: " + fromType + " or toType: " + toType

def connectTypeNodes(typeFrom, relName, typeTo):
    typeFrom = getTypeNode(typeFrom)
    typeTo = getTypeNode(typeTo)
    relType = getRelationshipType(relName)
    if (typeFrom != None and typeTo != None and relType != None):
        if connectionExistBetweenTypeNodes(typeFrom, relType, typeTo):
            return "Connection exists"
        fromToRel = Relationship(typeFrom, "HAS_RELATIONSHIP", relType)
        fromToRel['forwardRelated'] = typeTo['name']
        relToTo = Relationship(relType, "HAS_RELATIONSHIP", typeTo)
        relToTo['backwardRelated'] = typeFrom['name']
        g.create(relType, fromToRel, relToTo)
        return "Relationship created successfully!"
    else:
        return "Type or relationship not found: typeFrom - " + typeFrom + " typeTo - " + typeTo + " relType - " + relType

def connectionExistBetweenTypeNodes(typeFrom, relType, typeTo):
    for rel in typeFrom.match():
        if (rel['forwardRelated'] == typeTo['name']):
            return True
    return False
    
def getRelationshipNames():
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

