"""Function to call and generate networks to re-use it across different tests
and trainings."""

import os
import pickle
import sys
from typing import Any, Dict, Tuple

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd

sys.path.append(os.getcwd())
from nasimulator.networks.network_creator import create_mesh


def dump_pkl(obj: Any, name: str) -> None:
    """Simple function to dump objects into pickle files.

    Args:
        obj (Any): The object to be pickled.
        name (str): The name of the file where the object will be stored.
                    If the name does not end with ".pkl", it will be appended.

    Returns:
        None
    """
    if not name.endswith('.pkl'):
        name += '.pkl'

    with open(name, 'wb') as file:
        pickle.dump(obj, file)


def load_pkl(name: str) -> Any:
    """Function to load objects from pickle files.

    Args:
        name (str): The name of the pickle file to load.
                    If the name does not end with ".pkl", it will be appended.

    Returns:
        Any: The object loaded from the pickle file.
    """
    if not name.endswith('.pkl'):
        name += '.pkl'

    with open(name, 'rb') as file:
        return pickle.load(file)


def create_network(
    n_nodes: int,
    connectivity: float,
    output_dir: str,
    filename: str,
    save_matrix: bool = True,
    save_graph: bool = False,
) -> Tuple[np.ndarray, Dict]:
    """Function to create a network and optionally save it for reuse.

    Args:
        n_nodes (int): Number of nodes in the network.
        connectivity (float): Percentage of edges connecting the nodes.
        output_dir (str): Directory to save the network files.
        filename (str): Base name for saving the network files.
        save_matrix (bool): Whether to save the matrix and edges as a .npz file.
        save_graph (bool): Whether to save the graph as a .npz file.

    Returns:
        Tuple[np.ndarray, Dict]: A tuple containing the adjacency matrix and node positions.
    """

    # Use the yawning titan generator to create the mesh of given size
    matrix, positions = create_mesh(size=n_nodes, connectivity=connectivity)

    nodes = [str(i) for i in range(n_nodes)]

    # Create the DataFrame for the graph
    graph_df = pd.DataFrame(matrix, index=nodes, columns=nodes)

    # Create a graph for visualization
    graph = nx.from_pandas_adjacency(graph_df)

    # Check if the filename has the right extension
    if not filename.endswith('.npz'):
        filename += '.npz'
    filen = os.path.join(output_dir, filename)

    # Save the matrix and positions as .npz file if save_matrix is True
    if save_matrix:
        np.savez(filen, matrix=matrix, positions=positions)

    # Save the graph as .npz file if save_graph is True
    if save_graph:
        graph_filename = os.path.join(output_dir,
                                      filename.replace('.npz', '_graph.npz'))
        np.savez(graph_filename, graph=graph)

    return matrix, positions


def main():
    # example running
    current_dir = os.getcwd()
    outdir = os.path.join(current_dir, 'work_dir', 'test_networks')

    # example nodes and connectivity
    n_nodes_list = [18, 50, 100]
    connectivity = 0.4

    for n_nodes in n_nodes_list:
        # showing the example
        file_name = str(n_nodes) + '_nodes_network'

        matrix, _ = create_network(
            n_nodes,
            connectivity,
            output_dir=outdir,
            filename=file_name,
            save_matrix=True,
        )
        # the positions are not relevant in this specific example

        nodes = [str(i) for i in range(n_nodes)]

        graph_df = pd.DataFrame(matrix, index=nodes, columns=nodes)

        # generate the graph using the adjacency matrix
        graph = nx.from_pandas_adjacency(graph_df)

        # seed the position for replicability
        my_pos = nx.spring_layout(graph, seed=99)

        graph_name = str(n_nodes) + '_nodes_graph.png'
        figure_name = os.path.join(outdir, graph_name)
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
        # plt.tight_layout() # sometimes it complains
        plt.show()
        # save the figure
        plt.savefig(figure_name)


if __name__ == '__main__':
    main()
