import UDClasses
import pandas as pd

uri = 'bolt://localhost:7687'
user = 'neo4j'
pwd = 'Neo_One'
db = 'neo4j'

conn = UDClasses.Neo4jConnection(uri, user, pwd, db)

# Read data
data_path = r'C:\Users\samea\Documents\GitHub\Neo_One\Data\example_rdb/'

friends_data = pd.read_csv(data_path + 'friends_table.csv')
posts_data = pd.read_csv(data_path + 'posts_table.csv')
posts_data['Index'] = posts_data.index.values + 1
reactions_data = pd.read_csv(data_path + 'reactions_table.csv')
user_data = pd.read_csv(data_path + 'user_table.csv')
user_data['Index'] = user_data.index.values + 1

# I use a = 1 where I want to include a breakpoint for debugging
a = 1

# Add constraints
# conn.query('CREATE CONSTRAINT papers IF NOT EXISTS ON (p:Paper)     ASSERT p.id IS UNIQUE')
# conn.query('CREATE CONSTRAINT authors IF NOT EXISTS ON (a:Author) ASSERT a.name IS UNIQUE')
# conn.query('CREATE CONSTRAINT categories IF NOT EXISTS ON (c:Category) ASSERT c.category IS UNIQUE')

#### Add Data:
# Manually-written rules
# Nodes first
# Inspiration: https://towardsdatascience.com/create-a-graph-database-in-neo4j-using-python-4172d40f89c4

# Example
# query = '''
# UNWIND $rows as row
# MERGE (p:Paper {id:row.id}) ON CREATE SET p.title = row.title
#
# // connect categories
# WITH row, p
# UNWIND row.category_list AS category_name
# MATCH (c:Category {category: category_name})
# MERGE (p)-[:IN_CATEGORY]->(c)

# Add Person nodes
query = '''
UNWIND $rows as row
MERGE (p:Person {data_source_id:row.Index, test_property:row.`Subscription Date`}) 
'''
conn.query(query, parameters={'rows': user_data.to_dict('records')})

# Add Post nodes
query = '''
UNWIND $rows as row
MERGE (p:Post {data_source_id:row.Index, test_property:row.`Post Date`})
'''
conn.query(query, parameters={'rows': posts_data.to_dict('records')})

# Add Person -> Post relationships
# // connect categories
# WITH row, p
# UNWIND row.category_list AS category_name
# MATCH (c:Category {category: category_name})
# MERGE (p)-[:IN_CATEGORY]->(c)

# Add Person -> Post relationships
# This might be slow because it needs to create (above) then find (here)
query = '''
UNWIND $rows AS row
MATCH 
(Person:Person {data_source_id: row.User}), 
(Post:Post {data_source_id: row.Index})
MERGE (Person)-[:creates]->(Post)
'''
conn.query(query, parameters={'rows': posts_data.to_dict('records')})

# Add Post_Type nodes
query = '''
UNWIND $rows as row
MERGE (p:Post_Type {
data_source:\'posts_data\', 
data_source_id:\'no_source_data_id\', 
name:row.`Post Type`
})
'''
conn.query(query, parameters={'rows': posts_data.to_dict('records')})

# Add Post -> Post_Type
# This might be slow because it needs to create (above) then find (here)
query = '''
UNWIND $rows AS row
MATCH 
(Post:Post {data_source_id: row.Index}), 
(Post_Type:Post_Type {name: row.`Post Type`})
MERGE (Post)-[:has_type]->(Post_Type)
'''
conn.query(query, parameters={'rows': posts_data.to_dict('records')})

#### Method 2: pseudo-config
