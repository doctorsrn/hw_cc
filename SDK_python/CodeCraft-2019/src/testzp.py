import logging
import sys
from util import *
from IOModule import *
import os
import time


def main():
    # print("hello")

    rpath = '../config0'
    cross_path = rpath + '/cross.txt'
    road_path = rpath + '/road.txt'
    car_path = rpath + '/car.txt'
    answer_path = rpath + '/answer.txt'

    car_df = read_car_from_txt(car_path)
    # print(car_df.head())
    road_df = read_road_from_txt(road_path)
    cross_df = read_cross_from_txt(cross_path)

    # process

    # count=dict(car_df['from'].value_counts())
    # print(count)

    # car_df_sort = car_df.sort_values(by=['planTime', 'speed'], axis=0, ascending=[True, False])
    # print(car_df_sort.head())
    # car_df_sort['planTime'][10018] = 2
    # print(car_df_sort.head())


    # build adjacency list
    ad_l = build_adjacency_list2(cross_df, road_df)

    """
    #floyed test
    startime = time.time()
    Floydpath = init_Floyd(ad_l)
    path = get_floyd_path(Floydpath, 46, 45)
    endtime = time.time()
    print(endtime-startime)
    print(path)
    # get time plans
    """

    time_plans, car_df_actual = get_time_plan6(car_df)

    # get path plans
    paths = get_allcarspaths_floyd(ad_l, car_df)
    # paths = get_all_cars_paths(ad_l, car_df['id'], car_df['from'], car_df['to'], use_networkx=False)
    #paths = get_all_cars_paths_cw(ad_l, car_df, use_networkx=False)

    # paths = get_all_paths_with_hc(ad_l, road_df, car_df['id'], car_df['from'], car_df['to'])
    #paths = get_all_paths_with_hc_cw(ad_l, road_df, car_df_actual)

    # get answer
    answers = get_answer(car_df['id'], paths, time_plans)

    # to write output file
    write_answer2file(answer_path, answers)

    print("Good luck...")


if __name__ == "__main__":
    main()