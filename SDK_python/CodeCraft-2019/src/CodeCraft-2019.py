import logging
import sys
import pandas
import numpy as np
# from util import build_adjacency_list, adj_list_visualize, get_path, build_ad_list_without_edge_id
from util import *
from IOModule import *


# from move_zp import *


logging.basicConfig(level=logging.DEBUG,
                    filename='../../logs/CodeCraft-2019.log',
                    format='[%(asctime)s] %(levelname)s [%(funcName)s: %(filename)s, %(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filemode='a')


def main():
    print("hello")

    if len(sys.argv) != 5:
        logging.info('please input args: car_path, road_path, cross_path, answerPath')
        exit(1)

    car_path = sys.argv[1]
    road_path = sys.argv[2]
    cross_path = sys.argv[3]
    answer_path = sys.argv[4]

    logging.info("car_path is %s" % (car_path))
    logging.info("road_path is %s" % (road_path))
    logging.info("cross_path is %s" % (cross_path))
    logging.info("answer_path is %s" % (answer_path))

    # to read input file

    car_df = read_from_txt(car_path)
    road_df = read_from_txt(road_path)
    cross_df = read_from_txt(cross_path)

    # process

    # build adjacency list
    ad_l = build_adjacency_list(cross_df, road_df)

    # get path plans
    paths = get_all_cars_paths(ad_l, car_df['id'], car_df['from'], car_df['to'], use_networkx=True)

    # get time plans
    time_plans = get_time_plan1(car_df)

    # get answer
    answers = get_answer(car_df['id'], paths, time_plans)

    # to write output file
    write_answer2file(answer_path, answers)

    print("Good luck...")


if __name__ == "__main__":
    main()
