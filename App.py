from flask import Flask, request, current_app
from obtain.data_obtain import get_soc_blog_catalog
from response.response import Response
import service.service as service
from config.logging import config_log

# config the log
config_log()

app = Flask(__name__)


@app.route('/', methods=['GET'])
def hello_world():
    print(request.args.get('name'))
    return Response.fail(1, '曹辉')


@app.route('/test', methods=['GET'])
def test_global():
    return Response.success(1, "success", current_app.config['soc_blog_graph'])


@app.route('/test2', methods=['GET'])
def test_global2():
    return Response.success(2, current_app.config['name'])


if __name__ == '__main__':
    with app.app_context():
        soc_blog_graph = get_soc_blog_catalog("./data/soc-BlogCatalog.mtx")
        print(len(soc_blog_graph.nodes()))
        model = service.node2vec(soc_blog_graph, "./dump/model/soc_blog_model")
        # model.wv.most_similar(2)
        # current_app.config["soc_blog_graph"] = soc_blog_graph
        # app.run(debug=True, host="127.0.0.1", port=5000)
