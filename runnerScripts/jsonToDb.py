import requests
import json
baseurl = 'http://gmmotto.ddns.net/is/'


def getRelationship(orginalTypeName,connectingTypeName):
    url = baseurl + 'getRelationshipDict'
    data = {'typeName':orginalTypeName}
    r = requests.post(url, data = data)
    relationshipDict = json.loads(r.text)
    outDict = relationshipDict['out']
    inDict = relationshipDict['in']

    if connectingTypeName in outDict:
        return ('out',outDict[connectingTypeName])
    if connectingTypeName in inDict:
        return ('in',inDict[connectingTypeName])
    raise NameError('No Relationship Between ' + orginalTypeName + ' and ' + connectingTypeName + ' exists.')

def addNode(typeName,name,description):
    url = baseurl + 'addNode'
    data = {'typeName':typeName,'name':name,'description':description}
    r = requests.post(url, data = data)
    if r.status_code not in [200,201]:
        print 'Add Node Error:'
        print r.status_code, r.text

def addPropertyToNode(typeName,name,propName,propValue):
    url = baseurl + 'addPropertyToNode'
    data = {'typeName':typeName,'name':name,'propName':propName,'propValue':propValue}
    r = requests.post(url, data = data)
    if r.status_code not in [200,201]:
        print 'Add Property Error:'
        print r.status_code, r.text

def addRelationshipBetweenNodes(nodeToType,nodeToName,nodeFromType,nodeFromName,relationshipName):
    url = baseurl + 'addRelationshipBetweenNodes'
    data = {'toType':nodeToType,'toName':nodeToName,'fromType':nodeFromType,'fromName':nodeFromName,'relName':relationshipName}
    r = requests.post(url, data = data)
    if r.status_code not in [200,201]:
        print 'Add Relationship Error:'
        print r.status_code, r.text

def commitBasicNodeInfo(inputData):
    if 'type' in inputData:
        type = inputData['type']
    else:
        raise NameError('No Type In Input Data')
    if 'Informational' in inputData:
        title = None
        description = None

        try:
            if 'Title' in inputData['Informational']:
                if isinstance(inputData['Informational']['Title'],dict):
                    title = inputData['Informational']['Title']['en']
                else:
                    title = inputData['Informational']['Title']
        except:
            print inputData
            raise NameError('Title Not Set Up Properly')


        try:
            if 'Description' in inputData['Informational']:
                if isinstance(inputData['Informational'],(str,unicode,list)):
                    description = inputData['Informational']['Description']
                elif isinstance(inputData['Informational']['Title'],dict):
                    description = inputData['Informational']['Description']['en']
        except:
            raise NameError('Description Not Set Up Properly')

        if title == None:
            print inputData
            raise NameError('Title Not Set Up Properly: Title Non-existent')

        addNode(type,title,description)
        return (type,title,description)
    else:
        print inputData
        raise NameError('No Informational Data in Input Data')


def commitInformationalData(inputData,type,title):
    for key in inputData['Informational']:
        if key in ['Title','Description']:
            continue
        if isinstance(inputData['Informational'][key],list) or isinstance(inputData['Informational'][key],(str,unicode)):
            addPropertyToNode(type,title,key,inputData['Informational'][key])
        elif isinstance(inputData['Informational'][key],list):
            addPropertyToNode(type,title,key,inputData['Informational'][key]['en'])
        else:
            'Unknown Type of '+key+':'+str(inputData['Informational'][key])

def commitRelationships(inputData,type,title):
    for key in inputData['Relationships']:
        for item in inputData['Relationships'][key]:
            basics = commitBasicNodeInfo(item)
            commitInformationalData(item,basics[0],basics[1])
            commitRelationships(item,basics[0],basics[1])

            #determine direction
            (nodeFrom,relationshipNames) = getRelationship(type,key)
            if len(relationshipNames) > 1:
                if 'rel' in item and item['rel'] in relationshipNames:
                    relName = item['rel']
                else:
                    raise NameError('Relationship Must Be Defined Between ' + basics[0] + ' and ' + title + ' Options: ' + str(relationshipNames))
            else:
                relName = relationshipNames[0]

            if nodeFrom == 'out':
                addRelationshipBetweenNodes(key,basics[1],type,title,relName)
            else:
                addRelationshipBetweenNodes(type,title,key,basics[1],relName)



def addData(inputData):
#inputData = {'type':'Movie','informational':{},'singularRelationships':{},'complexRelationships':{}}
    #go through input Data to commit to Database
    basics = commitBasicNodeInfo(inputData)
    commitInformationalData(inputData,basics[0],basics[1])
    commitRelationships(inputData,basics[0],basics[1])

