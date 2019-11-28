from flask import Flask, request, current_app
from entity.entity import Node, Edge, Graph
from obtain.data_obain import get_soc_blog_catalog
from response.response import Response
app = Flask(__name__)


@app.route('/', methods=['GET'])
def hello_world():
    print(request.args.get('name'))
    return Response.fail(1, '曹辉')


@app.route('/test', methods=['GET'])
def test_global():
    return Response.success(2, current_app.config['name'])


@app.route('/test2', methods=['GET'])
def test_global2():
    return Response.success(2, current_app.config['name'])


if __name__ == '__main__':
    with app.app_context():
        soc_blog_graph = get_soc_blog_catalog("./data/soc-BlogCatalog.mtx")
        app.run(debug=True, host="127.0.0.1", port=5000)
