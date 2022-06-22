from generate_graph import pageRank, project, generate_graph


def exec_page_rank(comm):
    # generate_graph()
    # project(comm)
    x = pageRank(comm, "Bootstrap")
    print(x)
    return x
    # print(gds.graph.get("16").)

# Wants to learn
#
exec_page_rank("16")