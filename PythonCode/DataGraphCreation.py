import pandas as pd
from py2neo import Graph
from py2neo.bulk import create_relationships
from UDClasses import merge_nodes_from_dataframe, merge_relationships_from_dataframe
import json

uri = 'bolt://localhost:7687'
user = 'neo4j'
pwd = 'Neo_One'
db = 'neo4j'

graph = Graph("bolt://localhost:7687", auth=(user, pwd))
graph.run('MATCH (n) RETURN COUNT (n)')

# Paths
data_path = r'C:\Users\samea\Documents\GitHub\Neo_One\Data\example_rdb/'
json_path = r'C:\Users\samea\Documents\GitHub\Neo_One\PythonCode\JSON_Files/'

# Read tabular data
friends_data = pd.read_csv(data_path + 'friends_table.csv')
posts_data = pd.read_csv(data_path + 'posts_table.csv')
posts_data['Index'] = posts_data.index.values + 1
reactions_data = pd.read_csv(data_path + 'reactions_table.csv')
user_data = pd.read_csv(data_path + 'user_table.csv')
user_data['Index'] = user_data.index.values + 1

a = 1

# Define Person dict
with open(json_path + '/Person.json') as json_file:
    person_dict = json.load(json_file)

# Bring in Person nodes from user_data source
merge_nodes_from_dataframe(person_dict, user_data, 'user_data', graph)

# Define Post read dict
with open(json_path + '/Post.json') as json_file:
    post_dict = json.load(json_file)

# Bring in Post nodes from posts_data source
merge_nodes_from_dataframe(post_dict, posts_data, 'posts_data', graph)

# Create Person - CREATES -> Post
with open(json_path + '/Person-CREATES-Post.json') as json_file:
    person_creates_post_dict = json.load(json_file)

merge_relationships_from_dataframe(
    person_dict,
    person_creates_post_dict,
    post_dict,
    posts_data,
    'posts_data',
    graph
)
