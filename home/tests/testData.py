import requests
import random

baseurl = "http://localhost:8000/"

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

words = requests.get("http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain").content.splitlines()
def getRandomWord():
	return words[random.randint(0, len(words))]


# NON-META
nodes = [
	('actor', {'name':'Daniel Craig', 'hair': 'blond'}),
#	('actor', 'Daniel Craig', {'eyes': 'blue'}),
	('role', {'name':'Daniel Craig In Skyfall'}),
	('character', {'name':'James Bond'}),
	('movie', {'name':'Skyfall'}),
	('genre', {'name':'action'}),
	('award', {'name':'Tony'})
]
badRequestNodes = [
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
	('actor', 'Daniel Craig', 'had_role', 'role', 'Daniel Craig In Skyfall', {'hair': 'blond'}),
	('role', 'Daniel Craig In Skyfall', 'played', 'character', 'James Bond'),
	('role', 'Daniel Craig In Skyfall', 'in_production_of', 'movie', 'Skyfall'),
	('movie', 'Skyfall', 'has_genre', 'genre', 'action'),
	('movie', 'Skyfall', 'awarded', 'award', 'Tony')
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

multipleNodesRequestDict = {
	u'typeName': u'Movie'
}