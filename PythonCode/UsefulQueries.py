"""
This is meant to be a cheatsheet-style stash.
Some of these queries are most useful when run in Neo4j Browser as their output is visual.
"""

import UDClasses
import pandas as pd

uri = 'bolt://localhost:7687'
user = 'neo4j'
pwd = 'Neo_One'
db = 'neo4j'
conn = UDClasses.Neo4jConnection(uri, user, pwd, db)


# Create / Merge node with multiple labels
conn.query('MERGE (n:Meta:Meta_Person)')

# Show subgraph of one relationship
query = '''
MATCH (n:Person {data_source_id: 1})-->(m)
RETURN n, m
'''

# Show subgraph of two relationships
query = '''
MATCH (n:Person {data_source_id: 1}) --> (m:Post) --> (o:Post_Type)
RETURN n, m, o
'''

# Show all nodes
conn.query('MATCH(n) RETURN (n)')

# Show meta graph
conn.query('call apoc.meta.graph')

# Delete certain nodes
conn.query('MATCH (n:Post_Type) DELETE (n)')

# Delete certain relationships
conn.query('MATCH (n:Post)-[r]->() DELETE r')

# Delete entire graph. This does not delete labels.
conn.query('MATCH (n) DETACH DELETE n')
