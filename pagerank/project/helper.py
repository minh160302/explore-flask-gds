from gds_admin import gds


# Find all project's communities
def get_project_community():
    communities = gds.run_cypher(
        """
            CALL gds.graph.list()
        """
    ).values.tolist()
    listCommProjects = []
    listCommId = []
    for comm in communities:
        commId = comm[1]
        commProjects = gds.run_cypher(f"""
            MATCH (s:Project) WHERE s.Project_community = {commId} RETURN s.projectFullName
        """.format(commId = commId)).values.tolist()
        listCommProjects.append(commProjects)
        listCommId.append(commId)
    return listCommProjects, listCommId
