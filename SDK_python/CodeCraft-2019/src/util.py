"""
some useful data example in the following code:

cross dataframe:
id  roadID1  roadID2  roadID3  roadID4
id
1    1     5000     5005       -1       -1
2    2     5001     5006     5000       -1
3    3     5002     5007     5001       -1
4    4     5003     5008     5002       -1
5    5     5004     5009     5003       -1
...


road dataframe:
id  length  speed  channel  from  to  isDuplex
id
5000  5000      10      5        1     1   2         1
5001  5001      10      5        1     2   3         1
5002  5002      10      5        1     3   4         1
5003  5003      10      5        1     4   5         1
5004  5004      10      5        1     5   6         1
...


function: build_adjacency_list()-->adjacency_list
{1: {2: [5000, 2.0], 7: [5005, 2.0]}, 2: {8: [5006, 2.0], 1: [5000, 2.0], 3: [5001, 2.0]}, 3: {9: [5007, 2.0], 2: [5001, 2.0], 4: [5002, 2.0]}, 4: {10: [5008, 2.0], 3: [5002, 2.0], 5: [5003, 2.0]}, 5: {11: [5009, 2.0], 4: [5003, 2.0], 6: [5004, 2.0]}, 6: {12: [5010, 2.0], 5: [5004, 2.0]}, 7: {8: [5011, 2.0], 1: [5005, 2.0], 13: [5016, 2.0]}, 8: {9: [5012, 2.0], 2: [5006, 2.0], 14: [5017, 2.0], 7: [5011, 2.0]}, 9: {8: [5012, 2.0], 10: [5013, 2.0], 3: [5007, 2.0], 15: [5018, 2.0]}, 10: {16: [5019, 2.0], 9: [5013, 2.0], 11: [5014, 2.0], 4: [5008, 2.0]}, 11: {17: [5020, 2.0], 10: [5014, 2.0], 12: [5015, 2.0], 5: [5009, 2.0]}, 12: {18: [5021, 2.0], 11: [5015, 2.0], 6: [5010, 2.0]}, 13: {19: [5027, 2.0], 14: [5022, 2.0], 7: [5016, 2.0]}, 14: {8: [5017, 2.0], 20: [5028, 2.0], 13: [5022, 2.0], 15: [5023, 2.0]}, 15: {16: [5024, 2.0], 9: [5018, 2.0], 21: [5029, 2.0], 14: [5023, 2.0]}, 16: {17: [5025, 2.0], 10: [5019, 2.0], 22: [5030, 2.0], 15: [5024, 2.0]}, 17: {16: [5025, 2.0], 18: [5026, 2.0], 11: [5020, 2.0], 23: [5031, 2.0]}, 18: {24: [5032, 2.0], 17: [5026, 2.0], 12: [5021, 2.0]}, 19: {25: [5038, 2.0], 20: [5033, 2.0], 13: [5027, 2.0]}, 20: {26: [5039, 2.0], 19: [5033, 2.0], 21: [5034, 2.0], 14: [5028, 2.0]}, 21: {27: [5040, 2.0], 20: [5034, 2.0], 22: [5035, 2.0], 15: [5029, 2.0]}, 22: {16: [5030, 2.0], 28: [5041, 2.0], 21: [5035, 2.0], 23: [5036, 2.0]}, 23: {24: [5037, 2.0], 17: [5031, 2.0], 29: [5042, 2.0], 22: [5036, 2.0]}, 24: {18: [5032, 2.0], 30: [5043, 2.0], 23: [5037, 2.0]}, 25: {26: [5044, 2.0], 19: [5038, 2.0], 31: [5049, 2.0]}, 26: {32: [5050, 2.0], 25: [5044, 2.0], 27: [5045, 2.0], 20: [5039, 2.0]}, 27: {33: [5051, 2.0], 26: [5045, 2.0], 28: [5046, 2.0], 21: [5040, 2.0]}, 28: {34: [5052, 2.0], 27: [5046, 2.0], 29: [5047, 2.0], 22: [5041, 2.0]}, 29: {35: [5053, 2.0], 28: [5047, 2.0], 30: [5048, 2.0], 23: [5042, 2.0]}, 30: {24: [5043, 2.0], 36: [5054, 2.0], 29: [5048, 2.0]}, 31: {32: [5055, 2.0], 25: [5049, 2.0]}, 32: {33: [5056, 2.0], 26: [5050, 2.0], 31: [5055, 2.0]}, 33: {32: [5056, 2.0], 34: [5057, 2.0], 27: [5051, 2.0]}, 34: {33: [5057, 2.0], 35: [5058, 2.0], 28: [5052, 2.0]}, 35: {34: [5058, 2.0], 36: [5059, 2.0], 29: [5053, 2.0]}, 36: {35: [5059, 2.0], 30: [5054, 2.0]}}

function: build_ad_list_without_edge_id()-->ad_list_without_edge_id
{1: {2: 2.0, 7: 2.0}, 2: {8: 2.0, 1: 2.0, 3: 2.0}, 3: {9: 2.0, 2: 2.0, 4: 2.0}, 4: {10: 2.0, 3: 2.0, 5: 2.0}, 5: {11: 2.0, 4: 2.0, 6: 2.0}, 6: {12: 2.0, 5: 2.0}, 7: {8: 2.0, 1: 2.0, 13: 2.0}, 8: {9: 2.0, 2: 2.0, 14: 2.0, 7: 2.0}, 9: {8: 2.0, 10: 2.0, 3: 2.0, 15: 2.0}, 10: {16: 2.0, 9: 2.0, 11: 2.0, 4: 2.0}, 11: {17: 2.0, 10: 2.0, 12: 2.0, 5: 2.0}, 12: {18: 2.0, 11: 2.0, 6: 2.0}, 13: {19: 2.0, 14: 2.0, 7: 2.0}, 14: {8: 2.0, 20: 2.0, 13: 2.0, 15: 2.0}, 15: {16: 2.0, 9: 2.0, 21: 2.0, 14: 2.0}, 16: {17: 2.0, 10: 2.0, 22: 2.0, 15: 2.0}, 17: {16: 2.0, 18: 2.0, 11: 2.0, 23: 2.0}, 18: {24: 2.0, 17: 2.0, 12: 2.0}, 19: {25: 2.0, 20: 2.0, 13: 2.0}, 20: {26: 2.0, 19: 2.0, 21: 2.0, 14: 2.0}, 21: {27: 2.0, 20: 2.0, 22: 2.0, 15: 2.0}, 22: {16: 2.0, 28: 2.0, 21: 2.0, 23: 2.0}, 23: {24: 2.0, 17: 2.0, 29: 2.0, 22: 2.0}, 24: {18: 2.0, 30: 2.0, 23: 2.0}, 25: {26: 2.0, 19: 2.0, 31: 2.0}, 26: {32: 2.0, 25: 2.0, 27: 2.0, 20: 2.0}, 27: {33: 2.0, 26: 2.0, 28: 2.0, 21: 2.0}, 28: {34: 2.0, 27: 2.0, 29: 2.0, 22: 2.0}, 29: {35: 2.0, 28: 2.0, 30: 2.0, 23: 2.0}, 30: {24: 2.0, 36: 2.0, 29: 2.0}, 31: {32: 2.0, 25: 2.0}, 32: {33: 2.0, 26: 2.0, 31: 2.0}, 33: {32: 2.0, 34: 2.0, 27: 2.0}, 34: {33: 2.0, 35: 2.0, 28: 2.0}, 35: {34: 2.0, 36: 2.0, 29: 2.0}, 36: {35: 2.0, 30: 2.0}}

node path:
shortest path is: [1, 2, 8, 14, 20]

edge path: [5005, 5016, 5027, 5033]

"""

# import numpy as np
# import  pandas
import copy
from queue import Queue
import matplotlib.pyplot as plt
import numpy as np

from dijkstra.dijkstra import shortest_path

from utilzp import *
from floyd import *

from hp_finder import HamiltonianPath

from tqdm import tqdm

def tqdm(x):
    return x

try:
    global USE_NETWORKX
    # if USE_NETWORKX = True, use networkx lib to get shortest path as default; if import failed, then use dijkstra lib
    # if USE_NETWORKX = True, use dijkstra lib to get shortest path
    USE_NETWORKX = True
    import networkx as nx
    from networkx.algorithms import tournament
    from networkx.algorithms import cycles
except ImportError:
    nx = None
    USE_NETWORKX = False


def build_adjacency_list(cross_df, road_df):
    """
    brief:从cross和road信息建立带有边ID的邻接表来表示有向图，并定义有向图边的权值
    :param cross_df: cross.txt解析得到的DataFrame结构的数据
    :param road_df: road.txt解析得到的DataFrame结构的数据
    :return: 返回带权值的邻接表:e.g. adjacency_list[1] = {2: [5002, 0.1]}
    """
    # 带有边ID的邻接表结构： 使用嵌套字典：{节点：{相邻节点1：[边ID，边权重], 相邻节点2：[边ID，边权重], '''}}
    adjacency_list = {}
    # 计算一些重要的道路统计信息
    # pandas.series.mean() 求均值
    # pandas.series.max()  求最大值
    channel_max = road_df['channel'].max()  # 求最大车道数
    road_df['time'] = road_df.apply(lambda x: (x['length'] / x['speed']), axis=1)
    time_cost_max = road_df['time'].max()  # 求所有路长度除以速度的最大值
    time_cost_mean = road_df['time'].mean()  # 求所有路长度除以速度的均值

    # weight = 0
    # next_cross_id = 0

    for cross_id in cross_df['id']:
        for i in range(4):
            r_id = 'roadID' + str(i+1)

            # 从cross dataframe中得到路的ID
            road = cross_df[r_id][cross_id]
            if road != -1:
                # 得到下一个路口ID
                next_cross_id = road_df['to'][road]

                # 如果获取的'to'路口ID与当前路口ID一样，则说明下一个路口的ID为'from'中存储的路口ID
                if (next_cross_id == cross_id) and (road_df['isDuplex'][road] == 1):
                    next_cross_id = road_df['from'][road]
                # 设置该条边的权重
                # weight = weight_func(road_df['length'][road], road_df['speed'][road])
                weight = weight_func(road_df['time'][road],
                                     road_df['channel'][road],
                                     cha_max=channel_max,
                                     t_mean=time_cost_mean)

                # 将数据存入嵌套字典
                if adjacency_list.__contains__(cross_id):
                    adjacency_list[cross_id][next_cross_id] = [road, weight]
                else:
                    adjacency_list[cross_id] = {next_cross_id: [road, weight]}

    return adjacency_list


def build_ad_list_without_edge_id(cross_df, road_df):
    """
    brief: 从cross_df, road_df得到不带边ID的邻接表
    :param cross_df:
    :param road_df:
    :return:
    """
    # 不带边ID的邻接表结构： 使用嵌套字典：{节点：{相邻节点1：边权重, 相邻节点2：边权重, '''}}
    ad_list_without_edge_id = {}

    # 计算一些重要的道路统计信息
    # pandas.series.mean() 求均值
    # pandas.series.max()  求最大值
    channel_max = road_df['channel'].max()  # 求最大车道数
    road_df['time'] = road_df.apply(lambda x: (x['length'] / x['speed']), axis=1)
    time_cost_max = road_df['time'].max()  # 求所有路长度除以速度的最大值
    time_cost_mean = road_df['time'].mean()  # 求所有路长度除以速度的均值
    # weight = 0
    # next_cross_id = 0

    for cross_id in cross_df['id']:
        for i in range(4):
            r_id = 'roadID' + str(i + 1)

            # 从cross dataframe中得到路的ID
            road = cross_df[r_id][cross_id]
            if road != -1:
                # 得到下一个路口ID
                next_cross_id = road_df['to'][road]

                # 如果获取的'to'路口ID与当前路口ID一样，则说明下一个路口的ID为'from'中存储的路口ID
                if (next_cross_id == cross_id) and (road_df['isDuplex'][road] == 1):
                    next_cross_id = road_df['from'][road]
                # 设置该条边的权重
                # weight = weight_func(road_df['length'][road], road_df['speed'][road])
                weight = weight_func(road_df['time'][road],
                                     road_df['channel'][road],
                                     cha_max=channel_max,
                                     t_mean=time_cost_mean)

                # 将数据存入嵌套字典
                if ad_list_without_edge_id.__contains__(cross_id):
                    ad_list_without_edge_id[cross_id][next_cross_id] = weight
                else:
                    ad_list_without_edge_id[cross_id] = {next_cross_id: weight}

    return ad_list_without_edge_id


def build_ad_list_without_weight(cross_df, road_df, str_pattern=False):
    """
    brief: 从cross_df, road_df得到不带边ID的邻接表
    :param cross_df:
    :param road_df:
    :return:
    """
    # 不带边ID的邻接表结构： 使用嵌套字典：{节点：{相邻节点1：边权重, 相邻节点2：边权重, '''}}
    ad_list_without_weight = {}
    # weight = 0
    # next_cross_id = 0

    for cross_id in cross_df['id']:
        for i in range(4):
            r_id = 'roadID' + str(i + 1)

            # 从cross dataframe中得到路的ID
            road = cross_df[r_id][cross_id]
            if road != -1:
                # 得到下一个路口ID
                next_cross_id = road_df['to'][road]

                # 如果获取的'to'路口ID与当前路口ID一样，则说明下一个路口的ID为'from'中存储的路口ID
                if (next_cross_id == cross_id) and (road_df['isDuplex'][road] == 1):
                    next_cross_id = road_df['from'][road]
                # 设置该条边的权重
                # weight = weight_func(road_df['length'][road], road_df['speed'][road])

                # 将数据存入嵌套字典
                if not str_pattern:
                    if ad_list_without_weight.__contains__(cross_id):
                        ad_list_without_weight[cross_id].append(next_cross_id)
                    else:
                        ad_list_without_weight[cross_id] = [next_cross_id]
                else:
                    if ad_list_without_weight.__contains__(str(cross_id)):
                        ad_list_without_weight[str(cross_id)].append(str(next_cross_id))
                    else:
                        ad_list_without_weight[str(cross_id)] = [str(next_cross_id)]

    return ad_list_without_weight


def convert_adl2adl_w(adl):
    """
    brief: 将带有边ID的邻接表转换为不带边ID的邻接表
    :param adl: 带有边ID的邻接表
    :return:
    """
    adl_w = copy.deepcopy(adl)
    for key, value in adl_w.items():
        for k, v in value.items():
            adl_w[key][k] = v[1]

    return adl_w


def get_path_n2e(path_n, ad_list):
    """
    brief: 将有节点构成的路径转换为有边ID构成的路径
    :param path_n:由节点构成的路径
    :param ad_list:由build_adjacency_list函数得到的带有边ID的邻接表
    :return: path_e:返回由边ID构成的路径
    """
    path_e = []
    if len(path_n) != 0:
        if len(path_n) != 1:
            for n1, n2 in zip(path_n[:-1], path_n[1:]):
                path_e.append((ad_list[n1][n2])[0])
        else:
            return []
    else:
        raise Exception("cannot get edge path from empty node path")
    return path_e


def get_node_from_pairs(pairs_):
    """
    从节点对里找出所有节点
    :param pairs_:
    :return:
    """
    nodes = []
    for p in pairs_:
        if p[0] not in nodes:
            nodes.append(p[0])
        if p[1] not in nodes:
            nodes.append(p[1])

    return nodes


def __get_value_in_list(sl, start, end):
    """
    从列表中获取元素start, end之前的值
    :param sl:单元素列表
    :param start:
    :param end:
    :return:
    """
    if start not in sl or end not in sl:
        raise Exception("Invalid input for start or end.")

    sub_list = sl[sl.index(start):sl.index(end)]

    if len(sub_list) == 0:
        sl_reverse = sl[::-1]
        sub_list = sl_reverse[sl_reverse.index(start):sl_reverse.index(end)]
    # 记得加上尾元素
    sub_list.append(end)

    return sub_list


def __get_value_in_cycle_list(cl, start, end):
    """
    cl列表中的元素首位相连构成环，获取环中任意两点间最短边的子列表
    """
    cycle_list = cl + cl
    
    # start
    s_index = cycle_list.index(start)
    
    temp = cycle_list[s_index:(s_index+len(cl)+1)]
    
    path1 = __get_value_in_list(temp, start, end)
    
    temp.reverse()
    path2 = __get_value_in_list(temp, start, end)
    
    if len(path1) < len(path2):
        return path1
    else:
        return path2
    
    
def adj_list_visualize(adl_list_):
    """
    brief: 将邻接表表征的有向图进行可视化
    :param adl_list_:带有边ID的邻接表
    :return:
    """
    G = nx.DiGraph()
    for st in adl_list_.keys():
        for to in adl_list_[st].keys():
            G.add_edge(st, to)

    # 选择nx.spectral_layout排列节点效果更好一些
    # pos = nx.spring_layout(G)
    pos = nx.spectral_layout(G)

    # nx.draw_networkx_nodes(G, pos, node_size=700)
    # nx.draw_networkx_labels(G, pos, font_size=20, font_family='sans-serif')
    nx.draw(G, pos, with_labels=True)
    plt.show()
    return G


def cut_adjacency_list(adl_, road_df, cut_speed_level=0, cut_channel_level=0):
    """
    传入带边信息的邻接表，格式：{1: {9: [5007, 2.5], 2: [5000, 2.5]}, 2: {1: [5000, 2.5], 10: [5008, 2.0],,对邻接表进行剪枝
    剪枝原则： 1.减掉两个节点间非双向的连接
            2.根据道路的最大速度进行剪枝，考虑先将最大速度、车道小于某个值的道路剪掉，根据Hamiltonian Path的搜索情况再决定是否继续剪枝
    :param road_df: road dateframe
    :param cut_channel_level:
    :param cut_speed_level:
    :param adl_:
    :return:
    """
    # 得到不带边信息的邻接表
    adwE = convert_adl2adl_w(adl_)

    # duplex connect pairs
    # single connect pairs
    d_connect_pairs = []
    s_connect_pairs = []

    # rest pairs after cutted by speed or channel parameter
    rest_pairs = []

    # 剪枝，减掉非双相连接的节点
    for key, value in adwE.items():
        for next_node in value.keys():

            if adwE[next_node].__contains__(key):
                # 当前节点间是双向连接
                if ([key, next_node] not in d_connect_pairs) and ([next_node, key] not in d_connect_pairs):
                    d_connect_pairs.append([key, next_node])

            else:
                # 当前节点间不是双向连接
                if [key, next_node] not in s_connect_pairs:
                    s_connect_pairs.append([key, next_node])

    if cut_speed_level != 0:
        # 将双向道路中通行速度小于cut_speed_level的减掉
        dcp_temp = copy.deepcopy(d_connect_pairs)
        for pair in dcp_temp:
            # 根据带边ID的邻接表得到对应的边ID
            roadID = (adl_[pair[0]][pair[1]])[0]
            if (road_df['speed'][roadID] <= cut_speed_level) or (road_df['channel'][roadID] <= cut_channel_level):
                # 剪掉
                d_connect_pairs.remove(pair)
                # 回收剪掉的pair
                rest_pairs.append(pair)

        return d_connect_pairs, s_connect_pairs, rest_pairs

    elif cut_channel_level != 0:
        dcp_temp = copy.deepcopy(d_connect_pairs)
        for pair in dcp_temp:
            # 根据带边ID的邻接表得到对应的边ID
            roadID = (adl_[pair[0]][pair[1]])[0]
            if road_df['channel'][roadID] <= cut_speed_level:
                # 剪掉
                d_connect_pairs.remove(pair)
                # 回收剪掉的pair
                rest_pairs.append(pair)

        return d_connect_pairs, s_connect_pairs, rest_pairs

    else:
        pass

    return d_connect_pairs, s_connect_pairs, rest_pairs


# # TODO: 权重函数还没有进行科学设置
# def weight_func(road_l, road_mv):
#     weight = road_l / road_mv
#     return weight
def weight_func(time_cost, cha, cha_max=8, t_mean=3, la1=1, la2=0.5):
    """
    time_cost: Length / speed
    cha_max: 最大车道数
    t_mean:  Length / speed的均值
    t_max: Length / speed的最大值
    weight: weight的预计范围为[0.1, t_max]
    """
    weight = la1 * time_cost + la2 * (- cha / cha_max * t_mean)

    # 设置weight的下界为0.1
    if weight <= 0:
        weight = 0.1
    return weight


def update_weight(adwE_, path_n_, typeU=0, weight_factor=0.1):
    """
    根据道路使用情况实时更新道路权重，边使用次数为设边使用次数为N，则对该条边的权重影响为：
          weight = weight + N * 0.05
    adwE_ :不带边ID的邻接表
    path_n_:规划出来的路径,由节点构成
    typeU :更新权重的类型， =0表示将当前path累加到之前的权重
                         =1表示将当前的path从之前的权重中去除
    weight_factor: 表示一条路在路径中出现一次对该路权重的影响因子，通过估计每条路车辆承载量
                   和weight原始范围[0.1, T_mean]来决定weight_factor的取值
    log: weight_factor=0.05
         weight_factor=0.08 controlcarnum = 41  # 37 39:414 414  42:405 fail    3 6 40s  3 6 41s(401,412)
         weight_factor=0.1 42:415 fail  41s(414,410)
         weight_factor=0.05 42:412 fail
         weight_factor=0.03 42:failed fail
    """

    # 根据path累加权重
    if typeU == 0:
        for node, next_node in zip(path_n_[:-1], path_n_[1:]):
            if adwE_.__contains__(node):
                adwE_[node][next_node] += weight_factor
            else:
                raise Exception("the adwE not correct")
    elif typeU == 1:
        for node, next_node in zip(path_n_[:-1], path_n_[1:]):
            if adwE_.__contains__(node):
                adwE_[node][next_node] -= weight_factor

                # 限定weight的下界
                if adwE_[node][next_node] <= 0:
                    adwE_[node][next_node] = 0.1
            else:
                raise Exception("the adwE not correct")
    else:
        raise Exception("wrong typeU for update weight")

    return adwE_


def get_bestHCHP(dp_pairs, searchNum=200, n=3, bestType=0):
    """
    从给定的双向对中获取最佳的HC和HP
    :pairs: 双向对
    :searchNum: 搜索次数设置
    :n: n是从HP头尾搜索HC时搜索元素的个数
    :bestType: 表示返回的HC和HP的最优类型，默认是确保HC是最优，同时将生成HC的HP作为最优,若HC不存在最优
               bestType = 1: 表示返回的HP和HC均为最优，但是HP和HC没有从属关系
    """
    
    nodes = get_node_from_pairs(dp_pairs)
    graph = HamiltonianPath(len(nodes))
    graph.pairs = dp_pairs
    
    # set initial length
    hpLength = int(len(nodes) / 5)
    hcLength = int(len(nodes) / 5)
    
    bestHP = []
    bestHC = []
    bestHCP = []

    print("get_bestHCHP：")
    for x in tqdm(range(1, searchNum)):
        output = graph.isHamiltonianPathExist()
        solution = output[0]
        # if len(solution) == numOfNodes:
        #     yes += 1
        # else:
        #     no += 1
        
        # 求得最优HP
        if len(solution) > hpLength:
                bestHP = solution
                hpLength = len(solution) 
        if len(solution) > hcLength:
            # 搜索HC
            for st in solution[:n]:
                for ed in solution[-n:]:
                    # st = output[0][0]
                    # ed = output[0][-1]
                    if ([st, ed] in dp_pairs) or ([ed, st] in dp_pairs):
                        bestHCP = solution
                        bestHC = __get_value_in_list(solution, st, ed)
                        hcLength = len(bestHC)
#          
#                        print('st, ed:', st, ed)
#                        print('Hamiltonian Cycle:', len(output[0]))
#                        print('output[0]:', output[0])
        else:
            pass
    
    if 1 == bestType:
        return [bestHP, bestHC]
        
    return [bestHCP, bestHC]


def __isGoStraight(nodeL, adl_list, cross_df):
    """
    判断当前节点构成的路线是否是直行通道
    nodeL: 节点列表[pre_node, node, next_node]
    adl_list: 带边ID的邻接表
    road_df: road dataframe
    """
    if len(nodeL) != 3:
        raise Exception("Input wrong node list.")
    road = adl_list[nodeL[0]][nodeL[1]][0]  # 得到上一节点和当前节点之间的路
    road_next = adl_list[nodeL[1]][nodeL[2]][0]  # 得到当前节点和下一节点之间的路

    # 得到node节点周围四条路的ID
    roads = list(cross_df.loc[nodeL[1]])[1:]

    road_index = roads.index(road)
    road_next_index = roads.index(road_next)

    # 当两条路的不相邻时，构成的路线为直行
    if abs(road_index - road_next_index) == 2:
        return True
    else:
        return False


def get_straight_num(path_, adl_list, cross_df):
    """从给定的路径中判断直行的次数"""
    num = 0
    for pre_node, node, next_node in zip(path_[:-2], path_[1:-1], path_[2:]):
        if __isGoStraight([pre_node, node, next_node], adl_list, cross_df):
            num += 1

    return num


def get_bestHCHP_with_direction(dp_pairs, adl_list, cross_df, searchNum=200, n=3, bestType=0):
    """
    从给定的双向对中获取最佳的HC和HP,满足直行道路最多
    :pairs: 双向对
    :adl_list: 带边ID的邻接表
    :cross_df: cross dataframe
    :searchNum: 搜索次数设置
    :n: n是从HP头尾搜索HC时搜索元素的个数
    :bestType: 表示返回的HC和HP的最优类型，默认是确保HC是最优，同时将生成HC的HP作为最优,若HC不存在最优
               bestType = 1: 表示返回的HP和HC均为最优，但是HP和HC没有从属关系
    """

    nodes = get_node_from_pairs(dp_pairs)
    graph = HamiltonianPath(len(nodes))
    graph.pairs = dp_pairs

    # set initial length
    hpLength = int(len(nodes) / 5)
    hcLength = int(len(nodes) / 5)
    hcStraightNum = 0

    bestHP = []
    bestHC = []
    bestHCP = []

    print("Finding Hamiltonian Paths...")
    for x in tqdm(range(1, searchNum)):
        output = graph.isHamiltonianPathExist()
        solution = output[0]
        # if len(solution) == numOfNodes:
        #     yes += 1
        # else:
        #     no += 1

        # 求得最优HP
        if len(solution) > hpLength:
            bestHP = solution
            hpLength = len(solution)
        if len(solution) > hcLength - 3:  # -3 为了放松对hc长度的要求，为了找到更多的直行
            # 搜索HC
            for st in solution[:n]:
                for ed in solution[-n:]:
                    # st = output[0][0]
                    # ed = output[0][-1]
                    if ([st, ed] in dp_pairs) or ([ed, st] in dp_pairs):

                        temp = __get_value_in_list(solution, st, ed)

                        temp_num = get_straight_num(temp, adl_list, cross_df)

                        if temp_num > hcStraightNum:
                            hcStraightNum = temp_num
                            bestHCP = solution
                            bestHC = temp
                            hcLength = len(bestHC)
        #
        #                        print('st, ed:', st, ed)
        #                        print('Hamiltonian Cycle:', len(output[0]))
        #                        print('output[0]:', output[0])
        else:
            pass

    if 1 == bestType:
        return [bestHP, bestHC]

    return [bestHCP, bestHC]


def remove_hp_from_dp(dp_, hp):
    """
    将duplex pairs中含有的hamiltonian path pairs删除，参见cut_adjacency_list()返回的数据
    :param dp_: duplex pairs, 数据举例[[1, 9], [1, 2], [2, 10], [2, 3], [3, 11], [4, 12],...]
    :param hp: hamiltonian path, 数据举例[46, 38, 37, 36, 28, 29, 30, 22, 21, 20, 19, 27...]
    :return: 返回删除后的dp
    """
    for node, next_node in zip(hp[:-1], hp[1:]):
        if [node, next_node] in dp_:
            dp_.remove([node, next_node])
        elif [next_node, node] in dp_:
            dp_.remove([next_node, node])
        else:
            pass
            # print('[node, next_node]:', [node, next_node])
            #TODO: SOME ERROR HERE TO DEBUG
            # raise Exception('hp pairs not in duplex pairs')
    return dp_


def rebuild_adl_from_hp(adl_, dp_, sp_, rp_, hp):
    """
    从剪枝之后的duplex pairs, simple pairs和hamiltonian path生成新的邻接表
    dp_, sp_, rp_: 参见cut_adjacency_list()返回的数据
    :param adl_: 带有权重和边信息的原始邻接表, 数据举例:{1: {9: [5007, 2.5], 2: [5000, 2.5]}, 2: {1: [5000, 2.5], 10: [5008, 2.0],...}}
    :param dp_: 剪枝留下的用于寻找hamiltonian path的双向对, 数据举例[[1, 9], [1, 2], [2, 10], [2, 3], [3, 11], [4, 12],...]
    :param sp_: 剪枝剪掉的单向对， 格式同上，但有方向指向
    :param rp_: 剪枝剪掉的双向对， 格式同上
    :param hp: 从剪枝留下的主干dp_生成的hamiltonian path, 数据举例[46, 38, 37, 36, 28, 29, 30, 22, 21, 20, 19, 27...]
    :return: 返回新的邻接表, 格式{1: {9: 2.5, 2: 2.5}, 2: {1: 2.5, 10: 2.0, 3: 4.5},...}
    """
    # 新的邻接表, 数据格式： 带权重，不带边
    new_adl = {}

    # 将带边信息的邻接表转化为不带便的邻接表
    adwE = convert_adl2adl_w(adl_)

    # 得到所有不在hamiltonian path中的双向对
    all_dp = rp_ + remove_hp_from_dp(dp_, hp)

    # 将hp中的所有节点作为一个大节点，命名为'HP',且'HP'继承它所包含节点的邻接关系
    # hp是list
    for node, value in adwE.items():
        for next_node, weight in value.items():
            # 如果node和指向的next node都在hp中,则不用添加至新邻接表，因为它们均为'HP'节点--->这种想法错误
            # 会导致很多邻接关系丢失，应该将这种情况看为'HP' <---> node,和'HP' <---> next_node共四种单向连接关系
            if (node in hp) and (next_node in hp):
                # if new_adl.__contains__('HP'):
                #     # TODO:这种情况的weight待定？？？????????????????????????????????????有待讨论
                #     new_adl['HP'][next_node] = weight
                #     new_adl['HP'][node] = weight
                # else:
                #     new_adl['HP'] = {next_node: weight}
                #     new_adl['HP'] = {node: weight}
                #
                # if new_adl.__contains__(node):
                #     new_adl[node]['HP'] = weight
                # else:
                #     new_adl[node] = {'HP': weight}
                #
                # if new_adl.__contains__(next_node):
                #     new_adl[next_node]['HP'] = weight
                # else:
                #     new_adl[next_node] = {'HP': weight}

                break

            # 否则按照指向添加至新邻接表
            # 'HP' -> other node
            if node in hp:
                if new_adl.__contains__('HP'):
                    new_adl['HP'][next_node] = weight
                else:
                    new_adl['HP'] = {next_node: weight}
            # other node -> 'HP'
            elif next_node in hp:
                if new_adl.__contains__(node):
                    new_adl[node]['HP'] = weight
                else:
                    new_adl[node] = {'HP': weight}
            # 非ph中的节点间的邻接关系保持不变
            else:
                if new_adl.__contains__(node):
                    new_adl[node][next_node] = weight
                else:
                    new_adl[node] = {next_node: weight}

    return new_adl


def get_path_with_hp_simple(adl_, hp, start, end, use_networkx=False):
    """
    直接使用重规划将dijkstra规划得到的路接入HP中
    """
    adl_list_w = convert_adl2adl_w(adl_)
    
    path_origin = shortest_path(adl_list_w, start, end)
    
    path = replan_for_hp(hp, path_origin)
    
    return path


def get_path_with_hc_simple(adwE_, hc, start, end, use_networkx=False):
    """
    直接使用重规划将dijkstra规划得到的路接入HC中
    """
    #    adl_list_w = convert_adl2adl_w(adl_)

    path_origin = shortest_path(adwE_, start, end)

    #    print('origin path:', path_origin)

    path = replan_for_hc(hc, path_origin)

    return path


def replan_for_hc(hc, path_origin_):
    """
    将dijkstra规划出来的path_origin_接入HC
    :param path_origin_:
    :param hc:
    :param path_origin:
    :return:
    """

    # print(hp, path_)
    rt_index = 0
    lf_index = 0
    lf = 0
    rt = 0
    for a in path_origin_:
        if a in hc:
            lf = a
            lf_index = path_origin_.index(a)
            break
        else:
            lf_index = 0

    for b in path_origin_[::-1]:
        if b in hc:
            rt = b
            rt_index = path_origin_.index(b)
            break
        else: 
            rt_index = 0

    # print(lf_index,rt_index,lf,rt)
    
    # 如果满足替换条换条件则替换
    if lf_index < rt_index:
        path_origin_ = path_origin_[:lf_index] + __get_value_in_cycle_list(hc, lf, rt) + path_origin_[rt_index+1:]

    return path_origin_


# TODO: improve this function to multi-process
def get_all_paths_with_hc(adl_list, road_df, carIDL, startL, endL, use_networkx=False):

    paths = {}
    adl_list_w = convert_adl2adl_w(adl_list)

    # 剪枝
    dp, sp, rp = cut_adjacency_list(adl_list, road_df, cut_channel_level=0, cut_speed_level=1)
    
    _, hc = get_bestHCHP(dp)

    # 基于get_path_with_hp()函数进行路径规划
    # 为所有车各规划一条最短路径
    print("\nget_all_paths_with_hc:")
    for carID, st, ed in tqdm(zip(carIDL, startL, endL)):
        try:
#            path_n = get_path_with_hp(new_ad, adl_list, hp, st, ed)
#            path_n = get_path_with_hp_simple(adl_list, hp, st, ed)
            path_n = get_path_with_hc_simple(adl_list, hc, st, ed)
        except:
            # print("hp", hp)
            # print("error:st, ed", st, ed)
            path_n = shortest_path(adl_list_w, st, ed)
            path_n = replan_for_hc(hc, path_n)

        # 将规划得到的节点构成的路径转换为边构成的路径
        path_e = get_path_n2e(path_n, adl_list)

        paths[carID] = path_e

    return paths


# TODO: 效果不好，有待考虑
def get_all_paths_with_weight_update(adl_list, road_df, car_df, cross_df, pathType=0, update_w=True, use_networkx=False):
    """
    路劲规划时，权重实时更新
    adl_list: 原始邻接表
    road_df： road dateframe
    car_df： car dateframe
    pathType： 路径规划的方法:  =0: 基于HC
                             =1: 基于HP
                             =2: 基于原始Dijkstra算法
    log: i>800 get_time_plan5 controlcarnum = 38:  411 422
         i>800 get_time_plan5 controlcarnum = 39   411 failed
    """
    # 根据每辆车的计划出发时间进行升序排列
    car_df_sort = car_df.sort_values(by=['planTime', 'id'], axis=0, ascending=[True, True])
    # car_len = len(car_df_sort['id'])

    paths = {}
    size = car_df_sort['id'].shape[0]
    shares = 3

    adl_list_w = convert_adl2adl_w(adl_list)
    adl_list_w_bkp = copy.deepcopy(adl_list_w)
    interval = int(size / shares)

    # 剪枝
    # cut_channel_level=1 2629   cut_channel_level=2 774+668  cut_channel_level=3 583+dead lock
    # i > 150,100,80  m1 failed
    # i > 150,100,80 m2 succeed
    # cut_channel_level=0  1563 i > 350     controlcarnum = 35 m1 failed
    ## 为了更新权重使用的一些参数和变量
    pathQueue = Queue()
    i = 0
    startFlag = 0

    print("get_all_paths_with_weight_update:")
    # 为所有车各规划一条最短路径
    for carID, st, ed in tqdm(zip(car_df_sort['id'], car_df_sort['from'], car_df_sort['to'])):

        i += 1

        if pathType == 0:  # 基于HC
            try:
                #                path_n = get_path_with_hp(new_ad, adl_list, hp, st, ed)
                #                path_n = get_path_with_hp_simple(adl_list, hp, st, ed)
                dp, sp, rp = cut_adjacency_list(adl_list, road_df, cut_channel_level=1, cut_speed_level=1)
                _, hc = get_bestHCHP_with_direction(dp, adl_list, cross_df, searchNum=400)
                path_n = get_path_with_hc_simple(adl_list_w, hc, st, ed)

            except:
                # print("hp", hp)
                # print("error:st, ed", st, ed)
                path_n = shortest_path(adl_list_w, st, ed)
                path_n = replan_for_hc(hc, path_n)

            finally:
                if update_w:
                    # 更新权重操作
                    # 首先是权重累积
                    adl_list_w = update_weight(adl_list_w, path_n, typeU=0)
                    # 将累加过的路径添加至队列中。消减权重时使用
                    pathQueue.put(path_n)

                    # 然后是权重消减，表示当前车已经行驶玩这条路径，所以要释放这条路
                    # TODO: 设置合理的开始消减权重的条件，当前设置为第100辆车之后开始消减
                    # # 50 100 m1 failed  250 m1 succeed  350 succeed
                    # if i > 800 or startFlag:
                    #     startFlag = 1
                    #     if not pathQueue.empty():
                    #         # 从路径队列中取出路径，消减该路径在在权重中的影响
                    #         path_out = pathQueue.get()
                    #         adl_list_w = update_weight(adl_list_w, path_out, typeU=1)

        elif pathType == 1:  # 基于HP
            raise Exception("not finish")
            pass

        elif pathType == 2:  # 基于Dijkstra
            path_n = shortest_path(adl_list_w, st, ed)

            # 更新权重操作
            # 首先是权重累积
            if update_w:
                adl_list_w = update_weight(adl_list_w, path_n, typeU=0)
                # 将累加过的路径添加至队列中。消减权重时使用
                # pathQueue.put(path_n)

                # 然后是权重消减，表示当前车已经行驶玩这条路径，所以要释放这条路
                # TODO: 设置合理的开始消减权重的条件，当前设置为第100辆车之后开始消减
                # 50 100 m1 failed
                # if i > 800 or startFlag:
                #     startFlag = 1
                #     if not pathQueue.empty():
                #         # 从路径队列中取出路径，消减该路径在在权重中的影响
                #         path_out = pathQueue.get()
                #         adl_list_w = update_weight(adl_list_w, path_out, typeU=1)

        # m2 succeed
        # 重置权重
        # if i % interval == 0:
        #     adl_list_w = adl_list_w_bkp
        #
        #     i = 0
        #     startFlag = 0
        # log : 重置权重  weight_factor=0.1

        # 将规划得到的节点构成的路径转换为边构成的路径
        path_e = get_path_n2e(path_n, adl_list)

        paths[carID] = path_e

    return paths


def get_all_paths_with_hc_cw(adl_list, road_df, cardf, use_networkx=False):
    # 每规划一辆车的路径，所经过的路上权重增加weightAddValue
    # 达到interval时恢复原来的权重

    # 根据每辆车的计划出发时间进行升序排列 速度降序排列 id升序排列
    car_df_sort = cardf.sort_values(by=['planTime', 'speed', 'id'], axis=0, ascending=[True, False, True])

    carIDL = car_df_sort['id']
    startL = car_df_sort['from']
    endL = car_df_sort['to']
    carnum = carIDL.shape[0]

    adl_list_w = convert_adl2adl_w(adl_list)

    # 深拷贝
    tempdict = copy.deepcopy(adl_list_w)

    """
    #权重变化函数1
    # 单调递减
    #最优参数 weightAddValue = 0.01 shares = 9
    weightAddValue = 0.01
    shares = 9
    interval = int(carnum / shares)
    """

    # 权重变化函数2
    # 指数衰减
    # 最优参数 factor = 3  shares = 9
    factor = 3
    shares = 9
    interval = int(carnum / shares)

    paths_e = {}

    i = 1

    # 剪枝
    # 最优参数 cut_channel_level=2, cut_speed_level=2
    # 此参数可能会导致未使用hc 直接使用dikstra算法
    dp, sp, rp = cut_adjacency_list(adl_list, road_df, cut_channel_level=1, cut_speed_level=2)
    hp, hc = get_bestHCHP(dp)
    print(hc)
    # print(hp)

    # 基于get_path_with_hp()函数进行路径规划
    # 为所有车各规划一条最短路径
    # print("get_all_paths_with_hc_cw:")
    for carID, st, ed in zip(carIDL, startL, endL):
        try:
            #            path_n = get_path_with_hp(new_ad, adl_list, hp, st, ed)
            #            path_n = get_path_with_hp_simple(adl_list, hp, st, ed)
            path_n = get_path_with_hc_simple(tempdict, hc, st, ed)
        except:
            # print("hp", hp)
            # print("error:st, ed", st, ed)
            path_n = shortest_path(tempdict, st, ed)

            # path_n = replan_for_hc(hc, path_n)

        # 将规划得到的节点构成的路径转换为边构成的路径
        path_e = get_path_n2e(path_n, adl_list)

        paths_e[carID] = path_e

        # 更新权重
        if (i % interval) == 0:
            # 深拷贝
            tempdict = copy.deepcopy(adl_list_w)
        else:

            # 权重变化函数1
            # addvalue = max(weightAddValue * (interval-2*(i % interval))/interval, 0)
            # 权重变化函数2
            addvalue = np.exp(-factor * interval / (interval - (i % interval)))

            for k in range(len(path_n) - 1):
                cross_last = path_n[k]
                cross_next = path_n[k + 1]

                tempdict[cross_last][cross_next] += addvalue

        i += 1

    return paths_e


def getallpaths_dj_cw(adl_list, road_df, cardf, use_networkx=False):
    # 每规划一辆车的路径，所经过的路上权重增加addvalue
    # 达到interval时恢复原来的权重

    # 根据每辆车的计划出发时间进行升序排列 速度降序排列 id升序排列
    car_df_sort = cardf.sort_values(by=['planTime', 'speed', 'id'], axis=0, ascending=[True, False, True])
    # print(car_df_sort.head(10))

    carIDL = car_df_sort['id']
    startL = car_df_sort['from']
    endL = car_df_sort['to']
    carnum = carIDL.shape[0]

    adl_list_w = convert_adl2adl_w(adl_list)

    # 深拷贝
    tempdict = copy.deepcopy(adl_list_w)

    """
    #权重变化函数1
    # 单调递减
    #最优参数 weightAddValue = 0.01 shares = 9
    weightAddValue = 0.01
    shares = 9
    interval = int(carnum / shares)
    """

    # 权重变化函数2
    # 指数衰减
    # 最优参数 factor = 3  shares = 9
    factor = 3
    shares = 9
    interval = int(carnum / shares)

    paths_e = {}

    i = 1

    # 为所有车各规划一条最短路径
    for carID, st, ed in zip(carIDL, startL, endL):
        path_n = shortest_path(tempdict, st, ed)

        # 将规划得到的节点构成的路径转换为边构成的路径
        path_e = get_path_n2e(path_n, adl_list)

        paths_e[carID] = path_e

        # 更新权重
        if (i % interval) == 0:
            # 深拷贝
            tempdict = copy.deepcopy(adl_list_w)
        else:

            # 权重变化函数1
            # addvalue = max(weightAddValue * (interval-2*(i % interval))/interval, 0)
            # 权重变化函数2
            addvalue = np.exp(-factor * interval / (interval - (i % interval)))

            # print(addvalue)
            for k in range(len(path_n) - 1):
                cross_last = path_n[k]
                cross_next = path_n[k + 1]
                # print(tempdict[cross_last][cross_next])

                tempdict[cross_last][cross_next] += addvalue

                # print(tempdict[cross_last][cross_next])

        i += 1

    return paths_e


def getallpaths_dj_cw2(adl_list, road_df, cardf, use_networkx=False):
    # 每规划一辆车的路径，所经过的路上权重增加addvalue
    # 根据车速和道路速度的倒数来变权重
    # 达到interval时恢复原来的权重

    # 根据每辆车的计划出发时间进行升序排列 速度降序排列 id升序排列
    car_df_sort = cardf.sort_values(by=['planTime', 'speed', 'id'], axis=0, ascending=[True, False, True])
    # print(car_df_sort.head(10))

    carIDL = car_df_sort['id']
    startL = car_df_sort['from']
    endL = car_df_sort['to']
    carnum = carIDL.shape[0]

    adl_list_w = convert_adl2adl_w(adl_list)

    # 深拷贝
    tempdict = copy.deepcopy(adl_list_w)

    # 最优参数 9
    shares = 5
    interval = int(carnum / shares)

    paths_e = {}

    i = 1

    # 为所有车各规划一条最短路径
    for carID, st, ed in zip(carIDL, startL, endL):
        path_n = shortest_path(tempdict, st, ed)

        # 将规划得到的节点构成的路径转换为边构成的路径
        path_e = get_path_n2e(path_n, adl_list)

        paths_e[carID] = path_e

        # 更新权重
        if (i % interval) == 0:
            # 深拷贝
            tempdict = copy.deepcopy(adl_list_w)
        else:

            carspeed = cardf['speed'][carID]
            for k in range(len(path_n) - 1):
                cross_last = path_n[k]
                cross_next = path_n[k + 1]
                # print(tempdict[cross_last][cross_next])

                roadname = adl_list[cross_last][cross_next][0]
                # print(roadname)
                maxspeed = min(road_df['speed'][roadname], carspeed)

                addvalue = 1/(maxspeed*road_df['channel'][roadname])

                # addvalue = road_df['length'][roadname] / (maxspeed * road_df['channel'][roadname])

                tempdict[cross_last][cross_next] += addvalue

                # print(tempdict[cross_last][cross_next])

        i += 1

    return paths_e


def get_all_cars_paths_cw(adl_list, cardf, use_networkx=True):
    """
    brief: 获取所有车的一条最短路径
           每规划一辆车的路径，所经过的路上权重增加weightAddValue
           达到interval时恢复原来的权重
    :param adl_list: 带有边ID的邻接表
    :param carIDL: carID 列表
    :param startL: car 起始点列表
    :param endL: car 终点列表
    :param use_networkx:
    :return: paths: 数据格式:字典{carID： [edge path]}
    """
    # 根据每辆车的计划出发时间进行升序排列 速度降序排列
    car_df_sort = cardf.sort_values(by=['planTime', 'speed'], axis=0, ascending=[True, False])

    carIDL = car_df_sort['id']
    startL = car_df_sort['from']
    endL = car_df_sort['to']

    # 检查传入的参数是否合理
    if not len(carIDL) == len(startL) == len(endL):
        raise Exception("input size of  carIDL, startL, endL not equal")

    # 深拷贝
    tempdict = copy.deepcopy(adl_list)
    adl_list_w = convert_adl2adl_w(tempdict)

    weightAddValue = 0.01
    shares = 9

    size = carIDL.shape[0]
    interval = int(size / shares)

    i = 1

    global USE_NETWORKX
    paths = {}
    adl_list_w = convert_adl2adl_w(adl_list)

    if USE_NETWORKX and use_networkx:
        G = nx.DiGraph()
        for st in adl_list_w.keys():
            for to in adl_list_w[st].keys():
                G.add_edge(st, to, weight=(adl_list_w[st][to]))

        # 为所有车各规划一条最短路径
        for carID, st, ed in zip(carIDL, startL, endL):
            path_n = nx.algorithms.shortest_path(G, st, ed)
            # 将规划得到的节点构成的路径转换为边构成的路径
            path_e = get_path_n2e(path_n, adl_list)

            paths[carID] = path_e

    else:
        # 为所有车各规划一条最短路径
        print("get_all_cars_paths_cw:")
        for carID, st, ed in tqdm(zip(carIDL, startL, endL)):
            path_n = shortest_path(adl_list_w, st, ed)

            # 将规划得到的节点构成的路径转换为边构成的路径
            path_e = get_path_n2e(path_n, adl_list)

            paths[carID] = path_e

            # 更新权重
            if (i % interval) == 0:
                # 深拷贝
                tempdict = copy.deepcopy(adl_list)
                adl_list_w = convert_adl2adl_w(tempdict)
            else:
                for k in range(len(path_n) - 1):
                    cross_last = path_n[k]
                    cross_next = path_n[k + 1]

                    # 设置权重变化函数
                    # 单调递减
                    addvalue = max(weightAddValue * (interval - 2 * (i % interval)) / interval, 0)
                    # 指数衰减

                    tempdict[cross_last][cross_next][1] += addvalue

            i += 1

    return paths


def get_allcarspaths_floyd(adl_list, cardf):
    """
    brief: floyd获取所有车的一条最短路径
    :param adl_list: 带有边ID的邻接表
    :param carIDL: carID 列表
    :return: paths: 数据格式:字典{carID： [edge path]}
    """
    # 根据每辆车的计划出发时间进行升序排列 速度降序排列
    car_df_sort = cardf.sort_values(by=['planTime', 'speed'], axis=0, ascending=[True, False])

    carIDL = car_df_sort['id']
    startL = car_df_sort['from']
    endL = car_df_sort['to']

    # 检查传入的参数是否合理
    if not len(carIDL) == len(startL) ==len(endL):
        raise Exception("input size of  carIDL, startL, endL not equal")

    adl_list_w = convert_adl2adl_w(adl_list)
    Floydpath = init_Floyd(adl_list_w)

    paths = {}

    # 为所有车各规划一条最短路径
    # print("get_allcarspaths_floyd:")
    for carID, st, ed in tqdm(zip(carIDL, startL, endL)):
        path_n = get_floyd_path(Floydpath, st, ed)

        # 将规划得到的节点构成的路径转换为边构成的路径
        path_e = get_path_n2e(path_n, adl_list)

        paths[carID] = path_e

    return paths


def get_allcarspaths_floyd_cw(adl_list, cardf):
    """
    brief: floyd获取所有车的一条最短路径
    :param adl_list: 带有边ID的邻接表
    :param carIDL: carID 列表
    :return: paths: 数据格式:字典{carID： [edge path]}
    """
    # 根据每辆车的计划出发时间进行升序排列 速度降序排列
    car_df_sort = cardf.sort_values(by=['planTime', 'speed'], axis=0, ascending=[True, False])

    carIDL = car_df_sort['id']
    startL = car_df_sort['from']
    endL = car_df_sort['to']
    carnum = car_df_sort.shape[0]

    # 检查传入的参数是否合理
    if not len(carIDL) == len(startL) == len(endL):
        raise Exception("input size of  carIDL, startL, endL not equal")

    adl_list_w = convert_adl2adl_w(adl_list)

    # 深拷贝
    tempdict = copy.deepcopy(adl_list_w)

    """
    #权重变化函数1
    # 单调递减
    #最优参数 weightAddValue = 0.01 shares = 9
    weightAddValue = 0.01
    shares = 9
    interval = int(carnum / shares)
    """

    # 权重变化函数2
    # 指数衰减
    # 最优参数 factor = 3  shares = 9
    factor = 3
    shares = 1000
    interval = int(carnum / shares)

    Floydpath = init_Floyd(tempdict)

    paths = {}

    i = 1

    # 为所有车各规划一条最短路径
    for carID, st, ed in zip(carIDL, startL, endL):
        path_n = get_floyd_path(Floydpath, st, ed)

        # 将规划得到的节点构成的路径转换为边构成的路径
        path_e = get_path_n2e(path_n, adl_list)

        paths[carID] = path_e

        # 更新权重
        if (i % interval) == 0:
            Floydpath = init_Floyd(tempdict)
            # 深拷贝
            tempdict = copy.deepcopy(adl_list_w)
        else:

            # 权重变化函数1
            # addvalue = max(weightAddValue * (interval-2*(i % interval))/interval, 0)
            # 权重变化函数2
            addvalue = np.exp(-factor * interval / (interval - (i % interval)))

            for k in range(len(path_n) - 1):
                cross_last = path_n[k]
                cross_next = path_n[k + 1]

                tempdict[cross_last][cross_next] += addvalue

            # Floydpath = init_Floyd(tempdict)

        i += 1

    return paths


def get_path_with_hp(new_adl_, adl_, hp, start, end, use_networkx=False):
    """
    基于hamiltonian path进行路径规划
    :param adl_: 旧的邻接表，有边信息，格式{1: {9: [5007, 2.5], 2: [5000, 2.5]}, 2: {1: [5000, 2.5], 10: [5008, 2.0], 3: [5001, 4.5]},...}
    :param new_adl_: 重建后的邻接表
    :param hp:
    :param start:
    :param end:
    :param use_networkx:
    :return:
    """
    # TODO: 记得之后有时间的话添加路径不存在情况的异常判断和处理
    # 将带边信息的邻接表转化为不带便的邻接表
    adwE = convert_adl2adl_w(adl_)
    # path = []

    # 如果start和end都在hp中
    if (start in hp) and (end in hp):
        # print("start&end in hp")
        # path = hp[hp.index(start):hp.index(end)]
        # # path 为空需要倒序重新分割出路径
        # if len(path) == 0:
        #     hp_reverse = hp[::-1]
        #     path = hp_reverse[hp_reverse.index(start):hp_reverse.index(end)]
        # path.append(end)

        path = __get_value_in_list(hp, start, end)
        return path

    # start在hp,而end不在
    elif start in hp:
        # print("start in hp")
        # 将起始节点设为'HP'
        start_n = 'HP'

        # 得到部分路径
        path1 = get_path(new_adl_, start_n, end, use_networkx)
        # print('path1:', path1)

        # path1[0]='HP', path1[1]对应的节点和hp有邻接关系,由hp指向path1[1]
        connect_node = path1[1]

        # 如果start直接和connect node相连，可以直接返回
        if connect_node in adwE[start].keys():
            path1[0] = start
            # 得到路径
            path = path1

            return path

        # 寻找node在hp中, next node是conne_node的节点
        connect_node_in_hp = []
        for node, value in adwE.items():
            for next_node in value.keys():

                if (next_node == connect_node) and (node in hp):
                    connect_node_in_hp.append(node)

        # 从connect_node_in_hp中选取距离start最近的点
        if len(connect_node_in_hp) == 0:
            raise Exception("cannot find path with HP.")
        if len(connect_node_in_hp) == 1:
            middle_node = connect_node_in_hp[0]

            # path = hp[hp.index(start):hp.index(middle_node)]
            # # path 为空需要倒序重新分割出路径
            # if len(path) == 0:
            #     hp_reverse = hp[::-1]
            #     path = hp_reverse[hp_reverse.index(start):hp_reverse.index(middle_node)]
            # path.append(middle_node)

            path = __get_value_in_list(hp, start, middle_node)

            # final path
            path = path + path1[1:]
        else:
            init_l = 1000
            path_short = []
            for middle_node in connect_node_in_hp:
                path_t = __get_value_in_list(hp, start, middle_node)
                if len(path_t) < init_l:
                    init_l = len(path_t)
                    path_short = path_t
            # final path
            path = path_short + path1[1:]

        return path

############################################################ some error may occur
    elif end in hp:
        # print("end in hp")
        # 将起始节点设为'HP'
        end_n = 'HP'

        # 得到部分路径
        path1 = get_path(new_adl_, start, end_n)
        # print("path1:", path1)

        # path1[-1]='HP', path1[-2]对应的节点和hp有邻接关系,由hp指向path1[1]
        connect_node = path1[-2]

        # 如果start直接和connect node相连，可以直接返回
        if connect_node in adwE[end].keys():
            path1[-1] = end
            # 得到路径
            path = path1

            return path

        # 寻找node在conne_node, next node在hp中
        connect_node_in_hp = []
        for node, value in adwE.items():
            for next_node in value.keys():

                if (node == connect_node) and (next_node in hp):
                    connect_node_in_hp.append(next_node)

        # print("connect_node_in_hp:", connect_node_in_hp)

        # 从connect_node_in_hp中选取距离start最近的点
        if len(connect_node_in_hp) == 0:
            raise Exception("cannot find path with HP.")
        if len(connect_node_in_hp) == 1:
            middle_node = connect_node_in_hp[0]

            # path = hp[hp.index(start):hp.index(middle_node)]
            # # path 为空需要倒序重新分割出路径
            # if len(path) == 0:
            #     hp_reverse = hp[::-1]
            #     path = hp_reverse[hp_reverse.index(start):hp_reverse.index(middle_node)]
            # path.append(middle_node)

            path = __get_value_in_list(hp, middle_node, end)

            # final path
            path = path1[:-1] + path
        else:
            init_l = 1000
            path_short = []
            for middle_node in connect_node_in_hp:
                path_t = __get_value_in_list(hp, middle_node, end)
                if len(path_t) < init_l:
                    init_l = len(path_t)
                    path_short = path_t
            # final path
            path = path1[:-1] + path_short

        return path

    # start和end均不在hp中  # TODO: 可能出现start和end均不在hp中，且无法仅通过一次HP就能得到所有路径，也就是此处可能会报错get_path(new_adl_, start, end)无法找打路径
    else:
        path_t = get_path(new_adl_, start, end)

        # 根据路径中是否包含'HP'节点而分情况讨论
        # 如果路径中包含'HP'节点: 例如[1,2,5,7,'HP',12], 即1->2->5->7->'HP'->12
        if 'HP' in path_t:
            hp_index = path_t.index('HP')
            left_node = path_t[hp_index-1]
            right_node = path_t[hp_index+1]

            l_mid_node = []
            r_mid_node = []
            # 寻找所有满足条件的在hp中的中间节点
            for node, value in adwE.items():
                for next_node in value.keys():

                    if (node == left_node) and (next_node in hp):
                        l_mid_node.append(next_node)

                    if (node in hp) and (next_node == right_node):
                        r_mid_node.append(node)


            # TODO：根据权重选择
            # TODO:写不动了，随便选一个了
            if (len(l_mid_node) != 0) and (len(r_mid_node) != 0):
                path_mid = __get_value_in_list(hp, l_mid_node[0], r_mid_node[0])

                path = path_t[:hp_index] + path_mid + path_t[hp_index+1:]

                return path
        # 如果不包含，则直接返回
        else:
            return path_t


def get_all_paths_with_hp(adl_list, road_df, carIDL, startL, endL, use_networkx=False):

    paths = {}
    adl_list_w = convert_adl2adl_w(adl_list)

    # 剪枝
    dp, sp, rp = cut_adjacency_list(adl_list, road_df, cut_channel_level=1, cut_speed_level=1)

    # 搜索较优的hamiltonian path
    nodes = get_node_from_pairs(dp)
    graph = HamiltonianPath(len(nodes))
    graph.pairs = dp
    for _ in range(300):
        output = graph.isHamiltonianPathExist()
        if len(output[0]) >= 40:
            break
            # print('output[0]:', output[0])
            # try:
            #     # 重新构建邻接表
            #     new_ad = rebuild_adl_from_hp(adl_list, dp, sp, rp, hp)
            #
            #     # 基于get_path_with_hp()函数进行路径规划
            #     # 为所有车各规划一条最短路径
            #     for carID, st, ed in zip(carIDL, startL, endL):
            #         path_n = get_path_with_hp(new_ad, adl_list, hp, st, ed)
            #
            #         # 将规划得到的节点构成的路径转换为边构成的路径
            #         path_e = get_path_n2e(path_n, adl_list)
            #
            #         paths[carID] = path_e
            #
            #     break
            # except:
            #     print("run once more")


    hp = output[0]
    #
    # 重新构建邻接表
    new_ad = rebuild_adl_from_hp(adl_list, dp, sp, rp, hp)

    # 基于get_path_with_hp()函数进行路径规划
    # 为所有车各规划一条最短路径
    for carID, st, ed in zip(carIDL, startL, endL):
        try:
#            path_n = get_path_with_hp(new_ad, adl_list, hp, st, ed)
            path_n = get_path_with_hp_simple(adl_list, hp, st, ed)
        except:
            # print("hp", hp)
            # print("error:st, ed", st, ed)
            path_n = shortest_path(adl_list_w, st, ed)
            path_n = replan_for_hp(hp, path_n)

        # 将规划得到的节点构成的路径转换为边构成的路径
        path_e = get_path_n2e(path_n, adl_list)

        paths[carID] = path_e

    return paths


def replan_for_hp(hp, path_):
    """
    将规划出来的path_接入hp
    :param hp:
    :param path_:
    :return:
    """
    # print(hp, path_)
    for a in path_:
        if a in hp:
            lf = a
            lf_index = path_.index(a)
            break
        else:
            lf_index = 0

    for b in path_[::-1]:
        if b in hp:
            rt = b
            rt_index = path_.index(b)
            break
        else: 
            rt_index = 0

    # print(lf_index,rt_index,lf,rt)
    if lf_index < rt_index:
        path_ = path_[:lf_index] + __get_value_in_list(hp, lf, rt) + path_[rt_index+1:]

    return path_


def get_path(adl_list_w, start, end, use_networkx=False):
    """
    brief: 给定起点和终点，从邻接表中搜索得到一条可行路径，满足最优条件
    :param adl_list_w: 不带边ID的邻接表
    :param start:
    :param end:
    :param use_networkx: 默认根据networkx库导入情况决定使用那种方法获取路径
    :return:
    """
    global USE_NETWORKX
    if USE_NETWORKX and use_networkx:
        G = nx.DiGraph()
        for st in adl_list_w.keys():
            for to in adl_list_w[st].keys():
                G.add_edge(st, to, weight=(adl_list_w[st][to]))

        path = nx.algorithms.shortest_path(G, start, end)
    else:
        path = shortest_path(adl_list_w, start, end)

    return path


def get_all_cars_paths(adl_list, carIDL, startL, endL, use_networkx=True):
    """
    brief: 获取所有车的一条最短路径
    :param adl_list: 带有边ID的邻接表
    :param carIDL: carID 列表
    :param startL: car 起始点列表
    :param endL: car 终点列表
    :param use_networkx:
    :return: paths: 数据格式:字典{carID： [edge path]}
    """
    # 检查传入的参数是否合理
    if not len(carIDL) == len(startL) ==len(endL):
        raise Exception("input size of  carIDL, startL, endL not equal")

    global USE_NETWORKX
    paths = {}
    adl_list_w = convert_adl2adl_w(adl_list)

    if USE_NETWORKX and use_networkx:
        G = nx.DiGraph()
        for st in adl_list_w.keys():
            for to in adl_list_w[st].keys():
                G.add_edge(st, to, weight=(adl_list_w[st][to]))

        # 为所有车各规划一条最短路径
        for carID, st, ed in zip(carIDL, startL, endL):
            path_n = nx.algorithms.shortest_path(G, st, ed)
            # 将规划得到的节点构成的路径转换为边构成的路径
            path_e = get_path_n2e(path_n, adl_list)

            paths[carID] = path_e

    else:
        # 为所有车各规划一条最短路径
        for carID, st, ed in zip(carIDL, startL, endL):
            path_n = shortest_path(adl_list_w, st, ed)

            # 将规划得到的节点构成的路径转换为边构成的路径
            path_e = get_path_n2e(path_n, adl_list)

            paths[carID] = path_e

    return paths


def get_path_dijkstra(adl_list_w, start, end):
    path = shortest_path(adl_list_w, start, end)
    return path


def get_time_plan(time_plan_func, car_df, ):
    """
    brief:规划每辆车的出发时刻
    :param car_df: car dataframe
    :return: 每辆车的出发时刻 time_plan: 数据格式:字典{carID： [carID, start time]}
    """
    pass


def get_time_plan0(car_df):
    """
    不更改出发时间
    :param car_df:
    :return:
    """
    time_plans = {}

    for carID, pT in zip(car_df['id'], car_df['planTime']):

        time_plans[carID] = [carID, pT]

    return time_plans



def get_time_plan1(car_df):
    """
    brief:简单粗暴的时间安排1
    :param car_df:
    :return:
    """
    time_plans = {}

    # 根据每辆车的计划出发时间进行升序排列
    car_df_sort = car_df.sort_values(by='planTime', axis=0, ascending=True)
    car_len = len(car_df_sort['id'])

    # some parameters
    # before:(0.3,50)->20406  (0.35,30)->20550 (0.3,35)->20476 (0.3,55)->20382
    split_factor = 0.3
    max_delay_time = 55

    i = 1
    for carID, pT in zip(car_df_sort['id'], car_df_sort['planTime']):
        pT += i
        i += 1
        if i/car_len < split_factor:
            pT = pT + int(i/(split_factor*car_len) * max_delay_time)
            time_plans[carID] = [carID, pT]

        if (i/car_len >= split_factor) and (i/car_len <= (1-split_factor)):
            pT = pT + max_delay_time
            time_plans[carID] = [carID, pT]
        if i/car_len > (1-split_factor):
            pT = pT + int(max_delay_time - i / (split_factor * car_len) * max_delay_time)
            time_plans[carID] = [carID, pT]

    return time_plans


def get_time_plan3(car_df):
    """
    brief:简单粗暴的时间安排1
    :param car_df:
    :return:
    """
    time_plans = {}

    # 根据每辆车的计划出发时间进行升序排列
    car_df_sort = car_df.sort_values(by='planTime', axis=0, ascending=True)
    car_len = len(car_df_sort['id'])

    # some parameters
    # before:(0.3,50)->20406  (0.35,30)->20550 (0.3,35)->20476 (0.3,55)->20382
    split_factor = 0.3
    max_delay_time = 5

    i = 1
    for carID, pT in zip(car_df_sort['id'], car_df_sort['planTime']):
        pT += i
        i += 1
        if i/car_len < split_factor:
            pT = pT + int(i/(split_factor*car_len) * max_delay_time)
            time_plans[carID] = [carID, pT]

        if (i/car_len >= split_factor) and (i/car_len <= (1-split_factor)):
            pT = pT + max_delay_time
            time_plans[carID] = [carID, pT]
        if i/car_len > (1-split_factor):
            pT = pT + int(max_delay_time - i / (split_factor * car_len) * max_delay_time)
            time_plans[carID] = [carID, pT]

    return time_plans


def get_time_plan2(car_df):
    """
    brief: 简单粗暴的时间安排2,相当于一辆一辆跑
    成绩： 2024130
    :param car_df:
    :return:
    """
    time_plans = {}

    # 根据每辆车的计划出发时间进行升序排列
    car_df_sort = car_df.sort_values(by='planTime', axis=0, ascending=True)

    i = 1
    for carID, pT in zip(car_df_sort['id'], car_df_sort['planTime']):
        i += 1
        pT += i*100

        time_plans[carID] = [carID, pT]

    return time_plans


def get_answer(car_list, path_plan, time_plan):
    """
    brief: 将每辆车规划的路径和出发时刻组合成answer格式
    :param car_list: 数据格式： pandas series
    :param path_plan: 数据格式:字典{carID： [edge path]}
    :param time_plan: 数据格式:字典{carID： [carID, start time]}
    :return: answer: 数据格式: [[carID, startTime, pathList...], ..., [carID, startTime, pathList...], ]
    """
    answer = []
    for carID in car_list:
        answer.append(time_plan[carID] + path_plan[carID])

    return answer
