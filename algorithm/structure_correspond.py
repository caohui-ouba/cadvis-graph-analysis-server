from sklearn.cluster import SpectralClustering
from gensim.models.word2vec import Word2Vec


def find_structure_correspond(gs: list, g_model: Word2Vec, components: list):
    """
    gs: the specific structure.
    g_model: the graph model.
    components: the similar structure of gs.
    return the correspondence of gs and components
    """
    X = []
    for node_id in gs:
        X.append(g_model.wv.get_vector(str(node_id)))

    spectral = SpectralClustering(n_clusters=(8 if len(X) >= 8 else 3))

    predict = spectral.fit_predict(X)
    max_n = max(predict)
    clusters = [[] for _ in range(max_n + 1)]
    for idx in range(len(predict)):
        clusters[predict[idx]].append(gs[idx])

    # 找到components中的每个节点属于哪个类
    ps = [[] for _ in range(len(predict))]

    all_node_ids = []
    for a in components:
        all_node_ids += a["nodes"]

    for node_id in all_node_ids:
        min_distance = float("Inf")
        min_cluster = -1
        for idx in range(len(clusters)):
            for id in clusters[idx]:
                distance = g_model.wv.distance(str(node_id), str(id))
                if distance < min_distance:
                    min_distance = distance
                    min_cluster = idx
        if min_cluster != -1:
            ps[min_cluster].append(node_id)

    # 为clusters中的每个node对应一个node
    correspond = {}
    for idx in range(len(clusters)):
        visited = []
        for node_id in clusters[idx]:
            min_distance = float("Inf")
            min_node_id = -1
            for target_id in ps[idx]:
                if target_id not in visited:
                    distance = g_model.wv.distance(
                        str(node_id), str(target_id))
                    if distance < min_distance:
                        min_distance = distance
                        min_node_id = target_id
            correspond[str(node_id)] = [min_node_id]
            if min_node_id != -1:
                visited.append(min_node_id)
        # 剩余的没有被分配的节点
        remain = [id for id in ps[idx] if id not in visited]
        # 均匀地分给cluster[idx]的节点
        p = 0
        q = 0
        while q < len(remain):
            correspond[str(clusters[idx][p])].append(remain[q])
            q += 1
            p = (p + 1) % len(clusters[idx])
    return correspond
