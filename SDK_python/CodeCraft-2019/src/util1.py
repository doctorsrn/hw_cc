from util import *
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor
from copy import deepcopy
from IOModule import *


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
    splice = [N*x for x in range(process_num)]
    splice.append(carL_len)

    # 启动多进程
    print('\nget_benchmark: ')
    p = ProcessPoolExecutor(max_workers=process_num)
    obj_l = []
    for st, ed in zip(splice[:-1], splice[1:]):
        obj = p.submit(__get_time_cost, paths, carL[st:ed], car_df, road_df)
        obj_l.append(obj)

    p.shutdown(wait=True)

    # 将多进程得到的结果进行整合
    # print([len(obj.result()) for obj in obj_l])
    for obj in obj_l:
        car_time_cost.update(obj.result()[0])
        all_time_cost += obj.result()[1]

    return car_time_cost, all_time_cost


def super_time_plan(paths, car_df, road_df, cross_df):
    """
    尝试基于时间迭代的实时路径规划与时间规划
    :type paths: 所有车的理想路径，可以是基于HC的路径或者直接Dijkstra的路径
    :return:
    """
    time_slice_num = 20000

    # 存储路径和时间规划结果
    paths_fianl = {}
    time_final = {}

    ## 系统状态初始化：车，路，路口
    # 车： 待发的车、在路上的车、已经到达的车
    # 使用pandas dataframe实现，添加status列：0: wait, N: on road and roadID, -1: arrived
    car_status = deepcopy(car_df)
    # 初始化所有车为等待出发状态
    car_status['status'] = 0

    # 构建发车池，利用理想情况的时间消耗来决定发车顺序
    cars_pool = deepcopy(car_df)
    # 添加时间消耗列，并使用理想情况的路径时间消耗为该列赋值
    cars_pool['timeCost'] = 0
    car_tcost, _ = get_benchmark(paths, car_df, road_df, cross_df)
    for car_id, tcost in car_tcost.items():
        cars_pool.loc[car_id, 'timeCost'] = tcost
    # print('t_cost:', cars_pool.head())

    # TODO：无效信息：### raod_status: {roadID: {from: [cap, used, {carID: position, carID:position..}], to: [cap, used, {carID: position, carID:position..}]}, roadID:...}

    ## 道路： 道路状态：道路车辆容纳数、当前已占用数, 占用车辆ID和位置
    # 使用pandas dataframe实现：添加列：cap1, used1, cars1, cap2, used2, cars2, 分别表示道路当前方向车容量、车数、路上车的情况
    road_status = deepcopy(road_df)
    # 初始化当前道路的车容量，道路使用情况和在该道路的车，按照道路是否双向分开记录道路状态
    road_status['cap1'] = road_df.apply(lambda x: (x['length'] * x['channel']), axis=1)
    road_status['used1'] = 0
    road_status['cars1'] = 0
    # 对于非双向车道的道路，设置其车辆容纳数为零
    road_status['cap2'] = road_df.apply(lambda x: (x['length'] * x['channel'] * x['isDuplex']), axis=1)
    road_status['used2'] = 0
    road_status['cars2'] = 0
    # print(road_status.head())
    # 路口： 路口？？？

    # 超参数
    carnum = 20   # 每个时间片发车数量

    carlist = list(car_df['id'])

    for i in tqdm(range(1, time_slice_num)):

        ## 选取当前时间片要出发的车
        # 对发车池的车按照出发时刻和理想状态到达目的地的时间消耗按从小到达排序进行排
        cars_pool.sort_values(by=['planTime', 'timeCost', 'id'], axis=0, ascending=[True, True, True], inplace=True)
        # 得到应该该时刻出发的车
        temp_car = cars_pool[cars_pool['planTime'] == i]
        # print("cars_pool:", cars_pool.head())
        # print("temp_car:", temp_car.head())

        # 选出要发的车
        # 判断是否满足发车条件，满足则发车，不满足则考虑延后发车或者路径重规划
        for _ in range(carnum):

            # 能否发车的条件判断：当前道路的车容量是否达到最大（最大值的80%），以及起始位置是否全被占用，以及timecost的消耗是否过大，
            # 对于时间消耗过大的车辆采取延后出发处理（考虑延后次数的限制）
            # 此时每发一辆车，采用状态立即更新：主要更新包括道路使用情况
            pass

        ## 将本时间片不能出发的车放回发车池，并且修改其出发时间为下一个发车池

        ## 根据道路状态考虑上路车辆的路径重规划问题,变权重问题
        ## 重规划的出发条件是即将进入的道路已经没有空位，这部分应该放于已上路车辆的状态更新部分
        # for car in cars_on_road:
        #     pass


        # 为下一时间片更新系统状态,两方面更新：车上路的更新和已经在路上的车的更新，主要更新车辆位置
        # car_status['status']、road_status

        ## 记录改时间片出发的车辆，以及路径信息（可能存在路径更新的车辆）

        # 发车池中没有车可发，且所有车均到达目的地时，时间片结束

        exit()


if __name__ == '__main__':
    rpath = '../config1'
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
    pa = get_all_paths_with_hc(al, road_df, car_df['id'], car_df['from'], car_df['to'])
    super_time_plan(pa, car_df, road_df, cross_df)


