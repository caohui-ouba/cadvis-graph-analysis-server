"""
create mock data. for graph
如何生成一个稀疏的社团结构明显的数据。
"""

import random

"""随机生成一个数字 10-20 """
partition_cnt = random.randint(10, 20)

"""每个社团 50-200个节点 """
partitions_size = [random.randint(50, 200) for _ in range(partition_cnt)]

node_size = sum(partitions_size)

"""保存每个社团的范围，从1开始"""
partitions_range = []
current = 0
for size in partitions_size:
    partitions_range.append((current + 1, current + size))
    current += size


def exists(edge, edge_s):
    """判断某个边集合中是否已经存在边"""
    for e in edge_s:
        if edge[0] in e and edge[1] in e:
            return True
    return False


"""给每个社团构造边"""
edges = []
current = 0
for size in partitions_size:
    edges_cnt = range(random.randint(int(size * size / 20),
                                     int(size * size / 10)))
    print("edges cnt = %s." % edges_cnt)
    edge_s = []
    print(current + 1, current + size)
    for _ in edges_cnt:
        edge = (random.randint(current + 1, current + size),
                random.randint(current + 1, current + size))
        if not exists(edge, edge_s):
            edge_s.append(edge)
    current += size
    edges += edge_s


"""社团之间构造稀疏的边 ,5 - 20条"""
for idx in range(partition_cnt):
    for other in range(idx + 1, partition_cnt):
        edge_cnt = random.randint(2, 3)
        edge_s = []
        for _ in range(edge_cnt):
            edge = (random.randint(partitions_range[idx][0], partitions_range[idx][1]), random.randint(
                partitions_range[other][0], partitions_range[other][1]))
            if not exists(edge, edge_s):
                edge_s.append(edge)
        edges += edge_s
        print("%s <-> %s : %s" % (idx, other, len(edge_s)))

with open('./data/mock_community_graph.txt', 'w') as file:
    file.write(str(node_size) + '\n')
    for size in partitions_size:
        file.write(str(size) + ' ')
    file.write('\n')
    for edge in edges:
        file.write(str(edge[0]) + ' ' + str(edge[1]) + '\n')
