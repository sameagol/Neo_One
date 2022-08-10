'''
In: Some parameters about the desired node
Out: A python dict and JSON file representing that node's definition
'''
import json

# Scrape node dictionaries to get allowable attributes
allowable_dict = {
    'Labels': [],
    'Properties': []
}

a = 1

# Open the JSON file
path = r'C:\Users\samea\Documents\GitHub\Neo_One\PythonCode\JSON_Files'
with open(path + '/Person.json') as json_file:
    data = json.load(json_file)

    # Compile Labels
    allowable_dict['Labels'] = list(set(allowable_dict['Labels'] + data['Labels']))

    # Compile Data Sources
    data_source_list = [k for k, v in data.items() if k not in ['Labels']]

    # Compile Properties
    property_list = []
    for data_source in data_source_list:
        property_list = property_list + list(data[data_source].keys())

    property_list = list(set(property_list))
