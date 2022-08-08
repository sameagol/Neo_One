import pandas as pd
from py2neo import Graph
from py2neo.bulk import create_relationships
from UDClasses import merge_nodes_from_dataframe, merge_relationships_from_dataframe

uri = 'bolt://localhost:7687'
user = 'neo4j'
pwd = 'Neo_One'
db = 'neo4j'

graph = Graph("bolt://localhost:7687", auth=(user, pwd))
graph.run('MATCH (n) RETURN COUNT (n)')

# Read data
data_path = r'C:\Users\samea\Documents\GitHub\Neo_One\Data\example_rdb/'

friends_data = pd.read_csv(data_path + 'friends_table.csv')
posts_data = pd.read_csv(data_path + 'posts_table.csv')
posts_data['Index'] = posts_data.index.values + 1
reactions_data = pd.read_csv(data_path + 'reactions_table.csv')
user_data = pd.read_csv(data_path + 'user_table.csv')
user_data['Index'] = user_data.index.values + 1

a = 1

# Define Person read dict
person_dict = {
    'Labels': ['Person'],
    'user_data': {
        'data_source_id': 'Index',
        'test_property': 'Subscription Date'
    },
    'posts_data': {
        'data_source_id': 'User'
    }
}

# Bring in Person nodes from user_data source
merge_nodes_from_dataframe(person_dict, user_data, 'user_data', graph)

# Define Post read dict
post_dict = {
    'Labels': ['Post'],
    'posts_data': {
        'data_source_id': 'Index',
        'test_property': 'Post Date'
    }
}

# Bring in Post nodes from posts_data source
merge_nodes_from_dataframe(post_dict, posts_data, 'posts_data', graph)

# Create Person - CREATES -> Post
person_creates_post_rel_dict = {
    'Labels': 'CREATES',
    'posts_data': {
        'Properties': {'data_source_id': 'Index', 'test_property': 'Post Date'},
        'Source Node': 'Person',
        'Destination Node': 'Post'
    }
}

merge_relationships_from_dataframe(
    person_dict,
    person_creates_post_rel_dict,
    post_dict,
    posts_data,
    'posts_data',
    graph
)
