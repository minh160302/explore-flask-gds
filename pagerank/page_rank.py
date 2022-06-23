import json

from pagerank.graph_algorithm import pageRank, project, generate_graph
from pagerank.helper import get_list_community


def create_page_rank_graph(comm):
    generate_graph()
    project(comm)


# Run this to create new page rank graph in the database. Right now having 16, 192, 171, 297, 241
# create_page_rank_graph("241")

def exec_page_rank(comm, skill):
    result = pageRank(comm, skill)
    return result


# Find a community for skill
def find_community(skill):
    communities = get_list_community()
    return communities
