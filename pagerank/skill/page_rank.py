import json
from pagerank.skill.skill_graph_algorithm import pageRank, project
from pagerank.skill.helper import get_list_community


def create_skill_page_rank_graph(comm):
    project(comm)


# Run this to create new page rank graph in the database. Right now having 16, 192, 171, 297, 241
# create_page_rank_graph("16")

def exec_skill_page_rank(comm, skill):
    result = pageRank(comm, skill)
    return result


# Find a community for skill
def find_skill_community(skills):
    listCommSkills, listCommId = get_list_community()
    response = {}
    existedId = []
    for skill in skills:
        for i in range(len(listCommId)):
            community = listCommSkills[i]
            commId = listCommId[i]
            for s in community:
                # COMPARE TO LOWERCASE
                if s[0].lower() == skill.lower() and commId not in existedId:
                    response[skill] = json.loads(exec_skill_page_rank(commId, skill))
                    existedId.append(commId)
    return response
