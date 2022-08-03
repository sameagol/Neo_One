import pandas as pd
from py2neo import Graph
from py2neo.bulk import create_relationships
from py2neo.bulk import merge_relationships
from UDClasses import merge_nodes_from_dataframe

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
    },
    'posts_data': {
        'data_source_id': 'User'
    }
}

# Bring in Person nodes from user_data source
merge_nodes_from_dataframe(read_person_dict, user_data, 'user_data', graph)

# Define Post read dict
read_post_dict = {
    'Labels': ['Post'],
    'posts_data': {
        'data_source_id': 'Index',
        'test_property': 'Post Date'
    }
}

# Bring in Post nodes from posts_data source
merge_nodes_from_dataframe(read_post_dict, posts_data, 'posts_data', graph)

# Create Person - CREATES -> Post
person_creates_post_rel_dict = {
    'Label': 'CREATES',
    'posts_data': {
        'Properties': {'data_source_id': 'Index', 'test_property': 'Post Date'},
        'Source Node': 'Person',
        'Destination Node': 'Post'
    }
}

def merge_relationships_from_dataframe(
        source_node_dict: dict,
        rel_dict: dict,
        destination_node_dict: dict,
        df: pd.DataFrame,
        data_source: str,
        graph
):

    source_node_dict = read_person_dict.copy()
    rel_dict = person_creates_post_rel_dict.copy()
    destination_node_dict = read_post_dict.copy()
    df = posts_data.copy()
    data_source = 'posts_data'

    property_list = []

    # Populate list of property dictionaries
    for ind, row in df.iterrows():
        item = {key: row[val] for key, val in rel_dict[data_source]['Properties'].items()}
        property_list.append(item)
    df['Property Dictionary'] = property_list

    # Reshape dataframe to data format that py2neo likes:
    # | Left Node Constraints | Property Dictionary | Right Node Constraints
    # | Single tuple User     | test_prop from PD   | Single tuple Index

    # Get left node constraints
    left_node_constraint = source_node_dict[data_source]['data_source_id']
    df['Left Node Constraints'] = list(zip(df[left_node_constraint]))

    df['Post Date'] = prop_dict

    data = df[data_cols_list].values.tolist()

    merge_relationships(graph.auto(), data, 'CREATES',
                        start_node_key=(('Person'), 'data_source_id'),
                        end_node_key=(('Post'), 'data_source_id')
                        )


