import random
import numpy as np
from  tqdm import tqdm

def get_time_plan4(car_df):
    '''
    分批出发，凑够一定数量的车再发车，可能某个时刻不发车
    :param car_df:
    :return:
    基本Dijkstra
    13-1775
    加hc
    cut_channel_level=1
    13-1918 14-1806 15-1732 16-1609 17-1579 18-1611
    cut_channel_level=2
    13-1775 14-1663 15-1585 16-1535 17-1581 18-1608
    '''
    time_plans = {}
    controlcarnum = 18

    # 根据每辆车的计划出发时间进行升序排列
    #car_df_sort = car_df.sort_values(by='planTime', axis=0, ascending=True)
    # 根据每辆车的计划出发时间进行升序排列 速度降序排列
    car_df_sort = car_df.sort_values(by=['planTime', 'speed'], axis=0, ascending=[True, False])

    i = 1
    tempsave = []
    time_last = -1
    idtime = -1
    for carID, pT in zip(car_df_sort['id'], car_df_sort['planTime']):
        tempsave.append(carID)
        if (i % controlcarnum) == 0:
            if pT <= time_last:
                idtime = time_last + 1
            else:
                idtime = pT

            for id in tempsave:
                time_plans[id] = [id, idtime]
                tempsave = []

            time_last = idtime

        i += 1

    for id in tempsave:   #将最后剩下的添加进来
        time_plans[id] = [id, time_last+1]

    return time_plans


def get_time_plan6(car_df):
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
    car_df_sort = car_df.sort_values(by=['planTime', 'speed'], axis=0, ascending=[True, False])
    # print(car_df_sort.head(50))

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

    # 发车数量控制2
    # 正弦发车
    # 最优参数 controlcarnum = 23 change = 3 interval = int(carsum/9)
    # controlcarnum = 20 18 m1 failed   m2 随controlcarnum减小而增大
    # controlcarnum = 26 剪枝参数cut_channel_level=1, cut_speed_level=1 m1:608 m2:734
    # controlcarnum = 30 剪枝参数cut_channel_level=1, cut_speed_level=1 m1:failed m2:failed

    # controlcarnum = 28 剪枝参数cut_channel_level=1, cut_speed_level=1 i > 350 m1:failed m2:748     change:4 m1 failed m2 736
    # controlcarnum = 28 剪枝参数cut_channel_level=1, cut_speed_level=1 i > 550 m1:691 m2:938
    # controlcarnum = 29 剪枝参数cut_channel_level=1, cut_speed_level=1 i > 550 m1:631 m2:failed
    # controlcarnum = 29 剪枝参数cut_channel_level=1, cut_speed_level=1 i > 450 m1:732 m2:failed
    # controlcarnum = 29 剪枝参数cut_channel_level=2, cut_speed_level=1 i > 450 m1:failed m2:failed
    # controlcarnum = 29 剪枝参数cut_channel_level=2, cut_speed_level=1 i > 750 m1:732 m2:failed

    # controlcarnum = 26 剪枝参数cut_channel_level=2, cut_speed_level=1 i > 750 m1:failed m2:565
    # controlcarnum = 26 剪枝参数cut_channel_level=2, cut_speed_level=1 i > 450 m1:failed m2:failed
    # controlcarnum = 26 剪枝参数cut_channel_level=2, cut_speed_level=1 i > 850 m1:failed m2:531
    # controlcarnum = 26 剪枝参数cut_channel_level=2, cut_speed_level=1 i > 950 m1:failed m2:531

    # controlcarnum = 26 interval = int(carsum/10) 剪枝参数cut_channel_level=2, cut_speed_level=1 i > 950 m1:562 m2:541  ---> best
    # controlcarnum = 27 interval = int(carsum/10) 剪枝参数cut_channel_level=2, cut_speed_level=1 i > 950 m1:failed m2:522
    # controlcarnum = 27 interval = int(carsum/11) 剪枝参数cut_channel_level=2, cut_speed_level=1 i > 950 m1:failed m2:527
    # controlcarnum = 27 interval = int(carsum/11) 剪枝参数cut_channel_level=2, cut_speed_level=1 i > 650 m1:failed m2:528
    # controlcarnum = 27 interval = int(carsum/11) 剪枝参数cut_channel_level=2, cut_speed_level=1 i > 450 m1:failed m2:failed
    # controlcarnum = 27 interval = int(carsum/12) 剪枝参数cut_channel_level=2, cut_speed_level=1 i > 450 m1:failed m2:failed
    # controlcarnum = 27 interval = int(carsum/13) 剪枝参数cut_channel_level=2, cut_speed_level=1 i > 450 m1:failed m2:550
    # controlcarnum = 27 interval = int(carsum/13) 剪枝参数cut_channel_level=2, cut_speed_level=1 i > 850 m1:failed m2:530
    # controlcarnum = 26 interval = int(carsum/13) 剪枝参数cut_channel_level=2, cut_speed_level=1 i > 850 m1:failed m2:550
    # controlcarnum = 26 interval = int(carsum/11) 剪枝参数cut_channel_level=2, cut_speed_level=1 i > 850 m1:failed m2:544
    # controlcarnum = 26 interval = int(carsum/11) 剪枝参数cut_channel_level=2, cut_speed_level=1 i > 1000 m1:541 m2:544 ---> best best
    # controlcarnum = 26 interval = int(carsum/11) 剪枝参数cut_channel_level=2, cut_speed_level=1 i > 1200 m1:failed m2:544
    # controlcarnum = 26 interval = int(carsum/12) 剪枝参数cut_channel_level=2, cut_speed_level=1 i > 1200 m1:563 m2:547 --> succeed
    # controlcarnum = 27 interval = int(carsum/12) 剪枝参数cut_channel_level=2, cut_speed_level=1 i > 1200 m1:failed m2:536


    # controlcarnum = 27 剪枝参数cut_channel_level=1, cut_speed_level=1 i > 350 m1:590 m2:754


    controlcarnum = 26
    change = 3
    interval = int(carsum/11)
    control = controlcarnum+int(change * np.sin(i*(2 * np.pi)/interval))

    print("get_time_plan6:")
    for carID, pT in tqdm(zip(car_df_sort['id'], car_df_sort['planTime'])):
        tempsave.append(carID)
        if (i % control) == 0:
            if pT <= time_last:
                idtime = time_last + 1
            else:
                idtime = pT

            for id in tempsave:
                time_plans[id] = [id, idtime]
                car_df_sort['planTime'][id] = idtime  #记录实际安排的出发时间
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
        car_df_sort['planTime'][id] = time_last+1   #记录实际安排的出发时间

    # print(car_df_sort.head(50))

    return time_plans, car_df_sort


def get_time_plan5(car_df):
    '''
    分批出发，某一时刻发车数量多于一定数量顺延
    :param car_df:
    :return:
    基本Dijkstra
    10-2222 11-2036 12-失败932  13-失败867
    加hp
    '''
    time_plans = {}
    controlcarnum = 16

    # 根据每辆车的计划出发时间进行升序排列
    car_df_sort = car_df.sort_values(by='planTime', axis=0, ascending=True)
    # 根据每辆车的计划出发时间进行升序排列 速度降序排列
    #car_df_sort = car_df.sort_values(by=['planTime', 'speed'], axis=0, ascending=[True , False])

    i = 1
    timemax_last = -1
    idtime = -1
    for carID, pT in zip(car_df_sort['id'], car_df_sort['planTime']):
        idtime = max(timemax_last,pT)
        time_plans[carID] = [carID, idtime]
        if idtime > timemax_last:
            timemax_last=idtime
        else:
            pass

        if (i % controlcarnum) == 0:
            timemax_last += 1
        i += 1

    return time_plans


def weight_func2(road_l, road_mv,road_channel):
    #考虑长度/速度/车道数
    weight = road_l / (road_mv*road_channel)
    return weight


def weight_func3(road_l, road_mv,road_channel,isDuplex):
    #考虑长度/速度/车道数/(1+isDuplex)
    weight = road_l / (road_mv*road_channel*(1.05+isDuplex))
    return weight

def build_adjacency_list2(cross_df, road_df):
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
                if (next_cross_id == cross_id) and (road_df['isDuplex'][road] == 1):
                    next_cross_id = road_df['from'][road]
                # 设置该条边的权重
                # weight = weight_func(road_df['length'][road], road_df['speed'][road])
                # weight = weight_func2(road_df['length'][road], road_df['speed'][road],road_df['channel'][road])
                weight = weight_func3(road_df['length'][road], road_df['speed'][road], road_df['channel'][road],
                                      road_df['isDuplex'][road])

                # 将数据存入嵌套字典
                if adjacency_list.__contains__(cross_id):
                    adjacency_list[cross_id][next_cross_id] = [road, weight]
                else:
                    adjacency_list[cross_id] = {next_cross_id: [road, weight]}

    return adjacency_list
