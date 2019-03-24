# from pqdict import PQDict
from dijkstra.pqdict import PQDict


def dijkstra(G, start, end=None):
    inf = float('inf')
    D = {start: 0}          # mapping of nodes to their dist from start
    Q = PQDict(D)           # priority queue for tracking min shortest path
    P = {}                  # mapping of nodes to their direct predecessors
    U = set(G.keys())       # unexplored nodes

    while U:                                    # nodes yet to explore
        (v, d) = Q.popitem()                    # node w/ min dist d on frontier
        D[v] = d                                # est dijkstra greedy score
        U.remove(v)                             # remove from unexplored
        if v == end: break

        # now consider the edges from v with an unexplored head -
        # we may need to update the dist of unexplored successors 
        for w in G[v]:                          # successors to v
            if w in U:                          # then w is a frontier node
                d = D[v] + G[v][w]              # dgs: dist of start -> v -> w
                if d < Q.get(w, inf):
                    Q[w] = d                    # set/update dgs
                    P[w] = v                    # set/update predecessor

    return D, P


def shortest_path(G, start, end):
    dist, pred = dijkstra(G, start, end)
    v = end
    path = [v]
    while v != start:
        v = pred[v]
        path.append(v)        
    path.reverse()
    return path


if __name__ == '__main__':

    graph = {'a': {'b': 1},
             'b': {'c': 2, 'b': 5},
             'c': {'d': 1},
             'd': {}}

    # get shortest path distances to each node in `graph` from `a`
    dist, pred = dijkstra(graph, 'a')
    assert dist == {'a': 0, 'c': 3, 'b': 1, 'd': 4}     # min dist from `a`
    assert pred == {'b': 'a', 'c': 'b', 'd': 'c'}       # direct predecessors
    assert shortest_path(graph, 'a', 'd') == list('abcd')

