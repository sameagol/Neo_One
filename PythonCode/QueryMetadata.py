import UDClasses

uri = 'bolt://localhost:7687'
user = 'neo4j'
pwd = 'Neo_One'
db = 'neo4j'

conn = UDClasses.Neo4jConnection(uri, user, pwd, db)

a = 1

conn.query('call apoc.meta.graph')
