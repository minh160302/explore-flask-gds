from py2neo import Graph
from gds_admin import gds
import logging
from pagerank.share import generate_JSON, generate_communities

logger = logging.getLogger('ftpuploader')


def project(comm):
    """
    Projects the specific community graph using Cypher queries
    @comm: int - number assigned to a specific community
    """
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
    gds.run_cypher(
        """
            CALL gds.graph.drop('skillSimilarity')
        """
    )


def pageRank(comm, skill_inp):
    """
    Run Personalized PageRank algorithm, using certain configurations such as
    +) source nodes(the algorithm will be biased towards a certain source nodes)
    +) maxIterations: iteratate 80 times to converge

    @comm: int - number assigned to a specific skill community
    @skill_inp - personal skills that are used for Personalized algorithm
    """
    sourceNodes = "{sourceNodes: source_nodes}"
    try:
        pageRankAlgo = gds.run_cypher(
            """
            MATCH (s:Skill)
            WHERE s.name = "{skill_input}"
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
    except Exception as e:
        logger.error('Failed to upload to ftp: ' + str(e))
        return {
            "error": str(e)
        }


def check_converge(comm, skill_inp):
    """
    Use stats mode to check whether our algorithm has converged or not
    *MUST CONVERGE*
    The result will return True if converged, False if not

    Extra info: compute milliseconds
    """
    sourceNodes = "{sourceNodes: source_nodes, maxIterations: 80}"
    convergeCheck = gds.run_cypher(
        """
        MATCH (s:Skill)
        WHERE s.name = "{skill_input}" 
        WITH collect(s) as source_nodes
        CALL gds.pageRank.stats(
        "{comm}",
        {sourceNodes}
        )
        YIELD didConverge, computeMillis
        RETURN didConverge, computeMillis
        """.format(comm=str(comm), skill_input=skill_inp, sourceNodes=sourceNodes)
    )
    print(convergeCheck)


def generate_skill_graph():
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


# Stupid intro Feature: see what skill is mostly utilized by people in the company
def betweenness_centrality(network_graph):
    """
    See the "cog in the machine", find the mostly used skill in the company
    """
    betweenness = gds.run_cypher(
        """
        CALL gds.betweenness.stream(
        '{network}'
        )
        YIELD nodeId, score
        RETURN gds.util.asNode(nodeId).name, score
        ORDER BY score DESC
        LIMIT 1
    """.format(network=network_graph)
    )
    print(betweenness)

# betweenness_centrality('skillSimilarity')
# UI intro: our mostly utilized skill is Docker. So learn Docker if ur a software engineer!
