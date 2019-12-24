from flask import Flask, request, current_app
from obtain.data_obtain import get_soc_blog_catalog
from obtain.data_obtain import get_mock_commutity_graph
from response.response import Response
import service.service as service
from config.logging import config_log
import json
# config the log
config_log()

app = Flask(__name__)


@app.after_request
def cors(environ):
    """Solove the cors problem."""
    environ.headers['Access-Control-Allow-Origin'] = '*'
    environ.headers['Access-Control-Allow-Method'] = '*'
    environ.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return environ


@app.route('/doTasks', methods=['POST'])
def doTasks():
    task = json.load(request.get_data())
    res = {}
    service.doTask(task, res)
    return Response.success(res)


@app.route('/get_graph_by_name', methods=['GET'])
def get_graph_by_name():
    name = request.args.get("name")
    return Response.success(service.get_graph_by_name(name))


@app.route('/get_similar_structure', methods=['POST'])
def get_similar_struc():
    data = json.loads(request.get_data())
    graph_name = data.get('graph_name')
    nodes = data.get('nodes')
    k = data.get('k')
    return Response.success(service.get_similar_struc(graph_name, nodes, k))


@app.route("/get_community_by_name", methods=['GET'])
def get_community_by_name():
    name = request.args.get('name')
    return Response.success(service.get_commutity_by_name(name))


if __name__ == "__main__":
    with app.app_context():
        soc_blog_graph = get_soc_blog_catalog("./data/soc-BlogCatalog.mtx")
        soc_blog_model = service.node2vec(
            soc_blog_graph, "./dump/model/soc_blog_model")
        mock_community_graph = get_mock_commutity_graph(
            "./data/mock_community_graph.txt")
        mock_community_model = service.node2vec(
            mock_community_graph, './dump/model/mock_community_graph')
        # print(patition)
        # print("the shape of parition is %s ." % np.shape(patition))
        # print("the q is %s" % q)
        current_app.config["soc_blog_graph"] = soc_blog_graph
        current_app.config["soc_blog_model"] = soc_blog_model
        current_app.config["mock_community_graph"] = mock_community_graph
        current_app.config["mock_community_model"] = mock_community_model
        # partition = service.get_patition_model_by_name(
        #     'soc_blog_catalog', './dump/community/soc_blog_community')
        # print(partition)
        app.run(debug=True, host="127.0.0.1", port=5000)
