from graphdatascience import GraphDataScience
import pandas as pd
from py2neo import Graph
from gds_admin import gds


def generate_JSON(query):
    graphpy2neo = Graph("bolt://localhost:7687", auth=("neo4j", "1234"))
    jsonized = graphpy2neo.run(query).data()
    return jsonized


def generate_communities(query):
    community = gds.run_cypher(
        query
    )
    return community


def project(comm):
    nodeQuery = "MATCH (s:Skill) WHERE s.Skill_community = {comm} RETURN id(s) as id".format(comm=str(comm))
    relaQuery = 'MATCH (u:Skill) -[r:COMMONLY_USED_TOGETHER]->(v:Skill) WHERE u.Skill_community = {comm} AND v.Skill_community = {comm} RETURN id(u) as source, id(v) as target, r.score as weight' \
        .format(comm=str(comm))
    G, res = gds.graph.project.cypher(
        str(comm),
        nodeQuery,
        relaQuery
    )
    print(G)
    print(res)


def pageRank(comm, skill_inp):
    sourceNodes = "{sourceNodes: source_nodes}"
    pageRankAlgo = gds.run_cypher(
        """
        MATCH (s:Skill)
        WHERE s.Skill = "{skill_input}"
        WITH collect(s) as source_nodes
        CALL gds.pageRank.stream(
        "{comm}",
        {sourceNodes}
        )
        YIELD nodeId, score
        RETURN gds.util.asNode(nodeId).name, score
        ORDER BY score DESC
        """.format(comm=str(comm), skill_input=skill_inp, sourceNodes=sourceNodes)
    )
    return pageRankAlgo.to_json()


def generate_graph():
    G, res = gds.graph.project(
        "skillSimilarity",
        ["Person", "Skill"],
        {
            "HAS_SKILL_RE": {
                "type": 'HAS_SKILL',
                "orientation": 'REVERSE'
            }
        }
    )

    nodeSim = gds.nodeSimilarity.mutate(
        G,
        relationshipTypes=['HAS_SKILL_RE'],
        similarityCutoff=0.5,
        mutateRelationshipType='COMMONLY_USED_TOGETHER',
        mutateProperty='score'
    )

    louvain = gds.louvain.write(
        G,
        relationshipTypes=['COMMONLY_USED_TOGETHER'],
        nodeLabels=['Skill'],
        writeProperty='Skill_community',
        relationshipWeightProperty='score'
    )

    gds.graph.writeRelationship(
        G,
        'COMMONLY_USED_TOGETHER',
        'score'
    )

    query1 = """
    MATCH (p1: Skill) -[r:COMMONLY_USED_TOGETHER] - (p2:Skill) 
    RETURN r LIMIT 10
    """
    generate_JSON(query1)

    query2 = """
    MATCH (s:Skill)
    RETURN s.Skill_community, count(*) as communitySize, collect(s.name)[..5] as Skills
    ORDER BY communitySize DESC
    LIMIT 10
    """
    generate_communities(query2)