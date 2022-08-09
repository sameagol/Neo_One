---
tags:
---

Separate databases for ontology and data graph
- Pro: "Meta" shows up in relationship labels
- Pro: Relationships can only have one type and NO labels
- Con: have to query two different dbs when using the ontology
- Con: have to explain to everyone and their mother that we need two dbs
- Con: [https://neo4j.com/labs/apoc/4.4/database-introspection/meta/](https://neo4j.com/labs/apoc/4.4/database-introspection/meta/)

The reason we can't have [[20220803_Proposed_Ontology_Data_Interaction.excalidraw.png]] is because GUI graph tools are not meant to capture metadata, which is what is wanted. Also, we want more complex functionality (multiple data sources listed) than what GUIs offer.

Is there a way to standardize an instance of Obsidian?

Can get the repo as a zip... how do we get that to NIPR?

Up next:
Insert data... is there a better way than unwind?
- [ ] Try py2neo ogm / Model
- [ ] Try ontology <> data interaction arc
- [ ] Try constraints
- [ ] Try assertions on allowable relationships vs meta graph
- [x] Try Neo4j python package stuff
- [ ] Try using meta to do something within python
- [ ] Try dictionary data insert