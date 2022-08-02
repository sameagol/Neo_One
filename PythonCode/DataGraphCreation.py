import pandas as pd
from py2neo import Graph
from UDClasses import merge_nodes_from_csv

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
read_person_dict = {
    'Labels': ['Person'],
    'user_data': {
        'data_source_id': 'Index',
        'test_property': 'Subscription Date'
    }
}

# Bring in Person nodes from user_data source
merge_nodes_from_csv(read_person_dict, user_data, graph)

# Define Post read dict
read_post_dict = {
    'Labels': ['Post'],
    'posts_data': {
        'data_source_id': 'Index',
        'test_property': 'Post Date'
    }
}

# Bring in Post nodes from posts_data source
merge_nodes_from_csv(read_post_dict, posts_data, graph)
