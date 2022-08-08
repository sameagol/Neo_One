from neo4j import GraphDatabase
import pandas as pd
from py2neo import Graph
from py2neo.bulk import merge_relationships
from py2neo.bulk import create_nodes, merge_nodes


# Define function for inserting nodes with just a dictionary and a table
def merge_nodes_from_dataframe(node_dict: dict, df: pd.DataFrame, data_source: str, graph):

    data_cols_list = list(node_dict[data_source].values())

    merge_nodes(
        graph.auto(),  # not sure what this is
        df[data_cols_list].values.tolist(),  # list of lists data format
        merge_key=tuple(node_dict['Labels'] + list(node_dict[data_source].keys())),  # tuple of distinction
        labels=tuple(node_dict['Labels']),  # Tuple of labels
        keys=list(node_dict[data_source].keys())  # List of parameter names
    )


# This would be cleaner if some kind of node_dict object were always available, instead
# of passing two node dicts and some names
def merge_relationships_from_dataframe(
        source_node_dict: dict,
        rel_dict: dict,
        destination_node_dict: dict,
        df: pd.DataFrame,
        data_source: str,
        graph
):

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

    # Get right node constraints
    right_node_constraint = destination_node_dict[data_source]['data_source_id']
    df['Right Node Constraints'] = list(zip(df[right_node_constraint]))

    data = df[['Left Node Constraints', 'Property Dictionary', 'Right Node Constraints']].values.tolist()

    merge_relationships(
        graph.auto(),
        data, 'CREATES',
        # start_node_key=(('Person'), 'data_source_id'),
        start_node_key=(tuple(source_node_dict['Labels']), 'data_source_id'),
        end_node_key=(tuple(destination_node_dict['Labels']), 'data_source_id')
    )



# Mostly pasted from Shuyi Yang: https://towardsdatascience.com/neo4j-cypher-python-7a919a372be7
class Neo4jConnection:

    def __init__(self, uri, user, pwd, db):
        self.__uri = uri
        self.__user = user
        self.__pwd = pwd
        self.__default_db = db
        self.__driver = None
        try:
            self.__driver = GraphDatabase.driver(self.__uri, auth=(self.__user, self.__pwd))
        except Exception as e:
            print("Failed to create the driver:", e)

    def close(self):
        if self.__driver is not None:
            self.__driver.close()

    def query(self, query, parameters=None, db=None):
        assert self.__driver is not None, "Driver not initialized!"
        session = None
        response = None
        try:
            session = self.__driver.session(database=db) if db is not None else \
                self.__driver.session(database=self.__default_db)
            response = list(session.run(query, parameters))
        except Exception as e:
            print("Query failed:", e)
        finally:
            if session is not None:
                session.close()
        return response
