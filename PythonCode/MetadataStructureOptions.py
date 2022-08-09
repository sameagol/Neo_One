'''
Option 1: Store metadata in an ontological knowledge graph

Option 2: Python Dictionaries

Option 3: JSON / YAML / txt

Option 4: py2neo ogm
Store the specific node's info in this ogm.Model structure
Node():
    Label1
    Label2

    Property1
    Property2

    othernodetype = RelatedTo('othernode', 'REL_TYPE')

Store the node's generic information (data sources, etc) elsewhere?

Option 5: Hybrid!
'''

# Data sources listed in node
person_dict_1 = {
    'Labels': ['Person'],
    'user_data': {
        'data_source_id': 'Index',
        'test_property': 'Subscription Date'
    },
    'posts_data': {
        'data_source_id': 'User'
    }
}

person_allowable_1 = {
    'Labels': ['Person', 'TestLabel'],
    'Properties': {'user_data', 'posts_data'}
}

# Data sources shown in graph
person_dict_2 = {
    'Labels': ['Person'],
    'data_source_id': 'Index',
    'test_property': 'Subscription Date'
}

person_allowable = {
    'Labels': ['Person', 'TestLabel'],
    'Properties': {'data_source_id', 'data_source', 'test_property'}
}

allowable_edges = [
    ['Person', 'CREATES', 'Post']
]

posts_data_allowable = {
    'Nodes': 'Pers'
}

# My best guess:
'''
Have a python function that creates python dictionaries.
Then convert the python dictionaries to json-like formats that are neo-friendly.
Allowable aspects of the graph can be a scrape of the objects themselves.
Data sources???
'''