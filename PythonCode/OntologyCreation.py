import UDFClasses

uri = 'bolt://localhost:7687'
user = 'neo4j'
pwd = 'Neo_One'
db = 'neo4j'

conn = UDFClasses.Neo4jConnection(uri, user, pwd, db)

# conn.query('CREATE CONSTRAINT papers IF NOT EXISTS ON (p:Paper)     ASSERT p.id IS UNIQUE')
# conn.query('CREATE CONSTRAINT authors IF NOT EXISTS ON (a:Author) ASSERT a.name IS UNIQUE')
# conn.query('CREATE CONSTRAINT categories IF NOT EXISTS ON (c:Category) ASSERT c.category IS UNIQUE')

a = 1

# Method 1: Node dictionary and manual edge queries
'''
This is a little redundant because when you create edges, you need to include some node info.
Inevitably there will need to be a manual connection of nodes. Here it happens in the
relationship instantiation.
'''

# Create list of node types
node_list = ['Person', 'Post', 'Post_Type']

# Create dictionary of node types and labels
node_dict = {key: ['Meta', 'Meta' + key] for key in node_list}

# Loop through node dictionary, creating each node
for key, val in node_dict.items():

    # Extract labels
    label_string = ':'.join(val)

    # Create nodes
    # Recipe:   MERGE (n:Label1:Label2 {name: 'Name'})
    conn.query('MERGE (n: {} {{name: \'{}\'}})'.format(label_string, key))

# Create Relationships
query = 'MATCH (a:Meta_{origin}), (b:Meta_{terminus}) ' \
        'WHERE a.name = \'{origin}\' AND b.name = \'{terminus}\' ' \
        'MERGE (a) - [r:Meta_Creates {{name: \'Creates\'}}] -> (b)' \
        ''.format(origin='Person', terminus='Post')
conn.query(query)

query = 'MATCH (a:Meta_{origin}), (b:Meta_{terminus}) ' \
        'WHERE a.name = \'{origin}\' AND b.name = \'{terminus}\' ' \
        'MERGE (a) - [r:Meta_Has_Type {{name: \'Has_Type\'}}] -> (b)' \
        ''.format(origin='Post', terminus='Post_Type')
conn.query(query)

# Method 2: Write cypher queries
'''
This method can be done via Neo4j Browser of from python.
It was abandoned because it just seems lame to write out each thing then test it.
'''
# https://neo4j.com/docs/cypher-cheat-sheet/current/
conn.query('MERGE (n:Meta:Meta_Person)')
conn.query('MATCH(n) RETURN (n)')
conn.query('MATCH (n) DETACH DELETE n')

# Method 3: Use relationships to define everything
conn.query('MERGE (n:MetaPerson {name: \'Person\'}) - '
           '[r:Meta_Creates {name: \'Creates\'}] -> '
           '(n:MetaPost {name: \'Post\'})')

rel_dict = {
    'Creates': '(n:MetaPerson) - [r:Meta_Creates {name: Creates}] -> (n:MetaPost)',

}