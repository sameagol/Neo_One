# Neo_One
The first exploration of Neo4j

This is meant to be an example of using python to transform csvs into a knowledge graph using neo4j's python driver.

The documentation is meant to be read and added to using Obsidian (https://obsidian.md) but any text editor should work.

# Requirements
python 3.9, see Documentation/Requirements/xxx_python_requirements.txt
Neo4j desktop: https://neo4j.com/download/
Neo4j APOC plugin: https://neo4j.com/labs/apoc/4.4/installation/#neo4j-desktop

# Design Choices
As of Aug 1, 2020, a discussion point is how to store "allowable relationships" There are options.
1. Don't store allowable relationships explicitly.
    - Neo4j has the ability to extract allowable relationships: https://neo4j.com/labs/apoc/4.4/database-introspection/meta/
2. Create an "ontology" graph... basically a separate knowledge graph where each node is a node type and each relationship
   is a relationship type. No actual data is stored in the ontology graph, just allowable relationships.
3. Use python dictionaries
4. Use config files

Similarly, there are options on where to store metadata. For instance, each "Person" node has a data source "user_data" or whatever.
Where do we keep that information?
1. If we have an ontology graph, we could put it there
2. Store metadata in each actual node instance. So each "Person" node would have data source as a property
    - These may actually change. A Person may come from various data sources... the amount of properties that are truly static is few.
