import pandas
import numpy as np
from util import build_adjacency_list, adj_list_visualize, get_path, build_ad_list_without_edge_id
from dijkstra.dijkstra import shortest_path, dijkstra


def read_from_txt(path_, type_= None):
    """
    :param path_: txt file path
           type_: not use
    :return: pandas DataFrame
    """
    # read txt file, splice number
    df = pandas.read_csv(path_, sep='[^\-|0-9]+', header=None, skiprows=1, engine='python')

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


def write_to_anser(path_):
    """
    :brief: write data to answer.txt, data pattern {carID, startTime, path series}
    :param path_:
    :return:
    """

    pass


if __name__ == "__main__":
    path = '/home/srn/SRn/Competition/HuaWei/hw_cc/SDK_python/CodeCraft-2019' + '/config/cross.txt'
    path1 =  '/home/srn/SRn/Competition/HuaWei/hw_cc/SDK_python/CodeCraft-2019' + '/config/road.txt'
    df = read_from_txt(path)

    print(df.head())
    print(df.shape)

    df1 = read_from_txt(path1)
    print(df1.head())
    print(df1.shape)
    al = build_adjacency_list(df, df1)
    print(al)

    adw = build_ad_list_without_edge_id(df, df1)
    print(adw)

    # 最短路径搜索
    p = get_path(adw, 1, 20)
    print('shortest path is:', p)

    # 最短路径搜索
    p1 = shortest_path(adw, 1, 20)
    print(p1)

    # 可视化有向图
    adj_list_visualize(al)



