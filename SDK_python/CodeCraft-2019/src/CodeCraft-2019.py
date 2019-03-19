import logging
import sys
# import numpy as np
# from util import build_adjacency_list, adj_list_visualize, get_path, build_ad_list_without_edge_id
from util import *
from IOModule import *
import os

# from move_zp import *


# logging.basicConfig(level=logging.DEBUG,
#                     filename='../logs/CodeCraft-2019.log',
#                     format='[%(asctime)s] %(levelname)s [%(funcName)s: %(filename)s, %(lineno)d] %(message)s',
#                     datefmt='%Y-%m-%d %H:%M:%S',
#                     filemode='a')


def main():
    # print("hello")

    if len(sys.argv) != 5:
        # logging.info('please input args: car_path, road_path, cross_path, answerPath')
        exit(1)

    car_path = sys.argv[1]
    road_path = sys.argv[2]
    cross_path = sys.argv[3]
    answer_path = sys.argv[4]
    
    # rpath = '/home/srn/SRn/Competition/HuaWei/hw_cc/SDK_python/CodeCraft-2019/config0'
    # cross_path = rpath + '/cross.txt'
    # road_path = rpath + '/road.txt'
    # car_path = rpath + '/car.txt'
    # answer_path = rpath + '/answer.txt'


    #
    # logging.info("car_path is %s" % (car_path))
    # logging.info("road_path is %s" % (road_path))
    # logging.info("cross_path is %s" % (cross_path))
    # logging.info("answer_path is %s" % (answer_path))

    # to read input file
    # car_df = read_from_txt(car_path)
    # road_df = read_from_txt(road_path)
    # cross_df = read_from_txt(cross_path)
    car_df = read_car_from_txt(car_path)
    # print(car_df.head())
    road_df = read_road_from_txt(road_path)
    cross_df = read_cross_from_txt(cross_path)

    # process

    # build adjacency list
    ad_l = build_adjacency_list(cross_df, road_df)

    # get path plans
    # paths = get_all_cars_paths(ad_l, car_df['id'], car_df['from'], car_df['to'], use_networkx=False)

    paths = get_all_paths_with_hc(ad_l, road_df, car_df['id'], car_df['from'], car_df['to'])

    # ##############
    # # debug
    #
    # adl_w = build_ad_list_without_edge_id(cross_df, road_df)
    # p = get_path(adl_w, 6, 50, use_networkx=False)
    # pe = get_path_n2e(p, ad_l)
    # print('p',p)
    # print('pe', pe)
    # print(ad_l)
    # adj_list_visualize(ad_l)
    # # os.system('pause')
    # #
    # ###############

    # get time plans
    time_plans = get_time_plan0(car_df)

    # get answer
    answers = get_answer(car_df['id'], paths, time_plans)

    # to write output file
    write_answer2file(answer_path, answers)

    # print("Good luck...")


if __name__ == "__main__":
    main()
