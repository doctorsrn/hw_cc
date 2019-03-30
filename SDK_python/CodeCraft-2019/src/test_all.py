import pandas
import sys
import time
import os
# import numpy as np

from util import *
from util1 import *
from IOModule import *
from hp_finder import HamiltonianPath
from concurrent.futures import ProcessPoolExecutor


def main():

    rpath = '../config0'
    path = rpath + '/cross.txt'
    path1 = rpath + '/road.txt'
    path2 = rpath + '/car.txt'
    path3 = rpath + '/answer.txt'
    answer_path = rpath + '/answer.txt'

    df = read_from_txt(path)
    # print(df.head())
    # print(df.shape)

    df1 = read_from_txt(path1)
    # print(df1.head())
    # print(df1.shape)

    df2 = read_from_txt(path2)
    # print(df2.head())
    # print(df2.shape)

    car_df = df2
    road_df = df1
    cross_df = df

    al = build_adjacency_list(df, df1)
    # print("al:", al)
    #
    # print("adwE:", convert_adl2adl_w(al))
    #
    # adw = build_ad_list_without_edge_id(df, df1)
    # print("adwE:", adw)

    # adj_list_visualize(al)
    # exit(0)

    # final test

    start_time = time.clock()
    time_plans, car_df_actual = get_time_plan5(car_df)
    t1 = time.clock()

    paths = get_all_paths_with_weight_update(al, road_df, car_df_actual, cross_df, pathType=2, update_w=True)
    t2 = time.clock()

    time_plans, paths = super_time_plan(paths, car_df_actual, road_df, cross_df, al)
    t22 = time.clock()

    answers = get_answer(car_df['id'], paths, time_plans)
    t3 = time.clock()

    write_answer2file(answer_path, answers)
    t4 = time.clock()

    print('CPU cost time for get time plan:', t1 - start_time)
    print('CPU cost time for path plan: ', t2 - t1)
    print('CPU cost time for path replan: ', t22 - t2)
    print('CPU cost time for get answer: ', t3 - t22)
    print('CPU cost time for write answer: ', t4 - t3)
    print('CPU cost time for all: ', t4 - start_time)

    sys.exit(0)


    # test cut_adjacency_list
    # dp, sp, rp: duplex connect pairs,single connect pairs, rest pairs
    dp, sp, rp = cut_adjacency_list(al, road_df, cut_speed_level=1, cut_channel_level=1)
    print("dp", dp)
    print("sp", sp)
    print("rp", rp)

    # #################
    #     network = public_transport.TransportNetwork.load_from_adjacency_list(adw)
    #     start_stop = public_transport.Stop('1')
    #     end_stop = public_transport.Stop('9')
    #     min_travel_time, shortest_connection = network.find_shortest_connection(start_stop, end_stop)
    #
    #     print(min_travel_time, shortest_connection)
    #     exit(1)
    # #################

    print("adwW:", build_ad_list_without_weight(df, df1, str_pattern=True))

    # hp_finder.py test
    nodes = get_node_from_pairs(dp)
    print('len of nodes and pairs:', len(nodes), len(dp))
    nodes.sort()
    print(nodes)


    
    ########### get HC test
#    graph = HamiltonianPath(len(nodes))
#    graph.pairs = dp
#    for i  in range(2000):
#        output = graph.isHamiltonianPathExist()
#        # # find long HP
#        # if len(output[0]) >=40:
#        #     print('Hamiltonian Paths:', len(output[0]))
#        #     print('output[0]:', output[0])
#        #     break
##        print('output[0]:', output[0])
#        # find long HC
#        print(i)
#        if len(output[0]) >= 40:
#            print('output[0]:', output[0])
#            n = 3
#            for st in output[0][:n]:
#                for ed in output[0][-n:]:
#                    # st = output[0][0]
#                    # ed = output[0][-1]
#                    if ([st, ed] in dp) or ([ed, st] in dp):
#                        print('st, ed:', st, ed)
#                        print('Hamiltonian Cycle:', len(output[0]))
#                        print('output[0]:', output[0])
    
    start = 50
    end = 8
    
    output = get_bestHCHP(dp)
    hc = output[1]
    # print('best hp:', output[0])
    print('\nbest hc:', output[1])
    print('\nbest hc straight num:', get_straight_num(hc, al, cross_df))
    
    ###基于HC的路径规划测试
    p = get_path_with_hc_simple(adw, hc, start, end)
    print('hc path:', p)


    ## get_bestHCHP_with_direction
    output = get_bestHCHP_with_direction(dp, al, cross_df, searchNum=500)
    hc = output[1]

    print('\nbest hc with direction:', output[1])
    print('best hc straight num:', get_straight_num(hc, al, cross_df))

    ###基于HC的路径规划测试
    p = get_path_with_hc_simple(adw, hc, start, end)
    print('hc path:', p)
#    sys.exit(0)

        # TODO: if output[0][0] == output[0][-1]:   可以寻找 hamiltonian cycle

    # test remove_hp_from_dp()
    # print('remove_hp_from_dp:', remove_hp_from_dp(dp, output[0]))

    # test rebuild_adl_from_hp(adl_, dp_, sp_, rp_, hp)
    # hp = output[0]
    # hp = [1, 9, 10, 2, 3, 11, 19, 27, 26, 34, 35, 43, 44, 36, 28, 20, 12, 4, 5, 13, 14, 15, 7, 8, 16, 24, 32, 31, 39, 40, 48, 56, 55, 63, 64]
    hp = [1, 2, 3, 11, 10, 9, 17, 25, 26, 27, 19, 20, 21, 22, 30, 29, 37, 38, 39, 31, 32, 40, 48, 47, 46, 54, 62, 61, 53, 45, 44, 43, 42, 34, 33, 41, 49, 50, 58, 57]
    # hp = [53, 61, 62, 54, 55, 56, 48, 40, 39, 31, 32, 24, 16, 8, 7, 15, 14, 13, 5, 4, 12, 20, 21, 22, 30, 29, 28, 36, 37, 45, 44, 43, 35, 34, 33, 41, 42, 50, 58, 59, 60, 52]
    new_ad = rebuild_adl_from_hp(al, dp, sp, rp, hp)
    print('new_ad:', new_ad)
    print('new_ad[HP]:', new_ad['HP'])

    # test get_path_with_hp(new_adl_, adl_, hp, start, end, use_networkx=False)#
    # 测试了三种情况下的工作情况，一切正常

    print('\nget_path:', get_path(adw, start, end, use_networkx=False))
    p = get_path(adw, start, end, use_networkx=False)
    rp = replan_for_hp(hp, p)
    print('\nreplan(hp, p):', rp)

#TODO: 下面这条命令在windows下不会报错，但是在ubunut 下就会报错
    # print('\nget_path_with_hp:', get_path_with_hp(new_ad, al, hp, start, end , use_networkx=False))
    p = get_path_with_hp_simple(al, hp, start, end)
    print('get_path_with_hp_simple:', p)
    # p = get_path_with_hp(new_ad, al, hp, 58, 8, use_networkx=False)
    # print(p)

    # exit(0)
#    sys.exit(0)

#################终极测试
    start_time = time.clock()

    # test function: get_all_cars_paths(adl_list, carIDL, startL, endL, use_networkx=True)
    pa = get_all_paths_with_hc(al, road_df, car_df['id'], car_df['from'], car_df['to'])
    
    # test get_all_paths_with_weight_update(adl_list, road_df, car_df, pathType=0, use_networkx=False):
    # pa = get_all_paths_with_weight_update(al, road_df, car_df, cross_df)
    ct, at = get_benchmark(pa, car_df, road_df, cross_df)
    print("benchmark hc: all time cost:", at)
    
    end_time = time.clock()
    # print('all cars paths：', pa)
    print(len(pa))
    print('CPU cost time for path plan: ', end_time - start_time)
    # print(pa)
    # sys.exit(0)
    #####

    # adj_list_visualize(new_ad)

    # 基于hp的路径规划
    # p = get_path(new_ad, 6, 33, use_networkx=False)
    # print('shortest path is:', p)
#    exit()
#    sys.exit()

    # # hamiltonian path test
    # get_hamiltonian_path(adw, 1, 20)

    # # 可视化有向图
    # adj_list_visualize(al)
    # exit(1)

    # 最短路径搜索
    # adw['HP'] = {9: 2.5, 1: 2.5}
#     p = get_path(adw, 1, 20, use_networkx=False)
#     print('shortest path is:', p)
#
#
#     # 最短路径搜索
#     p1 = shortest_path(adw, 1, 20)
#     print(p1)
#
#     start_time = time.clock()
#
#     # test function: get_all_cars_paths(adl_list, carIDL, startL, endL, use_networkx=True)
    pa = get_all_cars_paths(al, df2['id'], df2['from'], df2['to'], use_networkx=False)
    ct, at = get_benchmark(pa, car_df, road_df, cross_df)
    print("benchmark dijkstra: all time cost:", at)
#
#
#
#     end_time = time.clock()
#     # print('all cars paths：', pa)
#     print(len(pa))
#     print('CPU cost time for path plan: ', end_time - start_time)

    sys.exit()

    ###############################################
    # # 读数据
    # readdata(path2, carmap)
    # readdata(path1, roadmap)
    # readdata(path, crossmap)
    # crossidtransfer(crossmap, crossidmap)
    # car_size = len(carmap)
    # cross_size = len(crossmap)
    # road_size = len(roadmap)
    #
    # # 路网定义
    # createnvir(cross_size)

    #############################################################
    # time cost result:  unit:second
    # config_5: car number:512, networkx:0.01287 , 3rdparty: 0.102
    # config_9: car number:2048, networkx:0.06 , 3rdparty: 0.4143
    # config_10: car number:2048, networkx:0.06 , 3rdparty: 0.396

    # test get_time_plan
    start_time = time.clock()
    pt = get_time_plan2(df2)
    print('CPU cost time for time plan: ', time.clock() - start_time)
    # print(pt)

    answer = get_answer(df2['id'], pa, pt)
    # print(answer)

    # write_answer2file(path3, answer)

    # # 求调度时间
    # value = CalScheduleTime(path3, crossmap, crossidmap, roadmap, carmap, cross_size, road_size, car_size,
    #                         roadmat)  # 参数：answer.txt路径、路口字典、道路字典、车辆字典、路口数目、道路数目、车辆数目、路网
    # print(value)


if __name__ == '__main__':
    main()
   
#    ############### process test
#    p = ProcessPoolExecutor()
#    obj_l = []
#    for i in range(4):
#        obj = p.submit(get_bestHCHP, 60, 100)
#        obj_l.append(obj)
#    loop_time_elapsed = (time.clock() - loop_start_time)
#    print([len(obj.result()) for obj in obj_l])
##    a = get_bestHCHP(60, 400)
##    print(len(a))
#    # p.shutdown()  # 等同于p.close(),p.join()
#    
#    # print("Accuracy:", yes,"%")
#    print("Time taken for 100 runs:", loop_time_elapsed)