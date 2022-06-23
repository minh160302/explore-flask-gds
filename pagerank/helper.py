import json

from gds_admin import gds


# Find all communities
def get_list_community():
    communities = gds.run_cypher(
        """
            CALL gds.graph.list()
        """
    ).values.tolist()
    # NOTE: Focus on this
    for comm in communities:
        relationshipQuery = comm[7]["relationshipQuery"]
        nodeQuery = comm[7]["nodeQuery"]
        # print(relationshipQuery)
        # print(nodeQuery)
        print(gds.run_cypher("""
        MATCH (s:Skill) WHERE s.Skill_community = 241 RETURN s.name
        """).values)
    # return communities.ge
    # return communities
