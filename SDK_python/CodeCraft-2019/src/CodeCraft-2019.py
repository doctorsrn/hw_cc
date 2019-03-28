import logging
import sys
from util import *
from util1 import *
from IOModule import *
import os

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
    # ad_l = build_adjacency_list2(cross_df, road_df)


    # # get time plans
    # # 效果最好的是get_time_plan6
    time_plans, car_df_actual = get_time_plan5(car_df)
    # pa = get_all_cars_paths(ad_l, car_df['id'], car_df['from'], car_df['to'], use_networkx=False)
    # time_plans, car_df_actual = get_time_plan7(pa, car_df, road_df, cross_df)

    # super time plan test
    # pa = get_all_cars_paths(ad_l, car_df['id'], car_df['from'], car_df['to'], use_networkx=False)
    # pa = get_all_paths_with_hc(ad_l, road_df, car_df['id'], car_df['from'], car_df['to'])
    # time_plans, car_df_actual = super_time_plan(pa, car_df, road_df, cross_df)

    # pa = get_all_cars_paths(ad_l, car_df['id'], car_df['from'], car_df['to'], use_networkx=False)
    paths = get_all_paths_with_weight_update(ad_l, road_df, car_df_actual, cross_df, pathType=2, update_w=True)
    # time_plans, paths = super_time_plan(pa, car_df, road_df, cross_df, ad_l)

    # 效果最好的是 getallpaths_dj_cw 和 getallpaths_dj_cw2
    # paths = getallpaths_dj_cw(ad_l, road_df, car_df_actual)
    # paths = getallpaths_dj_cw2(ad_l, road_df, car_df_actual)

    # plan8
    # time_plans = get_time_plan8(car_df, road_df, cross_df)


    # get path plans
    # 效果最好的是 get_all_paths_with_hc_cw
    # paths = get_all_cars_paths(ad_l, car_df['id'], car_df['from'], car_df['to'], use_networkx=False)
    # paths = get_all_paths_with_hc(ad_l, road_df, car_df['id'], car_df['from'], car_df['to'])
    # paths = get_all_paths_with_weight_update(ad_l, road_df, car_df_actual, cross_df, update_w=True)
    # paths = get_allcarspaths_floyd(ad_l, car_df)
    # paths = get_all_cars_paths(ad_l, car_df['id'], car_df['from'], car_df['to'], use_networkx=False)
    # paths = get_all_cars_paths_cw(ad_l, car_df, use_networkx=False)
    # paths = get_all_paths_with_hc(ad_l, road_df, car_df['id'], car_df['from'], car_df['to'])
    # paths = get_all_paths_with_hc_cw(ad_l, road_df, car_df_actual)


    # # get time plans
    # time_plans = get_time_plan0(car_df)

    # get answer
    answers = get_answer(car_df['id'], paths, time_plans)

    # to write output file
    write_answer2file(answer_path, answers)

    # print("Good luck...")


if __name__ == "__main__":
    main()
