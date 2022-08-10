'''
This file takes a dictionary in python and creates a JSON file
'''
import json

# Define Person dict
person_dict = {
    'Labels': ['Person'],
    'user_data': {
        'data_source_id': 'Index',
        'test_property': 'Subscription Date'
    },
    'posts_data': {
        'data_source_id': 'User',
        'test_property_2': 'Post Date'
    }
}

# Create JSON file
path = r'C:\Users\samea\Documents\GitHub\Neo_One\PythonCode\JSON_Files/'
with open(path + 'Person.json', 'w') as fp:
    json.dump(person_dict, fp)

# Create Post dict
post_dict = {
    'Labels': ['Post'],
    'posts_data': {
        'data_source_id': 'Index',
        'test_property': 'Post Date'
    }
}

# Create JSON file
path = r'C:\Users\samea\Documents\GitHub\Neo_One\PythonCode\JSON_Files/'
with open(path + 'Post.json', 'w') as fp:
    json.dump(post_dict, fp)

a = 1

# Create Person - CREATES -> Post dict
person_creates_post_dict = {
    'Label': 'CREATES',
    'posts_data': {
        'Properties': {'data_source_id': 'Index', 'test_property': 'Post Date'},
        'Source Node': 'Person',
        'Destination Node': 'Post'
    }
}

# Create JSON file
path = r'C:\Users\samea\Documents\GitHub\Neo_One\PythonCode\JSON_Files/'
with open(path + 'Person-CREATES-Post.json', 'w') as fp:
    json.dump(person_creates_post_dict, fp)

