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



import numpy as np
import  pandas
import copy
import matplotlib.pyplot as plt
from dijkstra.dijkstra import shortest_path


try:
    global USE_NETWORKX
    # if USE_NETWORKX = True, use networkx lib to get shortest path as default; if import failed, then use dijkstra lib
    # if USE_NETWORKX = True, use dijkstra lib to get shortest path
    USE_NETWORKX = True
    import networkx as nx
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
                if next_cross_id == cross_id:
                    next_cross_id = road_df['from'][road]
                # 设置该条边的权重
                weight = weight_func(road_df['length'][road], road_df['speed'][road])

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
                if next_cross_id == cross_id:
                    next_cross_id = road_df['from'][road]
                # 设置该条边的权重
                weight = weight_func(road_df['length'][road], road_df['speed'][road])

                # 将数据存入嵌套字典
                if ad_list_without_edge_id.__contains__(cross_id):
                    ad_list_without_edge_id[cross_id][next_cross_id] = weight
                else:
                    ad_list_without_edge_id[cross_id] = {next_cross_id: weight}

    return ad_list_without_edge_id


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
    return


# TODO: 权重函数还没有进行科学设置
def weight_func(road_l, road_mv):
    weight = road_l / road_mv
    return weight


def get_path(adl_list_w, start, end, use_networkx=True):
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
    split_factor = 0.3
    max_delay_time = 50

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
    brief: 简单粗暴的时间安排2
    :param car_df:
    :return:
    """
    time_plans = {}

    # 根据每辆车的计划出发时间进行升序排列
    car_df_sort = car_df.sort_values(by='planTime', axis=0, ascending=True)

    i = 1
    for carID, pT in zip(car_df_sort['id'], car_df_sort['planTime']):
        i += 1
        pT += i

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


if __name__ == "__main__":
    al = {1: {2: [5000, 2.0], 7: [5005, 2.0]}, 2: {8: [5006, 2.0], 1: [5000, 2.0], 3: [5001, 2.0]}, 3: {9: [5007, 2.0], 2: [5001, 2.0], 4: [5002, 2.0]}, 4: {10: [5008, 2.0], 3: [5002, 2.0], 5: [5003, 2.0]}, 5: {11: [5009, 2.0], 4: [5003, 2.0], 6: [5004, 2.0]}, 6: {12: [5010, 2.0], 5: [5004, 2.0]}, 7: {8: [5011, 2.0], 1: [5005, 2.0], 13: [5016, 2.0]}, 8: {9: [5012, 2.0], 2: [5006, 2.0], 14: [5017, 2.0], 7: [5011, 2.0]}, 9: {8: [5012, 2.0], 10: [5013, 2.0], 3: [5007, 2.0], 15: [5018, 2.0]}, 10: {16: [5019, 2.0], 9: [5013, 2.0], 11: [5014, 2.0], 4: [5008, 2.0]}, 11: {17: [5020, 2.0], 10: [5014, 2.0], 12: [5015, 2.0], 5: [5009, 2.0]}, 12: {18: [5021, 2.0], 11: [5015, 2.0], 6: [5010, 2.0]}, 13: {19: [5027, 2.0], 14: [5022, 2.0], 7: [5016, 2.0]}, 14: {8: [5017, 2.0], 20: [5028, 2.0], 13: [5022, 2.0], 15: [5023, 2.0]}, 15: {16: [5024, 2.0], 9: [5018, 2.0], 21: [5029, 2.0], 14: [5023, 2.0]}, 16: {17: [5025, 2.0], 10: [5019, 2.0], 22: [5030, 2.0], 15: [5024, 2.0]}, 17: {16: [5025, 2.0], 18: [5026, 2.0], 11: [5020, 2.0], 23: [5031, 2.0]}, 18: {24: [5032, 2.0], 17: [5026, 2.0], 12: [5021, 2.0]}, 19: {25: [5038, 2.0], 20: [5033, 2.0], 13: [5027, 2.0]}, 20: {26: [5039, 2.0], 19: [5033, 2.0], 21: [5034, 2.0], 14: [5028, 2.0]}, 21: {27: [5040, 2.0], 20: [5034, 2.0], 22: [5035, 2.0], 15: [5029, 2.0]}, 22: {16: [5030, 2.0], 28: [5041, 2.0], 21: [5035, 2.0], 23: [5036, 2.0]}, 23: {24: [5037, 2.0], 17: [5031, 2.0], 29: [5042, 2.0], 22: [5036, 2.0]}, 24: {18: [5032, 2.0], 30: [5043, 2.0], 23: [5037, 2.0]}, 25: {26: [5044, 2.0], 19: [5038, 2.0], 31: [5049, 2.0]}, 26: {32: [5050, 2.0], 25: [5044, 2.0], 27: [5045, 2.0], 20: [5039, 2.0]}, 27: {33: [5051, 2.0], 26: [5045, 2.0], 28: [5046, 2.0], 21: [5040, 2.0]}, 28: {34: [5052, 2.0], 27: [5046, 2.0], 29: [5047, 2.0], 22: [5041, 2.0]}, 29: {35: [5053, 2.0], 28: [5047, 2.0], 30: [5048, 2.0], 23: [5042, 2.0]}, 30: {24: [5043, 2.0], 36: [5054, 2.0], 29: [5048, 2.0]}, 31: {32: [5055, 2.0], 25: [5049, 2.0]}, 32: {33: [5056, 2.0], 26: [5050, 2.0], 31: [5055, 2.0]}, 33: {32: [5056, 2.0], 34: [5057, 2.0], 27: [5051, 2.0]}, 34: {33: [5057, 2.0], 35: [5058, 2.0], 28: [5052, 2.0]}, 35: {34: [5058, 2.0], 36: [5059, 2.0], 29: [5053, 2.0]}, 36: {35: [5059, 2.0], 30: [5054, 2.0]}}
    pn = [1, 7, 13, 19, 20]
    pe = get_path_n2e(pn, al)
    print(pe)

    # get_answer(car_list, path_plan, time_plan) test
    cl = [100, 101]
    pp = {100: [203, 303], 101: [213, 303, 304, 432]}  # path
    tp = {100: [100, 1], 101: [101, 3]}  # time
    an = get_answer(cl, pp, tp)
    print(an)

