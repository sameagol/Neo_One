import UDClasses
import pandas as pd

uri = 'bolt://localhost:7687'
user = 'neo4j'
pwd = 'Neo_One'
db = 'neo4j'
conn = UDClasses.Neo4jConnection(uri, user, pwd, db)

# Display subgraph of one relationship
query = '''
MATCH (n:Person {data_source_id: 1})-->(m)
RETURN n, m
'''

# Display subgraph of two relationships
query = '''
MATCH (n:Person {data_source_id: 1}) --> (m:Post) --> (o:Post_Type)
RETURN n, m, o
'''

# Create / Merge node with multiple labels
conn.query('MERGE (n:Meta:Meta_Person)')

# Show all nodes
conn.query('MATCH(n) RETURN (n)')

# Delete certain nodes
conn.query('MATCH (n:Post_Type) DELETE (n)')

# Delete certain relationships
conn.query('MATCH (n:Post)-[r]->() DELETE r')

# Delete entire graph. This does not delete labels.
conn.query('MATCH (n) DETACH DELETE n')
