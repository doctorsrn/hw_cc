# -*- coding: utf-8 -*-

## 表示无穷大
INF_val = 9999


def init_Floyd(adl):
    path_map = {}
    for crossID in adl.keys():
        path_map[crossID] = {}
        for neighborcross in adl[crossID]:
            path_map[crossID][neighborcross] = neighborcross

    adl_extend = {}
    for crossID in adl.keys():
        adl_extend[crossID] = {}
        for neighborcross in adl.keys():
            if neighborcross in adl[crossID]:
                adl_extend[crossID][neighborcross] = adl[crossID][neighborcross][1]
            else:
                adl_extend[crossID][neighborcross] = INF_val

    for k in adl.keys():
        for i in adl.keys():
            for j in adl.keys():
                tmp = adl_extend[i][k] + adl_extend[k][j]
                if adl_extend[i][j] > tmp:
                    adl_extend[i][j] = tmp
                    path_map[i][j] = path_map[i][k]


    return path_map


def get_floyd_path(path_map,from_node, to_node):
    node_list = []
    temp_node = from_node
    obj_node = to_node
    node_list.append(from_node)
    while True:
        node_list.append(path_map[temp_node][obj_node])
        temp_node = path_map[temp_node][obj_node]
        if temp_node == obj_node:
            break

    return node_list
