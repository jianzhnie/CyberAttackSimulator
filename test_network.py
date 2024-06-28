import time

import networkx as nx

if __name__ == '__main__':
    G = nx.wheel_graph(10)
    start_time = time.time()
    # edges = G.edges
    # end_time = time.time()
    # print(f"Time to list all edges: {end_time - start_time}")
    # adj_mat = nx.to_numpy_array(G)
    # end_time = time.time()
    # print(f"Time to get adj matrix: {end_time - start_time}")
    adj_mat = nx.to_scipy_sparse_array(G)
    print(adj_mat)
    end_time = time.time()
    print(f'Time to get adj matrix: {end_time - start_time}')
