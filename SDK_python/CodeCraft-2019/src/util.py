import numpy as np
import  pandas
import matplotlib.pyplot as plt

try:
    import networkx as nx
except ImportError:
    nx = None




def build_adjacency_list(cross_df, road_df):
    """
    brief:从cross和road信息建立邻接表来表示有向图，并定义有向图边的权值
    :param cross_df: cross.txt解析得到的DataFrame结构的数据
    :param road_df: road.txt解析得到的DataFrame结构的数据
    :return: 返回带权值的邻接表:e.g. adjacency_list[1] = {2: [5002, 0.1]}
    """
    # 邻接表结构： 使用复合字典：{节点：{相邻节点1：[边ID，边权重], 相邻节点2：[边ID，边权重], '''}}
    adjacency_list = {}
    weight = 0
    next_cross_id = 0

    for cross_id in cross_df['id']:
        for i in range(4):
            r_id = 'roadID' + str(i+1)

            # 从cross dataframe中得到路的ID
            road = cross_df[r_id][cross_id]
            if road != -1:
                # 得到下一个路口ID
                next_cross_id = road_df['to'][road]

                # 如果获取的'to'路口ID与当前路口ID一样，则说明下一个路口的ID为'from'中存储的路口ID
                if next_cross_id == cross_id:
                    next_cross_id = road_df['from'][road]
                # 设置该条边的权重
                weight = weight_func(road_df['length'][road], road_df['speed'][road])

                # 将数据存入嵌入字典
                if adjacency_list.__contains__(cross_id):
                    adjacency_list[cross_id][next_cross_id] = [road, weight]
                else:
                    adjacency_list[cross_id] = {next_cross_id: [road, weight]}

    return adjacency_list


def adj_list_visualize(adl_list_):
    """
    brief: 将邻接表表征的有向图进行可视化
    :param adl_list_:
    :return:
    """
    G = nx.DiGraph()
    for st in adl_list_.keys():
        for to in adl_list_[st].keys():
            G.add_edge(st, to)

    pos = nx.spring_layout(G)

    # nx.draw_networkx_nodes(G, pos, node_size=700)
    nx.draw_networkx_labels(G, pos, font_size=20, font_family='sans-serif')
    nx.draw(G, pos)
    plt.show()
    pass


def weight_func(road_l, road_mv):
    weight = road_l / road_mv
    return weight


if __name__ == "__main__":
    pass
