import pandas
# import numpy as np
# from util import build_adjacency_list, adj_list_visualize, get_path, build_ad_list_without_edge_id
from util import *
# from dijkstra.dijkstra import shortest_path

# from move_zp import *
from hp import *

import public_transport
import simulated_annealing

import time


def read_from_txt(path_, type_= None):
    """
    :param path_: txt file path
           type_: not use
    :return: pandas DataFrame
    """
    # read txt file, splice number
    df = pandas.read_csv(path_, sep='[^\\-|0-9]+', header=None, skiprows=1, engine='python')  # 正则表达式记得转义

    # delete NaN columns--> first column and last column
    df.drop(columns=[0, df.shape[1]-1], inplace=True)

    if path_.find('road') > 0: # road(id,length,speed,channel,from,to,isDuplex)
        df.set_axis(['id', 'length', 'speed', 'channel', 'from', 'to', 'isDuplex'], axis='columns', inplace=True)
        df.set_index(df['id'], inplace=True)
    elif path_.find('car') > 0: # car(id,from,to,speed,planTime)
        df.set_axis(['id',  'from', 'to', 'speed', 'planTime'], axis='columns', inplace=True)
        df.set_index(df['id'], inplace=True)
    elif path_.find('cross') > 0: # cross(id,roadId,roadId,roadId,roadId)
        df.set_axis(['id', 'roadID1', 'roadID2', 'roadID3', 'roadID4'], axis='columns', inplace=True)
        df.set_index(df['id'], inplace=True)
    else:
        raise Exception("input txt file error")

    return df


def read_car_from_txt(path_):
    df = pandas.read_csv(path_, sep='[^\\-|0-9]+', header=None, skiprows=1, engine='python')

    # delete NaN columns--> first column and last column
    df.drop(columns=[0, df.shape[1] - 1], inplace=True)

    df.set_axis(['id', 'from', 'to', 'speed', 'planTime'], axis='columns', inplace=True)
    df.set_index(df['id'], inplace=True)

    return df


def read_road_from_txt(path_):
    df = pandas.read_csv(path_, sep='[^\\-|0-9]+', header=None, skiprows=1, engine='python')

    # delete NaN columns--> first column and last column
    df.drop(columns=[0, df.shape[1] - 1], inplace=True)

    df.set_axis(['id', 'length', 'speed', 'channel', 'from', 'to', 'isDuplex'], axis='columns', inplace=True)
    df.set_index(df['id'], inplace=True)

    return df


def read_cross_from_txt(path_):
    df = pandas.read_csv(path_, sep='[^\\-|0-9]+', header=None, skiprows=1, engine='python')

    # delete NaN columns--> first column and last column
    df.drop(columns=[0, df.shape[1] - 1], inplace=True)

    df.set_axis(['id', 'roadID1', 'roadID2', 'roadID3', 'roadID4'], axis='columns', inplace=True)
    df.set_index(df['id'], inplace=True)

    return df


def write_answer2file(txt_path, answer_list):
    """
    :brief: write data to answer.txt, data pattern {carID, startTime, path series}
    :param txt_path: 要写入文件的路径
    :param answer_list: answer 2维数组，数据格式例如:[[100, 1, 203, 303], [101, 3, 213, 303, 304, 432]]
    :return:
    """
    with open(txt_path, 'w') as output:
        output.write('#carID, StartTime, RoadID...\n')
        for answer in answer_list:
            answer_str = "".join([str(x)+',' for x in answer])  # 将int list型的answer转换为str类型，并以逗号隔开
            output.writelines('(' + answer_str[:-1] + ')' + '\n')  # answer_str[:-1] 最后的逗号不写入


if __name__ == "__main__":
    rpath = '/home/srn/SRn/Competition/HuaWei/hw_cc/SDK_python/CodeCraft-2019/config0'
    path = rpath + '/cross.txt'
    path1 = rpath + '/road.txt'
    path2 = rpath + '/car.txt'
    path3 = rpath + '/answer.txt'

    df = read_from_txt(path)
    print(df.head())
    print(df.shape)

    df1 = read_from_txt(path1)
    print(df1.head())
    print(df1.shape)

    df2 = read_from_txt(path2)
    print(df2.head())
    print(df2.shape)
#
#     car_df = df2
#     road_df = df1
#     cross_df = df
#
#     al = build_adjacency_list(df, df1)
#     print("al:", al)
#
#     print("adwE:", convert_adl2adl_w(al))
#
#     adw = build_ad_list_without_edge_id(df, df1)
#     print("adwE:", adw)
#
#     # test cut_adjacency_list
#     # dp, sp, rp: duplex connect pairs,single connect pairs, rest pairs
#     dp, sp, rp = cut_adjacency_list(al, road_df, cut_speed_level=1, cut_channel_level=1)
#     print("dp", dp)
#     print("sp", sp)
#     print("rp", rp)
#
# # #################
# #     network = public_transport.TransportNetwork.load_from_adjacency_list(adw)
# #     start_stop = public_transport.Stop('1')
# #     end_stop = public_transport.Stop('9')
# #     min_travel_time, shortest_connection = network.find_shortest_connection(start_stop, end_stop)
# #
# #     print(min_travel_time, shortest_connection)
# #     exit(1)
# # #################
#
#     print("adwW:", build_ad_list_without_weight(df, df1, str_pattern=True))
#
#     # hp.py test
#     gr, nl = get_graph(road_df)
#     gr_test = [[str(x[0]), str(x[1])] for x in dp]
#
#     print("graph:", gr)
#     print("node list:", nl)
#     print("node list length:", len(nl))
#     greedy(gr_test, nl)
#     exhaustive(gr_test, nl)
#
#
#     # # hamiltonian path test
#     # get_hamiltonian_path(adw, 1, 20)
#
#     # # 可视化有向图
#     adj_list_visualize(al)
#     exit(1)
#
#     # 最短路径搜索
#     p = get_path(adw, 1, 20)
#     print('shortest path is:', p)
#
#     # 最短路径搜索
#     p1 = shortest_path(adw, 1, 20)
#     print(p1)
#
#     start_time = time.clock()
#
#     # test function: get_all_cars_paths(adl_list, carIDL, startL, endL, use_networkx=True)
#     pa = get_all_cars_paths(al, df2['id'], df2['from'], df2['to'], use_networkx=False)
#     print()
#
#     end_time = time.clock()
#     # print('all cars paths：', pa)
#     print(len(pa))
#     print('CPU cost time for path plan: ', end_time-start_time)
#
#     ###############################################
#     # # 读数据
#     # readdata(path2, carmap)
#     # readdata(path1, roadmap)
#     # readdata(path, crossmap)
#     # crossidtransfer(crossmap, crossidmap)
#     # car_size = len(carmap)
#     # cross_size = len(crossmap)
#     # road_size = len(roadmap)
#     #
#     # # 路网定义
#     # createnvir(cross_size)
#
#     #############################################################
#     # time cost result:  unit:second
#     # config_5: car number:512, networkx:0.01287 , 3rdparty: 0.102
#     # config_9: car number:2048, networkx:0.06 , 3rdparty: 0.4143
#     # config_10: car number:2048, networkx:0.06 , 3rdparty: 0.396
#
#     # test get_time_plan
#     start_time = time.clock()
#     pt = get_time_plan2(df2)
#     print('CPU cost time for time plan: ', time.clock() - start_time)
#     # print(pt)
#
#     answer = get_answer(df2['id'], pa, pt)
#     # print(answer)
#
#     # write_answer2file(path3, answer)
#
#     # # 求调度时间
#     # value = CalScheduleTime(path3, crossmap, crossidmap, roadmap, carmap, cross_size, road_size, car_size,
#     #                         roadmat)  # 参数：answer.txt路径、路口字典、道路字典、车辆字典、路口数目、道路数目、车辆数目、路网
#     # print(value)


