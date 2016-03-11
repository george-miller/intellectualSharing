Install Instructions:

Install python from apt-get or another service
Create and activate a virutual environment in the project root folder (You don't have to but it's nice)

Install Dependencies:
```pip install Django```
```pip install py2neo```

Install neo4j from their website and start neo4j with:
```PATH_TO_NEO4J/bin/neo4j console```

Running Tests:
Be careful! This will delete your db!
```python manage.py test```
