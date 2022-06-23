from gds_admin import gds
from pagerank.share import generate_JSON, generate_communities


def project(comm):
    """
    Projects the specific community graph using Cypher queries
    @comm: int - number assigned to a specific community
    """
    nodeQuery = "MATCH (s:Project) WHERE s.Project_community = {comm} RETURN id(s) as id".format(comm=str(comm))
    relaQuery = 'MATCH (u:Project) -[r:SIMILAR_TO]->(v:Project) WHERE u.Project_community = {comm} AND v.Project_community = {comm} RETURN id(u) as source, id(v) as target, r.score as weight'.format(
        comm=str(comm))
    G, res = gds.graph.project.cypher(
        str(comm),
        nodeQuery,
        relaQuery
    )
    print(G)
    print(res)
    gds.run_cypher(
        """
            CALL gds.graph.drop('projectSimilarity')
        """
    )


def pageRank(comm, project_inp):
    """
    Run Personalized PageRank algorithm, using certain configurations such as
    +) source nodes(the algorithm will be biased towards a certain source nodes)
    +) maxIterations: iteratate 70 times to converge

    @comm: int - number assigned to a specific project community
    @project_inp - Projects that are used for Personalized algorithm
    """

    config = "{sourceNodes: source_nodes, maxIterations: 70}"
    try:
        pageRankAlgo = gds.run_cypher(
            """
            MATCH (s:Project)
            WHERE s.projectFullName = "{project_inp}" 
            WITH collect(s) as source_nodes
            CALL gds.pageRank.stream(
            "{comm}",
            {config}
            )
            YIELD nodeId, score
            RETURN gds.util.asNode(nodeId).projectFullName, score
            ORDER BY score DESC
            """.format(comm=str(comm), project_inp=project_inp, config=config)
        )
        return pageRankAlgo.to_json()
    except Exception as e:
        return {
            "error": str(e)
        }


# Testing function
def check_converge(comm, project_inp):
    """
    Use stats mode to check whether our algorithm has converged or not
    *MUST CONVERGE*
    The result will return True if converged, False if not

    Extra info: compute milliseconds
    """
    config = "{sourceNodes: source_nodes, maxIterations: 70}"
    convergeCheck = gds.run_cypher(
        """
        MATCH (s:Project)
        WHERE s.projectFullName = "{project_inp}" 
        WITH collect(s) as source_nodes
        CALL gds.pageRank.stats(
        "{comm}",
        {config}
        )
        YIELD didConverge, computeMillis
        RETURN didConverge, computeMillis
        """.format(comm=str(comm), project_inp=project_inp, config=config)
    )
    print(convergeCheck)


def generate_project_graph():
    G, res = gds.graph.project(
        "projectSimilarity",
        ["Person", "Project", "Skill"],
        {
            "USES_SKILL": {
                "type": 'USES_SKILL',
                "orientation": 'NATURAL'
            },
            "WORKED_ON": {
                "type": "WORKED_ON",
                "orientation": "REVERSE"
            }
        }
    )

    nodeSim = gds.nodeSimilarity.mutate(
        G,
        relationshipTypes=['USES_SKILL', "WORKED_ON"],
        similarityCutoff=0.5,
        mutateRelationshipType='SIMILAR_TO',
        mutateProperty='score'
    )

    louvain = gds.louvain.write(
        G,
        relationshipTypes=['SIMILAR_TO'],
        nodeLabels=['Project'],
        writeProperty='Project_community',
        relationshipWeightProperty='score'
    )

    gds.graph.writeRelationship(
        G,
        'SIMILAR_TO',
        'score'
    )

    query1 = """
    MATCH (p1: Project) -[r:SIMILAR_TO] - (p2:Project) 
    RETURN r LIMIT 10
    """
    generate_JSON(query1)

    query2 = """
    MATCH (s:Project)
    RETURN s.Project_community, count(*) as communitySize, collect(s.projectFullName)[..5] as Project
    ORDER BY communitySize DESC
    LIMIT 10
    """
    generate_communities(query2)
