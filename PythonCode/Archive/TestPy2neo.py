import pandas as pd
from py2neo import Graph
from py2neo.bulk import create_nodes, merge_nodes
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

## Import data

# Define read person dict
read_person_dict = {
    'Labels': ['Person'],
    'user_data': {
        'data_source_id': 'Index',
        'test_property': 'Subscription Date'
    }
}

merge_nodes(
    graph.auto(),  # not sure what this is
    user_data[list(read_person_dict['user_data'].values())].values.tolist(),  # list of lists data format
    merge_key=tuple(read_person_dict['Labels'] + list(read_person_dict['user_data'].keys())),  # tuple of distinction
    labels=tuple(read_person_dict['Labels']),  # Tuple of labels
    keys=list(read_person_dict['user_data'].keys())  # List of parameter names
)
graph.nodes.match('Person').count()

merge_nodes_from_csv(read_person_dict, user_data, graph)
