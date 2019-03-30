from util import *
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor
from copy import deepcopy
from IOModule import *
import sys
import os
import numpy as np

def tqdm(x):
    return x

## 定义全局变量 用于调试
g_car_status = None
g_road_status = None
g_cars_pool = None
g_cars_pool1 = None
g_road_used = None

## 绘图
import matplotlib
import matplotlib.pyplot as plt

# # %matplotlib inline
#
# # set up matplotlib
# is_ipython = 'inline' in matplotlib.get_backend()
# if is_ipython:
#     from IPython import display
#
# plt.ion()

#
# def plot_durations(y):
#     plt.figure(1, figsize=(10, 10))
#     plt.clf()
#     ax1 = plt.subplot(2, 2, 1)
#     ax2 = plt.subplot(2, 2, 2)
#     ax3 = plt.subplot(2, 2, 3)
#     ax4 = plt.subplot(2, 2, 4)
#     plt.sca(ax1)
#     plt.title('road load rate ')
#     plt.xlabel('time slice')
#     plt.ylabel('load rate')
#     plt.plot(y[:, 0], y[:, 1])
#
#     plt.sca(ax2)
#     plt.title('cars to go ')
#     plt.xlabel('time slice')
#     plt.ylabel('cars num')
#     plt.plot(y[:, 0], y[:, 2])
#
#     plt.sca(ax3)
#     plt.title('cars on road ')
#     plt.xlabel('time slice')
#     plt.ylabel('cars on road')
#     plt.plot(y[:, 0], y[:, 3])
#
#     plt.sca(ax4)
#     plt.title('cars arrived ')
#     plt.xlabel('time slice')
#     plt.ylabel('cars arrived num')
#     plt.plot(y[:, 0], y[:, 4])
#
#     plt.pause(0.001)  # pause a bit so that plots are updated
#     if is_ipython:
#         display.clear_output(wait=True)
#         display.display(plt.gcf())


def __get_time_cost(paths, carL, car_df, road_df):
    # 得到理想情况下的最优时间： sum(path/max(car_speed, road_speed))
    car_time_cost = {}
    all_time_cost = 0
    for car in tqdm(carL):
        if not paths.__contains__(car):
            raise Exception("key not contains in dict")

        path = paths[car]
        time = 0
        # TODO:之后考虑通过路口的时间消耗问题，利用判题器进行该超参数的搜索
        for edge in path:
            time += road_df['length'][edge] / max(road_df['speed'][edge], car_df['speed'][car])

        car_time_cost[car] = time
        all_time_cost += time

    return car_time_cost, all_time_cost


def get_benchmark(paths, car_df, road_df, cross_df, process_num=4):
    """
    针对直接进行路径规划，假设不堵车的情况，得到理想情况下的运行时间
    使用多进程实现
    :param paths: 所有车规划出来的路径,数据格式:字典{carID： [edge path]}
    :param car_df:
    :param road_df:
    :return:  car_time_cost： 每个车的时间消耗{carID: time cost}
              all_time_cost: 所有车时间总消耗
    """
    car_time_cost = {}
    all_time_cost = 0

    carL = list(car_df['id'])
    carL_len = len(carL)

    # 为多进程进行分割数据
    N = int(carL_len / process_num)
    splice = [N * x for x in range(process_num)]
    splice.append(carL_len)

    # 启动多进程
    print('\nget_benchmark: ')
    try:
        p = ProcessPoolExecutor(max_workers=process_num)
        obj_l = []
        for st, ed in zip(splice[:-1], splice[1:]):
            obj = p.submit(__get_time_cost, paths, carL[st:ed], car_df, road_df)
            obj_l.append(obj)

        p.shutdown(wait=True)

        # 将多进程得到的结果进行整合

        #    print([len(obj.result()) for obj in obj_l])
        for obj in obj_l:
            car_time_cost.update(obj.result()[0])
            all_time_cost += obj.result()[1]
    except:
        print("Multi-processing failed, using single processing now")
        car_time_cost, all_time_cost = __get_time_cost(paths, carL, car_df, road_df)

    return car_time_cost, all_time_cost

# 提交结果
"""
controlcarnum = 25
    change = 10
    interval = 90   m1 fail m2 887
"""
def car_num_update(time_slice, load_rate=0, carsum=0):
    controlcarnum = 13
    change = 10
    interval = 80
    # control由三部分构成
    # 基本controlcarnum，正弦int(change * np.sin(time_slice*(2 * np.pi)/interval))
    # 衰减：y=-x^2 + 100或者y=-0.1x^3+100
    control = controlcarnum + \
              int(change * np.sin(time_slice * (2 * np.pi) / interval))
    # 前10秒钟增加发车数

    if time_slice > 0 and time_slice <= 10:
        # control += int(-0.1 * np.power(time_slice, 3) + 100)
        control += int(-1 * np.power(time_slice, 2) + 100)

    # TODO： 根据道路负载修改发车数，保持道路负载的动态平衡，特别是所有车快发完时，可以增大发车数
    if load_rate < 0.11:
        control = int(control * 1.1)
    elif load_rate > 0.11 and load_rate < 0.2:
        control = int(control * 0.85)
    elif load_rate > 0.2:
        control = 0
    else:
        pass

    return control


def super_time_plan(paths, car_df, road_df, cross_df, adl=None):
    """
    尝试基于时间迭代的实时路径规划与时间规划
    :type paths: 所有车的理想路径，可以是基于HC的路径或者直接Dijkstra的路径,数据格式:字典{carID： [edge path]}
    :return:
    """
    # 声明全局变量 用于调试
    global g_car_status
    global g_road_status
    global g_cars_pool
    global g_cars_pool1
    global g_road_used
    time_slice_num = 2000

    # 存储路径和时间规划结果
    paths_fianl = {}
    time_final = {}
    adwE = convert_adl2adl_w(adl)
    adl_cut = deepcopy(adwE)

    y = []

    ## 系统状态初始化：车，路，路口
    # 车： 待发的车、在路上的车、已经到达的车
    # 使用pandas dataframe实现，添加status列：0: wait, N: on road and roadID, -1: arrived
    car_status = car_df.copy(deep=True)
    # 初始化所有车为等待出发状态
    car_status['status'] = 0
    car_status.drop(columns=['from', 'to', 'speed', 'planTime'])  # 删除不使用的数据

    # # 构建发车池，利用理想情况的时间消耗来决定发车顺序
    # cars_pool = car_df.copy(deep=True)
    # cars_pool.drop(columns=['from', 'to', 'speed'], inplace=True)  # 删除不使用的数据
    # # 添加时间消耗列，并使用理想情况的路径时间消耗为该列赋值
    # cars_pool['timeCost'] = 0
    # car_tcost, _ = get_benchmark(paths, car_df, road_df, cross_df)
    # for car_id, tcost in car_tcost.items():
    #     cars_pool.loc[car_id, 'timeCost'] = tcost

    cars_pool = car_df.copy(deep=True)
    cars_pool.drop(columns=['from', 'to', 'speed'], inplace=True)  # 删除不使用的数据
    cars_pool.sort_values(by=['planTime', 'id'], axis=0, ascending=[True, True])


    # print('t_cost:', cars_pool.head())

    # TODO：无效信息：### raod_status: {roadID: {from: [cap, used, {carID: position, carID:position..}], to: [cap, used, {carID: position, carID:position..}]}, roadID:...}

    ## 道路： 道路状态：道路车辆容纳数、当前已占用数, 占用车辆ID和位置
    # 使用pandas dataframe实现：添加列：cap1, used1, cars1, cap2, used2, cars2, 分别表示道路当前方向车容量、车数、路上车的情况
    road_status = road_df.copy(deep=True)
    # 初始化当前道路的车容量，道路使用情况和在该道路的车，按照道路是否双向分开记录道路状态
    road_status['cap1'] = road_df.apply(lambda x: (x['length'] * x['channel']), axis=1)
    road_status['used1'] = 0
    # 将'cars1'设置为object类型，且赋值空字典
    road_status['cars1'] = None
    road_status['cars1'] = road_status['cars1'].astype(object)
    road_status['cars1'] = road_status.cars1.apply(lambda x: {})

    # 对于非双向车道的道路，设置其车辆容纳数为零
    road_status['cap2'] = road_df.apply(lambda x: (x['length'] * x['channel'] * x['isDuplex']), axis=1)
    road_status['used2'] = 0
    # 将'cars2'设置为object类型，且赋值空字典
    road_status['cars2'] = None
    road_status['cars2'] = road_status['cars2'].astype(object)
    road_status['cars2'] = road_status.cars2.apply(lambda x: {})

    roads_cap = road_status['cap1'].sum() + road_status['cap2'].sum()

    # 使用字典，提高运行速度
    road_status_length = road_status['length'].to_dict()
    road_status_cap1 = road_status['cap1'].to_dict()
    road_status_cap2 = road_status['cap2'].to_dict()
    road_df_to = road_df['to'].to_dict()
    road_df_from = road_df['from'].to_dict()
    car_df_speed = car_df['speed'].to_dict()
    road_from_to = road_df[['from','to']].to_dict()
    car_to = car_df['to'].to_dict()

    # print(road_status.head())
    # 路口： 路口？？？

    ## 绘图线程

    # 超参数
    car_num = 25  # 每个时间片发车数量
    cap_rate = 0  # 道路负载率
    cars_arrived_count = 0
    car_debug = 0

    #    carlist = list(car_df['id'])
    print("start time and path planning:")
    for i in tqdm(range(1, time_slice_num)):

        ## 选取当前时间片要出发的车
        # 对发车池的车按照出发时刻和理想状态到达目的地的时间消耗按从小到达排序进行排
        # cars_pool.sort_values(by=['planTime', 'timeCost', 'id'], axis=0, ascending=[True, True, True], inplace=True)
        cars_pool.sort_values(by=['planTime', 'id'], axis=0, ascending=[True, True])

        # 得到应该该时刻出发的车
        temp_car = cars_pool[cars_pool['planTime'] == i]
        # print("cars_pool:", cars_pool.head())
        # print("temp_car:", temp_car.head())
        car_num_count = 0

        # TODO: 设置实时改变carnum的函数
        # update_car_num()
        # car_num = car_num_update(i, cap_rate)
        car_num = 40

        # 选出要发的车
        # 判断是否满足发车条件，满足则发车，不满足则考虑延后发车或者路径重规划
        for carID in temp_car['id']:

            # 能否发车的条件判断：当前道路的车容量是否达到最大（最大值的80%），以及起始位置是否全被占用，以及timecost的消耗是否过大，
            # 对于时间消耗过大的车辆采取延后出发处理（考虑延后次数的限制）
            # 此时每发一辆车，采用状态立即更新：主要更新包括道路使用情况

            # 当发车达到最大值时结束该时间片
            if car_num_count > car_num or car_num == 0:
                #                car_num_count -= 1
                break

            # 得到该车的理想路径
            path = paths[carID]
            # print('path:', path)

            # 判断该条路是否有空位
            # TODO: 判断初始位置是否有空位
            start_road = path[0]
            next_road = path[1]
            # 判断道路方向
            if road_df_to[start_road] in [road_df_from[next_road], road_df_to[next_road]]:
                # 判断剩余车位，保证车位余量大于2
                #                if road_status['cap1'][start_road] - road_status['used1'][start_road] > 2:
                if road_status_cap1[start_road] - len(road_status['cars1'][start_road]) > 2:
                    # print(1)
                    # 可以发车
                    # 更新车的状态，更新发车池的状态、更新道路使用的状态
                    # car_status.loc[carID, 'status'] = start_road

                    cars_pool.drop(axis=0, index=carID, inplace=True)

                    #                    road_status.loc[start_road, 'used1'] += 1
                    # 将在同一条路上的车的字典合并
                    road_status.at[start_road, 'cars1'].update({carID: 0})  # 字典内容表示：{carID， position}

                    # 发车成功，并存入发车计划字典中
                    car_num_count += 1
                    time_final[carID] = [carID, i]
                else:
                    # 不可以发车：车依旧为等待发车状态，将发车时间片向后推1个时间片
                    # 更新发车池
                    # cars_pool.loc[carID, 'planTime'] += 1
                    cars_pool['planTime'][carID] += 1

            elif road_df_from[start_road] in [road_df_from[next_road], road_df_to[next_road]]:
                #                if road_status['cap2'][start_road] - road_status['used2'][start_road] > 2:
                if road_status_cap2[start_road] - len(road_status['cars2'][start_road]) > 2:
                    # print(2)
                    # 可以发车
                    # 更新车的状态，更新发车池的状态、更新道路使用的状态
                    # car_status.loc[carID, 'status'] = start_road

                    cars_pool.drop(axis=0, index=carID, inplace=True)

                    #                    road_status.loc[start_road, 'used2'] += 1
                    # 将在同一条路上的车的字典合并
                    road_status.at[start_road, 'cars2'].update({carID: 0})  # 字典内容表示：{carID， position}

                    # 发车成功，并存入发车计划字典中
                    car_num_count += 1
                    time_final[carID] = [carID, i]
                else:
                    # 不能出发的车放回发车池，并且修改其出发时间为下一个时间片
                    # cars_pool.loc[carID, 'planTime'] += 1
                    cars_pool['planTime'][carID] += 1
            else:
                print("something wrong...")

            # for DEBUG
            # g_car_status = car_status
            # g_cars_pool = cars_pool
            # g_road_status = road_status
            #            print(cars_pool.head())
            #            print(road_status)
            #            print(car_status)

            # print(carID)

        ## 至此完成当前时间片的发车

        ## 将发车池中时间片为本时刻的车向后推迟一个时间片, 其余时间片不改变
        cars_pool['planTime'] = cars_pool.planTime.apply(lambda x: x + 1 if x == i else x)
        # for DEBUG
        # g_cars_pool1 = cars_pool
        #        print(cars_pool.head())

        # 按照路口、道路的顺序进行车辆状态更新
        ## 根据道路状态考虑上路车辆的路径重规划问题,变权重问题
        ## 重规划的出发条件是即将进入的道路已经没有空位，这部分应该放于已上路车辆的状态更新部分
        # for car in cars_on_road:
        #     pass

        # 为下一时间片更新系统状态,两方面更新：车上路的更新和已经在路上的车的更新，主要更新车辆位置
        # car_status['status']、road_status

        # 筛选出路上有车的路
        road_status['used1'] = road_status.apply(lambda x: (len(x['cars1'])), axis=1)
        road_status['used2'] = road_status.apply(lambda x: (len(x['cars2'])), axis=1)
        #        road_used = deepcopy(road_status.loc[(road_status['used1'] > 0) | (road_status['used2'] > 0)])
        road_used = road_status.loc[(road_status['used1'] > 0) | (road_status['used2'] > 0)].copy(deep=True)
        #        road_used = road_status.loc[(len(road_status['cars1']) > 0) | (len(road_status['cars2']) > 0)].copy(deep=True)
        # g_road_used = road_used

        # 将series转换为dict，优化速度
        road_used_cars1 = road_used['cars1'].to_dict()
        road_used_cars2 = road_used['cars2'].to_dict()

        #        print(road_used)
        for road_id in road_used['id']:
            # print(road_id)
            # 更新道路上的车
            #            if road_used['used1'][road_id] > 0:
            if len(road_used_cars1[road_id]) > 0:
                #                car_on_road = deepcopy(road_used['cars1'][road_id])
                #                for car, posi in car_on_road.items():
                car_on_road = list(road_used_cars1[road_id].items())
                for car, posi in car_on_road:
                    car_debug = car
                    road_len = road_status_length[road_id]
                    #                    car_speed = car_status['speed'][car]
                    car_speed = car_df_speed[car]
                    car_path = paths[car]

                    ## 判断是否到达终点
                    #
                    if road_id == car_path[-1]:
                        # 车在最后一段路上
                        next_road = road_id
                    else:
                        # TODO： 此处由于重规划导致节点多次出现，对元素的正序索引会出现死循环的bug，通过倒序索引解决
                        # next_road = car_path[car_path.index(road_id) + 1]

                        # index = len(car_path) - car_path[::-1].index(road_id)
                        # next_road = car_path[index]
                        next_road = car_path[1]

                    next_posi = posi + car_speed

                    # 没有走出这条路
                    if next_posi <= road_len:
                        road_status.at[road_id, 'cars1'].update({car: next_posi})
                    # 走出这条路
                    else:
                        next_posi -= road_len

                        if next_road == road_id:
                            # 到达目的地
                            road_status.at[road_id, 'cars1'].pop(car)  # 删除原来路的车信息
                            #                            road_status.loc[road_id, 'used1'] -= 1

                            #                            car_status.loc[car, 'status'] = -1
                            cars_arrived_count += 1
###############
                            edge = paths[car].pop(0)
                            if paths_fianl.__contains__(car):
                                paths_fianl[car].append(edge)
                            else:
                                paths_fianl[car] = [edge]
                            continue

                        # 判断下一条路的空位
                        # 先判断方向
                        if road_df_to[road_id] == road_df_from[next_road]:
                            #                            if road_status['cap1'][next_road] - road_status['used1'][next_road] > 2:
                            if road_status_cap1[next_road] - len(road_status['cars1'][next_road]) > 2:
                                # 下一条路满足进入要求，进入下一条路
                                road_status.at[next_road, 'cars1'].update({car: next_posi})  # 为下一条路添加车信息
                                #                                road_status.loc[next_road, 'used1'] += 1
                                road_status.at[road_id, 'cars1'].pop(car)  # 删除原来路的车信息
                            #                                road_status.loc[road_id, 'used1'] -= 1

                            #                                car_status.loc[car, 'status'] = next_road # 更新车辆状态
###################
                                edge = paths[car].pop(0)
                                if paths_fianl.__contains__(car):
                                    paths_fianl[car].append(edge)
                                else:
                                    paths_fianl[car] = [edge]
                            else:
                                # 下一条路没有空位，走到该条路末端
                                road_status.at[road_id, 'cars1'].update({car: road_len})
                                # path replan
                                new_path = path_replan_with_time(car, car_path, road_id, next_road, adl_cut, adl, road_from_to, car_to)
                                paths[car] = new_path
                                # print("go to next road failed...")
                                # print(road_status_cap1[next_road] - len(road_status['cars1'][next_road]))
                                # TODO： 考虑重规划路径
                        # 另一个方向
                        elif road_df_to[road_id] == road_df_to[next_road]:
                            #                            if road_status['cap2'][next_road] - road_status['used2'][next_road] > 2:
                            if road_status_cap2[next_road] - len(road_status['cars2'][next_road]) > 2:
                                # 下一条路满足进入要求，进入下一条路
                                road_status.at[next_road, 'cars2'].update({car: next_posi})  # 为下一条路添加车信息
                                #                                road_status.loc[next_road, 'used2'] += 1
                                road_status.at[road_id, 'cars1'].pop(car)  # 删除原来路的车信息
                            #                                road_status.loc[road_id, 'used1'] -= 1

                            #                                car_status.loc[car, 'status'] = next_road  # 更新车辆状态
###################
                                edge = paths[car].pop(0)
                                if paths_fianl.__contains__(car):
                                    paths_fianl[car].append(edge)
                                else:
                                    paths_fianl[car] = [edge]
                            else:
                                # 下一条路没有空位，走到该条路末端
                                # TODO： 走到末端的设定不合理，待考虑
                                road_status.at[road_id, 'cars1'].update({car: road_len})
                                # path replan
                                new_path = path_replan_with_time(car, car_path, road_id, next_road, adl_cut, adl,
                                                                 road_from_to, car_to)
                                paths[car] = new_path
                                # print("go to next road failed...")
                                # print(road_status_cap2[next_road] - len(road_status['cars2'][next_road]))
                                # TODO： 考虑重规划路径

            #            if road_used['used2'][road_id] > 0:
            if len(road_used_cars2[road_id]) > 0:
                #                car_on_road = deepcopy(road_used['cars2'][road_id])
                #                for car, posi in car_on_road.items():
                car_on_road = list(road_used_cars2[road_id].items())
                for car, posi in car_on_road:
                    car_debug = car
                    road_len = road_status_length[road_id]
                    #                    car_speed = car_status['speed'][car]
                    car_speed = car_df_speed[car]
                    car_path = paths[car]

                    ## 判断是否到达终点
                    #
                    if road_id == car_path[-1]:
                        # 车在最后一段路上
                        next_road = road_id
                    else:
                        # TODO： 此处由于重规划导致节点多次出现，对元素的正序索引会出现死循环的bug，通过倒序索引解决
                        # next_road = car_path[car_path.index(road_id) + 1]

                        # index = len(car_path) - car_path[::-1].index(road_id)
                        # next_road = car_path[index]
                        next_road = car_path[1]

                    next_posi = posi + car_speed

                    # 没有走出这条路
                    if next_posi <= road_len:
                        road_status.at[road_id, 'cars2'].update({car: next_posi})
                    # 走出这条路
                    else:
                        next_posi -= road_len

                        if next_road == road_id:
                            # 到达目的地
                            road_status.at[road_id, 'cars2'].pop(car)  # 删除原来路的车信息
                            #                            road_status.loc[road_id, 'used2'] -= 1

                            #                            car_status.loc[car, 'status'] = -1
                            cars_arrived_count += 1

###################
                            edge = paths[car].pop(0)
                            if paths_fianl.__contains__(car):
                                paths_fianl[car].append(edge)
                            else:
                                paths_fianl[car] = [edge]

                            continue

                        # 判断下一条路的空位
                        # 先判断方向
                        if road_df_from[road_id] == road_df_from[next_road]:
                            #                            if road_status['cap1'][next_road] - road_status['used1'][next_road] > 2:
                            if road_status_cap1[next_road] - len(road_status['cars1'][next_road]) > 2:
                                # 下一条路满足进入要求，进入下一条路
                                road_status.at[next_road, 'cars1'].update({car: next_posi})  # 为下一条路添加车信息
                                #                                road_status.loc[next_road, 'used1'] += 1
                                road_status.at[road_id, 'cars2'].pop(car)  # 删除原来路的车信息
                            #                                road_status.loc[road_id, 'used2'] -= 1

                            #                                car_status.loc[car, 'status'] = next_road  # 更新车辆状态
###################
                                edge = paths[car].pop(0)
                                if paths_fianl.__contains__(car):
                                    paths_fianl[car].append(edge)
                                else:
                                    paths_fianl[car] = [edge]

                            else:
                                # 下一条路没有空位，走到该条路末端
                                road_status.at[road_id, 'cars2'].update({car: road_len})

                                # path replan
                                new_path = path_replan_with_time(car, car_path, road_id, next_road, adl_cut, adl,
                                                                 road_from_to, car_to)
                                paths[car] = new_path
                                # print("go to next road failed...")
                                # print(road_status_cap1[next_road] - len(road_status['cars1'][next_road]))
                                # TODO： 考虑重规划路径
                        # 另一个方向
                        elif road_df_from[road_id] == road_df_to[next_road]:
                            #                            if road_status['cap2'][next_road] - road_status['used2'][next_road] > 2:
                            if road_status_cap2[next_road] - len(road_status['cars2'][next_road]) > 2:
                                # 下一条路满足进入要求，进入下一条路
                                road_status.at[next_road, 'cars2'].update({car: next_posi})  # 为下一条路添加车信息
                                #                                road_status.loc[next_road, 'used2'] += 1
                                road_status.at[road_id, 'cars2'].pop(car)  # 删除原来路的车信息
                            #                                road_status.loc[road_id, 'used2'] -= 1

                            #                                car_status.loc[car, 'status'] = next_road  # 更新车辆状态
###################
                                edge = paths[car].pop(0)
                                if paths_fianl.__contains__(car):
                                    paths_fianl[car].append(edge)
                                else:
                                    paths_fianl[car] = [edge]

                            else:
                                # 下一条路没有空位，走到该条路末端
                                road_status.at[road_id, 'cars2'].update({car: road_len})

                                # path replan
                                new_path = path_replan_with_time(car, car_path, road_id, next_road, adl_cut, adl,
                                                                 road_from_to, car_to)
                                paths[car] = new_path
                                # print("go to next road failed...")
                                # print(road_status_cap2[next_road] - len(road_status['cars2'][next_road]))
                                # TODO： 考虑重规划路径

        ## 记录改时间片出发的车辆，以及路径信息（可能存在路径更新的车辆）
        # print(car_status)
        # print(road_status)
        #### 至此完成一个时间片的发车和状态更新
        # 发车池中没有车可发，且所有车均到达目的地时，时间片结束

        ### TODO： 添加系统状态监测和系统负载计算
        cap_rate = (road_status['used1'].sum() + road_status['used2'].sum()) / roads_cap
        cars_on_road = (road_status['used1'].sum() + road_status['used2'].sum())
        #        print('cap_rate:', cap_rate)
        # 可视化负载率,添加剩余待发车车辆数和到达车辆数
        y.append(np.array([i, cap_rate, car_num_count, cars_on_road, cars_arrived_count]))
        # plot_durations(np.array(y))

        ## 重建邻接表
        # 找出拥挤道路,删除其邻接关系
        road_status['cut'] = road_status.apply(
            lambda x: 1 if x['cap1'] - len(x['cars1']) < 3 or (3 > x['cap2'] - len(x['cars2']) > 0) else 0, axis=1)
        road_cut = road_status.loc[road_status['cut'] == 1]
        adl_cut = cut_adl(adwE, road_cut)
        # print(len(adl_cut))

        ## 时间片终止条件：所有车到达终点
        #        if sum((list(car_status['status'] == -1))) == len(car_status['status']):
        #        if sum(list(road_status['used1'])) + sum(list(road_status['used2'])) == 0:
        # if sum(road_status['cars1'] != {}) + sum(road_status['cars2'] != {}) == 0:
        if i > 50:
            if (road_status['used1'].sum() + road_status['used2'].sum()) == 0:
                print("all cars have arrived to the end and spend time is:", i)
                break
        #
        # if i > 640:
        #     pa = paths[car_debug]
        #     print("cannot arrive within 1500 time slice.")


        if i > 2500:
            print("cannot arrive within 1500 time slice.")
            break
    #        sys.exit()
    # car_df_time = car_df.copy(deep=True)
    # for carID in car_df_time['id']:
    #     car_df_time.loc[carID, 'planTime'] = time_final[carID][1]

    # paths_fianl = paths
    return time_final,  paths_fianl


## TODO:优化程序运行速度，可能是对Dataframe的深拷贝导致耗时严重问题

# 重规划路径
def path_replan_with_time(car_id, car_path,
                          road, next_road,
                          adl_cut,
                          adl,
                          road_from_to,
                          car_to):
    st = [road_from_to['from'][road], road_from_to['to'][road]]
    temp = [road_from_to['from'][next_road], road_from_to['to'][next_road]]
    # 找重规划的起始点
    if st[0] in temp:
        st = st[0]
    elif st[1] in temp:
        st = st[1]
    else:
        raise Exception('something wrong...')

    ed = car_to[car_id]

    # 剪掉当前道路的邻接关系
    adl_cut_twice = simple_cut(adl_cut, road_from_to['from'][road], road_from_to['to'][road])

    try:
        path_n = shortest_path(adl_cut_twice, st, ed)
    except:
        # 如果失败则为空
        path_n = []
    # 判断重规划是否成功
    if len(path_n) != 0:
        path_e = get_path_n2e(path_n, adl)

        # cut_index = car_path.index(road) + 1

        # new_path = car_path[:cut_index] + path_e
        new_path = [road] + path_e
    else:
        new_path = car_path
        # print('replan failed')

    # if car_id == 10013:
    #     print(new_path)

    return new_path


def simple_cut(adl_cut, road_from, road_to):
    # 剪除当前道路自身的邻接关系
    adl = deepcopy(adl_cut)
    node = road_from
    next_node = road_to
    if adl.__contains__(node):
        if adl[node].__contains__(next_node):
                adl[node].pop(next_node)
    if adl.__contains__(next_node):
        if adl[next_node].__contains__(node):
                adl[next_node].pop(node)
    return adl


def cut_adl(adl, rc):
    adl_cut = deepcopy(adl)
    for node, next_node in zip(rc['from'], rc['to']):
        # 将双向邻接关系都剪断
        if adl_cut.__contains__(node):
            if adl_cut[node].__contains__(next_node):
                adl_cut[node].pop(next_node)
        if adl_cut.__contains__(next_node):
            if adl_cut[next_node].__contains__(node):
                adl_cut[next_node].pop(node)

    return adl_cut


## 测试结果
# path由get_all_paths_with_hc获得
# config：  car_num =20 所有车到达目的地:85  实际耗时：3s
# config0:  car_num = 20 所有车到达目的地：958  实际耗时：5min左右
# config0:  car_num = 20 所有车到达目的地：913  实际耗时：5min34s

# path由get_all_cars_paths获得
# config：  car_num =20 所有车到达目的地:55  实际运行耗时：1s
# config0:  car_num = 20 所有车到达目的地：709  实际运行耗时：2min44s左右
# config0:  car_num = 20 所有车到达目的地：709  实际运行耗时：2min40s左右
# config0:  car_num = 30 所有车到达目的地：>1000  实际运行耗时：13min54s左右

# 优化之后
#    path由get_all_cars_paths获得
# config0:  car_num = 20 所有车到达目的地：679  实际运行耗时：2min32s左右
# config1:  car_num = 20 所有车到达目的地：662  实际运行耗时：1min06s左右

#    path由get_all_paths_with_hc获得
# config1:  car_num = 20 所有车到达目的地：835  实际运行耗时：2min22s左右
# config0:  car_num = 20 所有车到达目的地：>1000  实际运行耗时：9min27s左右

# to be continued......

# 提交结果
"""

"""

def get_time_plan7(paths, car_df, road_df, cross_df):
    '''
    分批出发，凑够一定数量的车再发车，可能某个时刻不发车
    并加入对发车数量的控制，开始为单调递减，其后为固定数量
    最优参数 controlcarnum=16 a=2 b=0.15
    :param car_df:
    :return:
    基本Dijkstra
    加hc
    cut_channel_level=1
    cut_channel_level=2
    16-1486
    '''
    time_plans = {}


    # 根据每辆车的计划出发时间进行升序排列
    # car_df_sort = car_df.sort_values(by='planTime', axis=0, ascending=True)
    # 根据每辆车的计划出发时间进行升序排列 速度降序排列
    # car_df_sort = car_df.sort_values(by=['planTime', 'speed'], axis=0, ascending=[True, False])
    # print(car_df_sort.head(50))

    car_df_sort = car_df.copy(deep=True)
    # 添加时间消耗列，并使用理想情况的路径时间消耗为该列赋值
    car_df_sort['timeCost'] = 0
    car_tcost, _ = get_benchmark(paths, car_df, road_df, cross_df)
    for car_id, tcost in car_tcost.items():
        # car_df_sort.loc[car_id, 'timeCost'] = tcost
        car_df_sort['timeCost'][car_id] = tcost

    car_df_sort.sort_values(by=['planTime', 'timeCost', 'id'], axis=0, ascending=[True, True, True], inplace=True)

    carsum = car_df_sort.shape[0]

    i = 1
    tempsave = []
    time_last = -1
    idtime = -1

    """
    #发车数量控制1 
    #先单调递减，再固定
    #最优参数 a=2 b=0.15 controlcarnum = 16
    a = 2  # 控制最开始发车数量为a*controlcarnum
    b = 0.15  # 控制b*carsum辆车以后发车数量固定为controlcarnum
    controlcarnum = 16
    if i< b * carsum:
        control = int(controlcarnum * (a + ((1-a)*(i-1))/(b*carsum)))
    else:
        control = controlcarnum
    """


    controlcarnum = 29
    change = 4
    interval = int(carsum/11)
    control = controlcarnum+int(change * np.sin(i*(2 * np.pi)/interval))

    print("get_time_plan7:")
    for carID, pT in tqdm(zip(car_df_sort['id'], car_df_sort['planTime'])):
        tempsave.append(carID)
        if (i % control) == 0:
            if pT <= time_last:
                idtime = time_last + 1
            else:
                idtime = pT

            for id in tempsave:
                time_plans[id] = [id, idtime]
                car_df_sort.loc[id, 'planTime'] = idtime  #记录实际安排的出发时间
                tempsave = []

            """
            #发车控制1
            if i < b * carsum:
                control = int(controlcarnum * (a + ((1 - a) * (i - 1)) / (b * carsum)))
            else:
                control = controlcarnum
            """

            #发车控制2
            control = controlcarnum + int(change * np.sin(i * (2 * np.pi) / interval))


            time_last = idtime

        i += 1

    for id in tempsave:   #将最后剩下的添加进来
        time_plans[id] = [id, time_last+1]
        car_df_sort.loc[id, 'planTime'] = time_last+1   #记录实际安排的出发时间

    # print(car_df_sort.head(50))

    return time_plans, car_df_sort

# 调参记录
"""
i>600 controlcarnum = 26 3 11 剪枝参数cut_channel_level=1, cut_speed_level=1  m1:failed m2:662
"""


def get_time_plan8(car_df, road_df, cross_df):
    """
    brief: 按照车辆出发点和终止点分类后发车
    成绩： +500 m2 1040 m1 failed
    :param car_df:
    :return:
    """
    time_plans = {}

    half_node_num = int(len(cross_df['id'])/2)

    # 根据每辆车的计划出发时间进行升序排列
    # car_df_sort = car_df.sort_values(by='planTime', axis=0, ascending=True)
    # road_used = road_status.loc[(road_status['used1'] > 0) | (road_status['used2'] > 0)].copy(deep=True)
    first_part = car_df.loc[(car_df['from'] <= half_node_num)].copy(deep=True)
    second_part = car_df.loc[(car_df['from'] > half_node_num)].copy(deep=True)

    for carID, pT in zip(first_part['id'], first_part['planTime']):
        time_plans[carID] = [carID, pT]

    for carID, pT in zip(second_part['id'], second_part['planTime']):
        pT += 300
        time_plans[carID] = [carID, pT]

    return time_plans


def get_time_plan9(paths, car_df, road_df, cross_df):
    '''
    分批出发，某一时刻发车数量多于一定数量顺延
    '''
    # 最优参数
    controlcarnum = 37  # 37

    time_plans = {}

    # # 根据每辆车的计划出发时间进行升序排列 速度降序排列 id升序
    # # car_df_sort = car_df.sort_values(by=['planTime', 'speed', 'id'], axis=0, ascending=[True, False, True])
    # # 根据每辆车的速度降序排列 id升序
    # car_df_sort = car_df.sort_values(by=['speed', 'id'], axis=0, ascending=[False, True])
    # # print(car_df_sort.head(20))


    car_df_sort = car_df.copy(deep=True)
    # 添加时间消耗列，并使用理想情况的路径时间消耗为该列赋值
    car_df_sort['timeCost'] = 0
    car_tcost, _ = get_benchmark(paths, car_df, road_df, cross_df)
    for car_id, tcost in car_tcost.items():
        car_df_sort.loc[car_id, 'timeCost'] = tcost

    # car_df_sort.sort_values(by=['planTime', 'timeCost', 'id'], axis=0, ascending=[True, True, True], inplace=True)
    car_df_sort.sort_values(by=['timeCost', 'id'], axis=0, ascending=[True, True], inplace=True)

    carsum = car_df_sort.shape[0]


    i = 1
    timemax_last = -1
    idtime = -1
    for carID, pT in zip(car_df_sort['id'], car_df_sort['planTime']):
        idtime = max(timemax_last, pT)
        time_plans[carID] = [carID, idtime]
        car_df_sort.loc[carID, 'planTime'] = idtime  # 记录实际安排的出发时间
        if idtime > timemax_last:
            timemax_last=idtime
        else:
            pass

        if (i % controlcarnum) == 0:
            timemax_last += 1
        i += 1

    print("max plantime: ", timemax_last)
    return time_plans, car_df_sort


if __name__ == '__main__':
    rpath = '../config0'
    path = rpath + '/cross.txt'
    path1 = rpath + '/road.txt'
    path2 = rpath + '/car.txt'
    path3 = rpath + '/answer.txt'

    cross_df = read_from_txt(path)
    # print(cross_df.head())
    # print(cross_df.shape)

    road_df = read_from_txt(path1)
    # print(road_df.head())
    # print(road_df.shape)

    car_df = read_from_txt(path2)
    # print(car_df.head())
    # print(car_df.shape)

    al = build_adjacency_list(cross_df, road_df)
    # pa = get_all_paths_with_weight_update(al, road_df, car_df, cross_df)
    # pa = get_all_paths_with_hc(al, road_df, car_df['id'], car_df['from'], car_df['to'])
    pa = get_all_cars_paths(al, car_df['id'], car_df['from'], car_df['to'], use_networkx=False)
    print(pa[10013])
    time_plan,  path_plan = super_time_plan(pa, car_df, road_df, cross_df, al)
    print(path_plan[10013])
    # print(time_plan)
    # print(car_time)
    print('end')
    # os.system('pause')
