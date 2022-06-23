import json
from pagerank.project.project_graph_algorithm import pageRank, project
from pagerank.project.helper import get_project_community


# This function creates a new pagerank graph of project in the database
# Right now having 30, 164, 99, 276, 97, 47, 146, 51, 84
def create_project_page_rank_graph(comm):
    project(comm)


# create_project_page_rank_graph(84)


def exec_project_page_rank(comm, project):
    return pageRank(comm, project)


# Find a community for project
def find_project_community(projectFullName):
    listCommProjects, listCommId = get_project_community()
    response = {}
    for i in range(len(listCommId)):
        community = listCommProjects[i]
        commId = listCommId[i]
        for s in community:
            # COMPARE TO LOWERCASE
            if s[0].lower() == projectFullName.lower():
                response[projectFullName] = json.loads(exec_project_page_rank(commId, projectFullName))
                break

    if response == {}:
        return {
            "error": "This project's name doesn't exist in the database."
        }
    return response
