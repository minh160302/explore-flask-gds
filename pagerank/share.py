from gds_admin import gds, graphpy2neo


def generate_JSON(query):
    jsonized = graphpy2neo.run(query).data()
    return jsonized


def generate_communities(query):
    """
    Generate community from query
    """
    community = gds.run_cypher(
        query
    )
    return community


def drop(graph):
    gds.run_cypher(
        f"""
            CALL gds.graph.drop("{graph}")
        """.format(graph=str(graph))
    )
    return 0
