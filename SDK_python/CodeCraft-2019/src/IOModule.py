import pandas


def read_from_txt(path_, type_= None):
    """
    :param path_: txt file path
           type_: not use
    :return: pandas DataFrame
    """
    # read txt file, splice number
    df = pandas.read_csv(path_, sep='[^\\-|0-9]+', header=None, skiprows=1, engine='python')  # 正则表达式记得转义

    # delete NaN columns--> first column and last column
    df.drop(columns=[0, df.shape[1]-1], inplace=True)

    if path_.find('road') > 0: # road(id,length,speed,channel,from,to,isDuplex)
        df.set_axis(['id', 'length', 'speed', 'channel', 'from', 'to', 'isDuplex'], axis='columns', inplace=True)
        df.set_index(df['id'], inplace=True)
        df.rename_axis('index', inplace=True)

    elif path_.find('car') > 0: # car(id,from,to,speed,planTime)
        df.set_axis(['id',  'from', 'to', 'speed', 'planTime'], axis='columns', inplace=True)
        df.set_index(df['id'], inplace=True)
        df.rename_axis('index', inplace=True)

    elif path_.find('cross') > 0: # cross(id,roadId,roadId,roadId,roadId)
        df.set_axis(['id', 'roadID1', 'roadID2', 'roadID3', 'roadID4'], axis='columns', inplace=True)
        df.set_index(df['id'], inplace=True)
        df.rename_axis('index', inplace=True)

    else:
        raise Exception("input txt file error")

    return df


def read_car_from_txt(path_):
    df = pandas.read_csv(path_, sep='[^\\-|0-9]+', header=None, skiprows=1, engine='python')

    # delete NaN columns--> first column and last column
    df.drop(columns=[0, df.shape[1] - 1], inplace=True)

    df.set_axis(['id', 'from', 'to', 'speed', 'planTime'], axis='columns', inplace=True)
    df.set_index(df['id'], inplace=True)
    df.rename_axis('index', inplace=True)

    return df


def read_road_from_txt(path_):
    df = pandas.read_csv(path_, sep='[^\\-|0-9]+', header=None, skiprows=1, engine='python')

    # delete NaN columns--> first column and last column
    df.drop(columns=[0, df.shape[1] - 1], inplace=True)

    df.set_axis(['id', 'length', 'speed', 'channel', 'from', 'to', 'isDuplex'], axis='columns', inplace=True)
    df.set_index(df['id'], inplace=True)
    df.rename_axis('index', inplace=True)

    return df


def read_cross_from_txt(path_):
    df = pandas.read_csv(path_, sep='[^\\-|0-9]+', header=None, skiprows=1, engine='python')

    # delete NaN columns--> first column and last column
    df.drop(columns=[0, df.shape[1] - 1], inplace=True)

    df.set_axis(['id', 'roadID1', 'roadID2', 'roadID3', 'roadID4'], axis='columns', inplace=True)
    df.set_index(df['id'], inplace=True)
    df.rename_axis('index', inplace=True)

    return df


def write_answer2file(txt_path, answer_list):
    """
    :brief: write data to answer.txt, data pattern {carID, startTime, path series}
    :param txt_path: 要写入文件的路径
    :param answer_list: answer 2维数组，数据格式例如:[[100, 1, 203, 303], [101, 3, 213, 303, 304, 432]]
    :return:
    """
    with open(txt_path, 'w') as output:
        output.write('#carID, StartTime, RoadID...\n')
        for answer in answer_list:
            answer_str = "".join([str(x)+',' for x in answer])  # 将int list型的answer转换为str类型，并以逗号隔开
            output.writelines('(' + answer_str[:-1] + ')' + '\n')  # answer_str[:-1] 最后的逗号不写入


if __name__ == "__main__":
    rpath = '/home/srn/SRn/Competition/HuaWei/hw_cc/SDK_python/CodeCraft-2019/config0'
    path = rpath + '/cross.txt'
    path1 = rpath + '/road.txt'
    path2 = rpath + '/car.txt'
    path3 = rpath + '/answer.txt'

    cross_df = read_from_txt(path)
    print(cross_df.head())
    print(cross_df.shape)

    road_df1 = read_from_txt(path1)
    print(road_df1.head())
    print(road_df1.shape)

    car_df = read_from_txt(path2)
    print(car_df.head())
    print(car_df.shape)
