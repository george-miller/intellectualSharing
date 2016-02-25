import cPickle as pickle
import requests


def addNode(typeName,name,description):
    url = 'http://gmmotto.ddns.net/is/addNode'
    data = {'typeName':typeName,'name':name,'description':description}
    r = requests.post(url, data = data)
    print r.text
    print typeName, 'added:',name

def addPropertyToNode(type,name,propName,propValue):
    url = 'http://gmmotto.ddns.net/is/addPropertyToNode'
    data = {'type':type,'name':name,'propName':propName,'propValue':propValue}
    r = requests.post(url, data = data)
    print r.text
    print 'Added', propName, 'to', name,'of type',type

def addRelationshipBetweenNodes(nodeToType,nodeToName,nodeFromType,nodeFromName,relationshipName):
    url = 'http://gmmotto.ddns.net/is/addRelationshipBetweenNodes'
    data = {'nodeToType':nodeToType,'nodeToName':nodeToName,'nodeFromType':nodeFromType,'nodeFromName':nodeFromName,'relationshipName':relationshipName}
    r = requests.post(url, data = data)
    print r.text
    print 'Added',relationshipName,'between',nodeToName,'and',nodeFromName



complexRelationships = ['People','Companies']
singularRelationships = ['Sequel','Film Festivals','Ratings','Genres','Countries of Origin','Languages','Subjects','Films','Franchises','Release Dates','Film Formats','Notable Filming Locations','Songs']
informational = ['Title','Tagline','Type','mVal','Metacritic ID','Netflix ID','Alternate Titles','Topical Webpage','Images','Estimated Budget','Official Website','Topic Equivalent Webpage','Trailers','Description','Run Time']


relationships = {'Genres':'Has_Genre','Countries of Origin':'Made_In','Languages':'Primary_Language'}
nodeTypes = {'Genres':'Genre','Countries of Origin':'Country','Languages':'Language'}

firstMovie = pickle.load(open('firstMovie.p','rb'))
nodeProperties = ['Alternate Titles', 'Topical Webpage', 'Topic Equivalent Webpage', 'mVal']

mainTitle = firstMovie['Title']['en']
description = None
if 'Description' in firstMovie:
    description = firstMovie['Description']['en'][0]

addNode('Movie',firstMovie['Title']['en'],description)
for key in firstMovie:

    if key in singularRelationships:
        for item in firstMovie[key]:

            title = item['Title']['en']
            description = None
            if 'Description' in item:
                description = item['Description']['en'][0]

            addNode(nodeTypes[key],title,description)

            for prop in nodeProperties:
                if prop in item:
                    if prop in ['Alternate Titles']:
                        addPropertyToNode(nodeTypes[key],title,prop,item[prop]['en'])
                    else:
                        addPropertyToNode(nodeTypes[key],title,prop,item[prop])
            addRelationshipBetweenNodes(nodeTypes[key],title,'Movie',mainTitle,relationships[key])
    elif key in complexRelationships:
        if key == 'People':
            for person in firstMovie['People']:
                if person['Role'][0] == 'Cast':
                    roleName = person['Actor']['Title']['en'] + ' in ' + mainTitle
                    addNode('Role',roleName,None)
                    addPropertyToNode('Role',roleName,'mVal',person['mVal'])
                    addNode('Person',person['Actor']['Title']['en'],None)
                    addNode('Profession','Actor',None)
                    addRelationshipBetweenNodes('Movie',mainTitle,'Role',roleName,'In_Production_Of')
                    addRelationshipBetweenNodes('Person',person['Actor']['Title']['en'],'Role',roleName,'Had_Role')
                    addRelationshipBetweenNodes('Profession','Actor','Role',roleName,'Worked_As')
                else:
                    roleName = person['Title']['en'] + ' in ' + mainTitle
                    addNode('Role',roleName,None)
                    addNode('Person',person['Title']['en'],person['Description']['en'][0])
                    for prop in nodeProperties:
                        if prop in item:
                            if prop in ['Alternate Titles']:
                                addPropertyToNode('Person',person['Title']['en'],prop,item[prop]['en'])
                            else:
                                addPropertyToNode('Person',person['Title']['en'],prop,item[prop])
                    addNode('Profession',person['Role'][0],None)
                    addRelationshipBetweenNodes('Role',roleName,'Movie',mainTitle,'In_Production_Of')
                    addRelationshipBetweenNodes('Person',person['Title']['en'],'Role',roleName,'Had_Role')
                    addRelationshipBetweenNodes('Profession',person['Role'][0],'Role',roleName,'Worked_As')
        elif key == 'Companies':
            for item in firstMovie[key]
            roleName = mainTitle + ' in association with ' + item['Title']['en']
            addNode('Role',roleName,None)
            description = None
            if 'Description' in item and 'en' in item['Description']:
                description = item['Description']['en']
            addNode('Company',item['Title']['en'],description)
            addPropertyToNode('Company',item['Title']['en'],'mVal',item['mVal'])
            addRelationshipBetweenNodes('Role',roleName,'Movie',mainTitle,'In_Production_Of')
            addRelationshipBetweenNodes('Company',item['Title']['en'],'Role',roleName,'Had_Role')
    elif key in informational:
        if isinstance(firstMovie[key],list) or isinstance(firstMovie[key],(str,unicode)):
            addPropertyToNode('Movie',mainTitle,key,item[key])
        elif isinstance(firstMovie[key],list):
            addPropertyToNode('Movie',mainTitle,key,item[key]['en'])
        else:
            'Unknown Type of '+key+':'+str(firstMovie[key])



#get json with type, name, title, description. Then three lists of info, singular Relationships, and complex Relationships
#singular relationships have interior structure of Relationship Type, Direction, and Info About Object on Other Side of Relationship
#complex is similar to singular, except that it has Relationship Type, And then Info About each other objects. Should be able to be abstracted indefinitely



