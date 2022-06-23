from gds_admin import gds


# Find all skill's communities
def get_list_community():
    communities = gds.run_cypher(
        """
            CALL gds.graph.list()
        """
    ).values.tolist()
    listCommSkills = []
    listCommId = []
    # NOTE: Focus on this
    for comm in communities:
        relationshipQuery = comm[7]["relationshipQuery"]
        nodeQuery = comm[7]["nodeQuery"]
        commId = comm[1]
        comSkills = gds.run_cypher(f"""
        MATCH (s:Skill) WHERE s.Skill_community = {commId} RETURN s.name
        """).values.tolist()
        listCommSkills.append(comSkills)
        listCommId.append(commId)

    return listCommSkills, listCommId
    # return communities
