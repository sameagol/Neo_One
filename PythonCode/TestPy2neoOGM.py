import pandas as pd
from py2neo import Graph
from py2neo import ogm
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

class Movie(Model):
    __primarykey__ = "title"

    title = Property()
    tag_line = Property("tagline")
    released = Property()

    actors = RelatedFrom("Person", "ACTED_IN")
    directors = RelatedFrom("Person", "DIRECTED")
    producers = RelatedFrom("Person", "PRODUCED")


class Person(ogm.Model):
    __primarykey__ = 'data_source_id'  # ? What if there are two data sources for one person?

    Person = ogm.Label()
    TestLabel = ogm.Label()

    user_data = ogm.PropertyDict()
    posts_data = ogm.PropertyDict()

    posts = ogm.RelatedTo('Post', 'CREATES')

person_type = Person()
bob = person_type

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

