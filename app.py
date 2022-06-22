from flask import Flask
from pagerank.page_rank import exec_page_rank

app = Flask(__name__)


@app.route('/page_rank', methods=['GET'])
def hello_world():  # put application's code here
    return


if __name__ == '__main__':
    app.run()
