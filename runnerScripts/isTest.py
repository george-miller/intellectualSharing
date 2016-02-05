import cPickle as pickle
import requests

baseurl = 'http://gmmotto.ddns.net/is/'

def addNode(typeName,name,description):
    url = baseurl + 'addNode'
    data = {'typeName':typeName,'name':name,'description':description}
    r = requests.post(url, data = data)
    print r.status_code, r.text

def addPropertyToNode(typeName,name,propName,propValue):
    url = baseurl + 'addPropertyToNode'
    data = {'typeName':typeName,'name':name,'propName':propName,'propValue':propValue}
    r = requests.post(url, data = data)
    print r.status_code, r.text

def addRelationshipBetweenNodes(nodeToType,nodeToName,nodeFromType,nodeFromName,relationshipName):
    url = baseurl + 'addRelationshipBetweenNodes'
    data = {'toType':nodeToType,'toName':nodeToName,'fromType':nodeFromType,'fromName':nodeFromName,'relName':relationshipName}
    r = requests.post(url, data = data)
    print r.status_code, r.text



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

    if key in ['Genres','Countries of Origin','Languages']:
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
    elif key == 'People':
        for person in firstMovie['People']:
            if person['Role'][0] == 'Cast':
                roleName = person['Actor']['Title']['en'] + ' in ' + mainTitle
                addNode('Role',roleName,None)
                addPropertyToNode('Role',roleName,'mVal',person['mVal'])
                addNode('Person',person['Actor']['Title']['en'],None)
                addRelationshipBetweenNodes('Movie',mainTitle,'Role',roleName,'In_Production_of')
                addRelationshipBetweenNodes('Person',person['Actor']['Title']['en'],'Role',roleName,'Had_Role')
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
                addRelationshipBetweenNodes('Movie',mainTitle,'Role',roleName,'In_Production_of')
                addRelationshipBetweenNodes('Person',person['Title']['en'],'Role',roleName,'Had_Role')
                addRelationshipBetweenNodes('Profession',person['Role'][0],'Role',roleName,'Worked_As')

    else:
        if key in ['Alternate Titles']:
            addPropertyToNode('Movie',mainTitle,key,item[key]['en'])
        else:
            addPropertyToNode('Movie',mainTitle,key,item[key])
