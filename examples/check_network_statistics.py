"""Generate some networks statistics."""

import os

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd


def process_graph_statistics(graph) -> None:
    # Calculate network statistics
    print('---------------------------')
    # Calculate the number of nodes
    print('number of nodes:', graph.number_of_nodes())
    # Calculate the number of edges
    print('number of edges:', graph.size())
    # Calculate the clustering
    clust = nx.clustering(graph)

    # Calculate the number of clusters
    num_clusters = np.sum([clust[key] for key in clust.keys()])
    print(f'{num_clusters} total number of clusters')
    print('---------------------------')
    # Calcualte the average clustering of the graph
    avg_clustering = nx.average_clustering(graph)
    print(f'{avg_clustering} average clustering')
    print('---------------------------')
    # Calculate the number of triangles present
    triangls = nx.triangles(graph)
    # Calculate the total number of triangles
    num_triangles = np.sum([triangls[key] for key in triangls.keys()])
    print(f'{num_triangles} total number of triangles')
    print('---------------------------')


if __name__ == '__main__':
    # staging
    current_dir = os.getcwd()
    network_dir = os.path.join(current_dir, 'work_dir', 'networks')
    # load the various files
    files = os.listdir(network_dir)
    # loop over the files
    for file_name in files:
        ifile = os.path.join(network_dir, file_name)
        num_triangles, num_clusters = 0, 0
        matrix = np.load(ifile, allow_pickle=True)['matrix']
        df = pd.DataFrame(matrix)
        graph = nx.from_pandas_adjacency(df)
        process_graph_statistics(graph)
        # seed the position for replicability
        my_pos = nx.spring_layout(graph, seed=99)
        graph_name = file_name.replace('npz', 'png')
        figure_name = os.path.join(network_dir, graph_name)
        plt.figure(figsize=(12, 9), dpi=150)
        nx.draw(
            graph,
            with_labels=True,
            node_size=300,
            node_shape='8',
            pos=my_pos,
            verticalalignment='center',
            horizontalalignment='left',
            clip_on=False,
            font_weight='normal',
            linewidths=0.5,
            alpha=1,
            width=0.8,
        )
        plt.title('Example graph')
        plt.axis('off')
        plt.show()
        # save the figure
        plt.savefig(figure_name)
