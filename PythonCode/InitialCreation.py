import UDFClasses

uri = 'bolt://localhost:7687'
user = 'neo4j'
pwd = 'Neo_One'

conn = UDFClasses.Neo4jConnection(uri, user, pwd)

a = 1
