import requests
import random

baseurl = "http://localhost:8000/"

words = requests.get("http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain").content.splitlines()
def getRandomWord():
	return words[random.randint(0, len(words))]


# META
types = ['actor', 'role', 'movie', 'genre', 'character', 'award']
badTypes = ['A C T', 'GG****', '[]', '|\|', ',..,']
relTypes = ['had_role', 'in_production_of', 'has_genre', 'played', 'awarded']
connections = [
	('actor', 'had_role', 'role'), 
	('role', 'in_production_of', 'movie'),
	('movie', 'has_genre', 'genre'),
	('role', 'played', 'character'),
	('actor', 'awarded', 'award'),
	('movie', 'awarded', 'award')
]


# NON-META
nodes = [
	('actor', {'name':'Liam Neeson', 'dictionary': {'courage': 'Liam Neeson', 'bravery' : 'Liam Neeson'}}),
	('actor', {'name':'Liam Neeson', 'description': ['Well Liam, you are descriptive', 'Yes you are'], 'dict': {'day':'lovely'}, 'list' : [1, 2, 3, 4, 5]}),
	('actor', {'name':'Daniel Craig', 'hair': 'blond', 'likes': ['sex', 'blood', '$$$']}),
	('actor', {'name':'Daniel Craig', 'eyes': 'blue'}),
	('role', {'name':'Daniel Craig In Skyfall'}),
	('role', {'name':'Liam Neeson in Taken'}),
	('character', {'name':'James Bond'}),
	('movie', {'name':'Skyfall'}),
	('movie', {'name':'Taken', 'ratings': '0.0'}),
	('genre', {'name':'action'}),
	('award', {'name':'Tony'})
]
badRequestNodes = [
	('actor', 'properties'),
	('actor', ['1', '2']),
	('$$', {'name':'Moneyyy'}),
	('TypeNode', {'name':'Actor'}),
	('acto r', {'name':'___'})
]
notFoundNodes = [
	('poop', {'name':'poop'}),
	('acttor', {'name':'*)*#'}),
	('actorr', {'name':'Baddie'})
]

badAddNodePostData = [
	[
		('typeName', getRandomWord()),
		(getRandomWord(), getRandomWord())
	],
	[
		(getRandomWord(), getRandomWord()),
		('name', getRandomWord())
	],
	[
		(getRandomWord(), getRandomWord()),
		(getRandomWord(), getRandomWord())
	]
]

rels = [
	('actor', {'name':'Daniel Craig', 'hair': 'blond'}, 'had_role', 'role', {'name': 'Daniel Craig In Skyfall'}),
	('role', {'name': 'Daniel Craig In Skyfall'}, 'played', 'character', {'name':'James Bond'}),
	('role', {'name': 'Daniel Craig In Skyfall'}, 'in_production_of', 'movie', {'name':'Skyfall'}),
	('movie', {'name':'Skyfall'}, 'has_genre', 'genre', {'name':'action'}),
	('movie', {'name':'Skyfall'}, 'awarded', 'award', {'name':'Tony'}),
	('actor', {'name':'Liam Neeson', 'dictionary': {'courage': 'Liam Neeson', 'bravery' : 'Liam Neeson'}}, 'had_role', 'role', {'name': 'Liam Neeson in Taken'}),
	('role', {'name': 'Liam Neeson in Taken'}, 'in_production_of', 'movie', {'name':'Taken'}),
]

movieRelationshipDict = {
	u'type' : u'Movie', 
	u'in' : {
		u'Role' : [u'In_Production_Of']
	},
	u'out' : {
		u'Award' : [u'Awarded'],
		u'Genre' : [u'Has_Genre']
	}
}

goodAddPropertyToNode = [
	{
		'typeName' : 'actor',
		'properties' : {'name':'Daniel Craig', 'hair': 'blond'},
		'newProperties' : {'eyes' : 'striking'}
	},
	{
		'typeName' : 'role',
		'properties' : {'name': 'Daniel Craig In Skyfall'},
		'newProperties' : {'rating' : '4.0'}
	},
	{
		'typeName' : 'movie',
		'properties' : {'name':'Skyfall'},
		'newProperties' : {'rating' : '4.1'}
	},
	{
		'typeName' : 'award',
		'properties' : {'name':'Tony'},
		'newProperties' : {'material' : 'gold'}
	}
]
badAddPropertyToNode = [
	{
		'typeName' : '$%^',
		'newProperties' : {'rating' : '4.0'}
	},
	{
		'typeName' : 'actor',
		'properties' : {'name':'Daniel Craig', 'hair': 'blond'}
	},
	{
		'properties' : {'name': 'Daniel Craig In Skyfall'},
		'newProperties' : {'rating' : '4.0'}
	}
]
notFoundAddPropertyToNode = [
	{
		'typeName' : 'vdfeq',
		'properties' : {'name':'Daniel Craig', 'hair': 'blond'},
		'newProperties' : {'eyes' : 'striking'}
	},
	{
		'typeName' : 'actor',
		'properties' : {'name':'Dandiel Craig', 'hair': 'blond'},
		'newProperties' : {'eyes' : 'striking'}
	}
]