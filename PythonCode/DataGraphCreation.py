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

#### Method 2a: APOC a
# Manually-written rules
# Nodes first
# Use APOC
# This turns out to be trivially similar to Method 1

# Add Person nodes
query = '''
UNWIND $rows as row
MERGE (p:Person {data_source_id:row.Index, test_property:row.`Subscription Date`}) 
'''
conn.query(query, parameters={'rows': user_data.to_dict('records')})

# Example:
# UNWIND {batch} as row
# CALL apoc.create.node(row.labels, row.properties) yield node
# RETURN count(*)

user_data_formatted = user_data[['Index', 'Subscription Date']].rename({
    'Index': 'data_source_id',
    'Subscription Date': 'test_property'
}, axis=1)

query = '''
UNWIND $rows as row
CALL apoc.create.node(['Person'], {test_property: row.test_property}) yield node
RETURN count(*)
'''
conn.query(query, parameters={'rows': user_data_formatted.to_dict('records')})

## BEGIN STUPIDITY
user_data_formatted_2 = user_data[['Index', 'Subscription Date']].rename({
    'Index': 'data_source_id',
    'Subscription Date': 'test_property'
}, axis=1)
user_data_formatted_2['Labels'] = [['Person', 'Test_Label']]*len(user_data_formatted_2)
user_data_formatted_2['Property'] = {'test_property': user_data_formatted_2['test_property']}
prop_dict = {
    'test_property': row['test_property'] for row in user_data_formatted_2.iterrows()
}
## END STUPIDITY

#### Method 3: pseudo-config
# The subdictionary's keys are descriptions, the values are what shows up in the data
node_dict = {
    'Person':
        {'Labels': 'Person',
         'DataSourceID': 'Index',
         'OutputSourceID': 'data_source_id',
         'DataProperties': '`Subscription Date`',
         'OutputProperties': 'test_property'},
}

# Test by adding Person nodes
query = '''
UNWIND $rows as row
MERGE (p:{Labels} {{
{OutputSourceID}:row.{DataSourceID}, 
{OutputProperties}:row.{DataProperties}
}})
'''.format(
    Labels=node_dict['Person']['Labels'],
    OutputSourceID=node_dict['Person']['OutputSourceID'],
    DataSourceID=node_dict['Person']['DataSourceID'],
    OutputProperties=node_dict['Person']['OutputProperties'],
    DataProperties=node_dict['Person']['DataProperties'],
)
conn.query(query, parameters={'rows': user_data.to_dict('records')})

node_dict = {
    'Person':
        {'Labels': 'Person',
         'DataSourceID': 'Index',
         'OutputSourceID': 'data_source_id',
         'DataProperties': '`Subscription Date`',
         'OutputProperties': 'test_property'},
}

# Test by adding Person nodes
unk_format_dict = {
    'labels': [
        'Person'
    ],
    'properties': {
        'name': 'Person',
        'data_source_id': howtogetthis,
        'test_property': howtogetthis2,
    }
}

query = '''
UNWIND $rows as row
MERGE (p:{Labels} {{
{OutputSourceID}:row.{DataSourceID}, 
{OutputProperties}:row.{DataProperties}
}})
'''.format(
    Labels=node_dict['Person']['Labels'],
    OutputSourceID=node_dict['Person']['OutputSourceID'],
    DataSourceID=node_dict['Person']['DataSourceID'],
    OutputProperties=node_dict['Person']['OutputProperties'],
    DataProperties=node_dict['Person']['DataProperties'],
)
conn.query(query, parameters={'rows': user_data.to_dict('records')})

