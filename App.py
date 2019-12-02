from flask import Flask, request, current_app
from obtain.data_obtain import get_soc_blog_catalog
from response.response import Response
import service.service as service
from config.logging import config_log
# config the log
config_log()

app = Flask(__name__)


@app.route('/get_soc_blog_catalog_graph', methods=['GET'])
def get_soc_blog_catalog_graph():
    return Response.success(service.get_graph(current_app.config['soc_blog_graph'], current_app.config['soc_blog_model']))


@app.route('/get_similar_structure', methods=['GET'])
def get_similar_structure():
    """
    data:{
        k:10,
        graph_name:'soc_blog_catalog',
        nodes:[1,2,3,4,5]
    }
    """
    data = request.get_json()
    graph_name = data.get('graph_name')
    nodes = data.get('nodes')
    k = data.get('k')
    return Response.success(service.get_similar_structure(graph_name, nodes, k))


if __name__ == "__main__":
    with app.app_context():
        soc_blog_graph = get_soc_blog_catalog("./data/soc-BlogCatalog.mtx")
        soc_blog_model = service.node2vec(
            soc_blog_graph, "./dump/model/soc_blog_model")
        current_app.config["soc_blog_graph"] = soc_blog_graph
        current_app.config["soc_blog_model"] = soc_blog_model
        app.run(debug=True, host="127.0.0.1", port=5000)
