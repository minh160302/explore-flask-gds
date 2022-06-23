from flask import Flask, request
from pagerank.skill.page_rank import exec_skill_page_rank, \
    find_skill_community, create_skill_page_rank_graph
from pagerank.skill.skill_graph_algorithm import generate_skill_graph
from pagerank.project.page_rank import find_project_community, create_project_page_rank_graph
from pagerank.project.project_graph_algorithm import generate_project_graph
from pagerank.share import drop
import time

app = Flask(__name__)

"""
    Shared API
"""


@app.route('/api/graph/drop', methods=['POST'])
def drop_graph():
    """
    Drop a graph in the database
    :return: NONE
    """
    args = request.get_json()
    graphName = args.get("graphName")
    drop(str(graphName))
    return '', 204


"""
    Skill API
"""

"""
NOTE: Must drop these graphs before you go:
    skillSimilarity
    projectSimilarity
"""


@app.route('/api/skill/similarity', methods=['POST'])
def skill_create_skill_similarity():
    """
    Create skillSimilarity graph
    WARNING: delete this before add new community groups in
    --->    SOLVED
    :return: NONE
    """
    generate_skill_graph()
    return '', 204


@app.route('/api/skill/page_rank/create_graph', methods=['POST'])
def skill_create_page_rank():
    """
    Create graph for a community based on page rank algorithm
    :return: NONE
    """
    args = request.get_json()
    comm = args.get("community")
    create_skill_page_rank_graph(comm)
    return '', 204


# This endpoint only runs if skill exists in community
@app.route('/api/skill/page_rank', methods=['POST'])
def skill_page_rank():
    """
    responses:
      200:
        description: The community associated with a skill
      400:
        description: ClientError: Please read the error message for more information
    """
    args = request.get_json()
    comm = args.get("community")
    skill = args.get("skill")
    return exec_skill_page_rank(comm, skill)


@app.route('/api/skill/find_community', methods=['POST'])
def skill_find_community():
    """
    responses:
      200:
        description: List of communities based on user's skills
      400:
        description: ClientError: Please read the error message for more information
    """
    # start_time = time.time()
    args = request.get_json()
    skill = args.get("skills")
    communities = find_skill_community(skill)
    # print("--- %s seconds ---" % (time.time() - start_time))
    return communities


"""
    Project API
"""


@app.route('/api/project/similarity', methods=['POST'])
def project_create_project_similarity():
    """
    Create projectSimilarity graph
    WARNING: delete this before add new community groups in
    --->    SOLVED
    :return: NONE
    """
    generate_project_graph()
    return '', 204


@app.route('/api/project/page_rank/create_graph', methods=['POST'])
def project_create_page_rank():
    """
    Create graph for a community based on page rank algorithm
    :return: NONE
    """
    args = request.get_json()
    comm = args.get("community")
    create_project_page_rank_graph(comm)
    return '', 204


@app.route('/api/project/find_community', methods=['POST'])
def project_find_community():
    """
    responses:
      200:
        description: The community associated with a project
      400:
        description: ClientError: Please read the error message for more information
    """
    args = request.get_json()
    projectFullName = args.get("projectFullName")
    return find_project_community(projectFullName)


if __name__ == '__main__':
    app.run()
