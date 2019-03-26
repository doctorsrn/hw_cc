from util import *
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor
from copy import deepcopy
from IOModule import *
import sys

## 定义全局变量 用于调试
g_car_status = None
g_road_status = None
g_cars_pool = None
g_cars_pool1 = None
g_road_used = None


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


def super_time_plan(paths, car_df, road_df, cross_df):
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

    # print(road_status.head())
    # 路口： 路口？？？

    # 超参数
    car_num = 20  # 每个时间片发车数量

    carlist = list(car_df['id'])

    for i in tqdm(range(1, time_slice_num)):

        ## 选取当前时间片要出发的车
        # 对发车池的车按照出发时刻和理想状态到达目的地的时间消耗按从小到达排序进行排
        cars_pool.sort_values(by=['planTime', 'timeCost', 'id'], axis=0, ascending=[True, True, True], inplace=True)
        # 得到应该该时刻出发的车
        temp_car = cars_pool[cars_pool['planTime'] == i]
        # print("cars_pool:", cars_pool.head())
        # print("temp_car:", temp_car.head())
        car_num_count = 0

        # TODO: 设置实时改变carnum的函数
        # update_car_num()

        # 选出要发的车
        # 判断是否满足发车条件，满足则发车，不满足则考虑延后发车或者路径重规划
        for carID in temp_car['id']:
            # 能否发车的条件判断：当前道路的车容量是否达到最大（最大值的80%），以及起始位置是否全被占用，以及timecost的消耗是否过大，
            # 对于时间消耗过大的车辆采取延后出发处理（考虑延后次数的限制）
            # 此时每发一辆车，采用状态立即更新：主要更新包括道路使用情况

            # 当发车达到最大值时结束该时间片
            if car_num_count > car_num:
                car_num_count = 1
                break

            # 得到该车的理想路径
            path = paths[carID]
            # print('path:', path)

            # 判断该条路是否有空位
            # TODO: 判断初始位置是否有空位
            start_road = path[0]
            next_road = path[1]
            # 判断道路方向
            if road_df['to'][start_road] in [road_df['from'][next_road], road_df['to'][next_road]]:
                # 判断剩余车位，保证车位余量大于2
                if road_status['cap1'][start_road] - road_status['used1'][start_road] > 2:
                    # print(1)
                    # 可以发车
                    # 更新车的状态，更新发车池的状态、更新道路使用的状态
                    car_status.loc[carID, 'status'] = start_road

                    cars_pool.drop(axis=0, index=carID, inplace=True)

                    road_status.loc[start_road, 'used1'] += 1
                    # 将在同一条路上的车的字典合并
                    road_status.at[start_road, 'cars1'].update({carID: 1})  # 字典内容表示：{carID， position}

                    # 发车成功，并存入发车计划字典中
                    car_num_count += 1
                    time_final[carID] = [carID, i]
                else:
                    # 不可以发车：车依旧为等待发车状态，将发车时间片向后推1个时间片
                    # 更新发车池
                    cars_pool.loc[carID, 'planTime'] += 1


            elif road_df['from'][start_road] in [road_df['from'][next_road], road_df['to'][next_road]]:
                if road_status['cap2'][start_road] - road_status['used2'][start_road] > 2:
                    # print(2)
                    # 可以发车
                    # 更新车的状态，更新发车池的状态、更新道路使用的状态
                    car_status.loc[carID, 'status'] = start_road

                    cars_pool.drop(axis=0, index=carID, inplace=True)

                    road_status.loc[start_road, 'used2'] += 1
                    # 将在同一条路上的车的字典合并
                    road_status.at[start_road, 'cars2'].update({carID: 1})  # 字典内容表示：{carID， position}

                    # 发车成功，并存入发车计划字典中
                    car_num_count += 1
                    time_final[carID] = [carID, i]
                else:
                    # 不能出发的车放回发车池，并且修改其出发时间为下一个时间片
                    cars_pool.loc[carID, 'planTime'] += 1
            else:
                print("something wrong...")

            # for DEBUG
            g_car_status = car_status
            g_cars_pool = cars_pool
            g_road_status = road_status
            #            print(cars_pool.head())
            #            print(road_status)
            #            print(car_status)

            # print(carID)

        ## 至此完成当前时间片的发车

        ## 将发车池中时间片为本时刻的车向后推迟一个时间片, 其余时间片不改变
        cars_pool['planTime'] = cars_pool.planTime.apply(lambda x: x + 1 if x == i else x)
        # for DEBUG
        g_cars_pool1 = cars_pool
        #        print(cars_pool.head())

        # 按照路口、道路的顺序进行车辆状态更新
        ## 根据道路状态考虑上路车辆的路径重规划问题,变权重问题
        ## 重规划的出发条件是即将进入的道路已经没有空位，这部分应该放于已上路车辆的状态更新部分
        # for car in cars_on_road:
        #     pass

        # 为下一时间片更新系统状态,两方面更新：车上路的更新和已经在路上的车的更新，主要更新车辆位置
        # car_status['status']、road_status
        # 筛选出路上有车的路
        road_used = deepcopy(road_status.loc[(road_status['used1'] > 0) | (road_status['used2'] > 0)])
        g_road_used = road_used
        #        print(road_used)
        for road_id in road_used['id']:
            # print(road_id)
            # 更新道路上的车
            if road_used['used1'][road_id] > 0:
                car_on_road = deepcopy(road_used['cars1'][road_id])
                for car, posi in car_on_road.items():
                    road_len = road_status['length'][road_id]
                    car_speed = car_status['speed'][car]
                    car_path = paths[car]

                    ## 判断是否到达终点
                    #
                    if road_id == car_path[-1]:
                        # 车在最后一段路上
                        next_road = road_id
                    else:
                        next_road = car_path[car_path.index(road_id)+1]

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
                            road_status.loc[road_id, 'used1'] -= 1

                            car_status.loc[car, 'status'] = -1
                            continue

                        # 判断下一条路的空位
                        # 先判断方向
                        if road_df['to'][road_id] == road_df['from'][next_road]:
                            if road_status['cap1'][next_road] - road_status['used1'][next_road] > 2:
                                # 下一条路满足进入要求，进入下一条路
                                road_status.at[next_road, 'cars1'].update({car: next_posi})  # 为下一条路添加车信息
                                road_status.loc[next_road, 'used1'] += 1
                                road_status.at[road_id, 'cars1'].pop(car)  # 删除原来路的车信息
                                road_status.loc[road_id, 'used1'] -= 1

                                car_status.loc[car, 'status'] = next_road # 更新车辆状态
                            else:
                                # 下一条路没有空位，走到该条路末端
                                road_status.at[road_id, 'cars1'].update({car: road_len})
                                # TODO： 考虑重规划路径
                        # 另一个方向
                        elif road_df['to'][road_id] == road_df['to'][next_road]:
                            if road_status['cap2'][next_road] - road_status['used2'][next_road] > 2:
                                # 下一条路满足进入要求，进入下一条路
                                road_status.at[next_road, 'cars2'].update({car: next_posi})  # 为下一条路添加车信息
                                road_status.loc[next_road, 'used2'] += 1
                                road_status.at[road_id, 'cars1'].pop(car)  # 删除原来路的车信息
                                road_status.loc[road_id, 'used1'] -= 1

                                car_status.loc[car, 'status'] = next_road  # 更新车辆状态
                            else:
                                # 下一条路没有空位，走到该条路末端
                                # TODO： 走到末端的设定不合理，待考虑
                                road_status.at[road_id, 'cars1'].update({car: road_len})
                                # TODO： 考虑重规划路径

            if road_used['used2'][road_id] > 0:
                car_on_road = deepcopy(road_used['cars2'][road_id])
                for car, posi in car_on_road.items():
                    road_len = road_status['length'][road_id]
                    car_speed = car_status['speed'][car]
                    car_path = paths[car]

                    ## 判断是否到达终点
                    #
                    if road_id == car_path[-1]:
                        # 车在最后一段路上
                        next_road = road_id
                    else:
                        next_road = car_path[car_path.index(road_id)+1]

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
                            road_status.loc[road_id, 'used2'] -= 1

                            car_status.loc[car, 'status'] = -1
                            continue

                        # 判断下一条路的空位
                        # 先判断方向
                        if road_df['from'][road_id] == road_df['from'][next_road]:
                            if road_status['cap1'][next_road] - road_status['used1'][next_road] > 2:
                                # 下一条路满足进入要求，进入下一条路
                                road_status.at[next_road, 'cars1'].update({car: next_posi})  # 为下一条路添加车信息
                                road_status.loc[next_road, 'used1'] += 1
                                road_status.at[road_id, 'cars2'].pop(car)  # 删除原来路的车信息
                                road_status.loc[road_id, 'used2'] -= 1

                                car_status.loc[car, 'status'] = next_road  # 更新车辆状态
                            else:
                                # 下一条路没有空位，走到该条路末端
                                road_status.at[road_id, 'cars2'].update({car: road_len})
                                # TODO： 考虑重规划路径
                        # 另一个方向
                        elif road_df['from'][road_id] == road_df['to'][next_road]:
                            if road_status['cap2'][next_road] - road_status['used2'][next_road] > 2:
                                # 下一条路满足进入要求，进入下一条路
                                road_status.at[next_road, 'cars2'].update({car: next_posi})  # 为下一条路添加车信息
                                road_status.loc[next_road, 'used2'] += 1
                                road_status.at[road_id, 'cars2'].pop(car)  # 删除原来路的车信息
                                road_status.loc[road_id, 'used2'] -= 1

                                car_status.loc[car, 'status'] = next_road  # 更新车辆状态
                            else:
                                # 下一条路没有空位，走到该条路末端
                                road_status.at[road_id, 'cars2'].update({car: road_len})
                                # TODO： 考虑重规划路径


        ## 记录改时间片出发的车辆，以及路径信息（可能存在路径更新的车辆）
        # print(car_status)
        # print(road_status)
        #### 至此完成一个时间片的发车和状态更新
        # 发车池中没有车可发，且所有车均到达目的地时，时间片结束

        ### TODO： 添加系统状态监测和系统负载计算
        ## function


        ## 时间片终止条件：所有车到达终点
        if sum((list(car_status['status'] == -1))) == len(car_status['status']):
            print("all cars have arrived to the end and spend time is:", i)
            break

        if i > 1000:
            print("cannot arrive within 1000 time slice.")
            break
        # sys.exit()
    return time_final
## TODO:优化程序运行速度，可能是对Dataframe的深拷贝导致耗时严重问题

## 测试结果
# path由get_all_paths_with_hc获得
# config：  car_num =20 所有车到达目的地:85  实际耗时：3s
# config0:  car_num = 20 所有车到达目的地：958  实际耗时：5min左右
# config0:  car_num = 20 所有车到达目的地：913  实际耗时：5min34s

# path由get_all_paths_with_hc获得
# config：  car_num =20 所有车到达目的地:55  实际运行耗时：1s
# config0:  car_num = 20 所有车到达目的地：709  实际运行耗时：2min44s左右
# config0:  car_num = 20 所有车到达目的地：709  实际运行耗时：2min40s左右
# config0:  car_num = 30 所有车到达目的地：>1000  实际运行耗时：13min54s左右
# to be continued......


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
    # pa = get_all_paths_with_hc(al, road_df, car_df['id'], car_df['from'], car_df['to'])
    pa = get_all_cars_paths(al, car_df['id'], car_df['from'], car_df['to'], use_networkx=False)
    super_time_plan(pa, car_df, road_df, cross_df)
    print('end')


