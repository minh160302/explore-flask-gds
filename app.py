from flask import Flask, request
from pagerank.page_rank import exec_page_rank, find_community
import time

app = Flask(__name__)


# This endpoint only runs if skill exists in community
@app.route('/page_rank', methods=['POST'])
def api_page_rank():  # put application's code here
    args = request.get_json()
    comm = args.get("community")
    skill = args.get("skill")
    return exec_page_rank(comm, skill)


@app.route('/find_community', methods=['POST'])
def api_find_community():
    start_time = time.time()
    args = request.get_json()
    skill = args.get("skill")
    find_community(skill)
    print("--- %s seconds ---" % (time.time() - start_time))
    return "nothing yet"


if __name__ == '__main__':
    app.run()
