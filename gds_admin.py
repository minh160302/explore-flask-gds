from graphdatascience import GraphDataScience
from py2neo import Graph

# Local connection
gds = GraphDataScience("bolt://localhost:11005", auth=("neo4j", "1234"))
graphpy2neo = Graph("bolt://localhost:11005", auth=("neo4j", "1234"))


# TODO: Push Neo4J with GDS to Docker, host on EC2.

# # Aura Neo4J
# gds = GraphDataScience("neo4j+s://aace8fcf.databases.neo4j.io",auth=("neo4j", "4jidkzuGY7B73fQ_EFm1aZPxZNfU1yDosn_lZLbIkpg"))
# graphpy2neo = Graph("neo4j+s://aace8fcf.databases.neo4j.io", auth=("neo4j", "4jidkzuGY7B73fQ_EFm1aZPxZNfU1yDosn_lZLbIkpg"))
