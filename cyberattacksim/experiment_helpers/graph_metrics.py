"""Collection of functions to help generating metrics and summary statistics
for networkx graphs."""

import copy
import statistics as stats
from typing import Callable, List

import networkx as nx
import numpy as np
from tabulate import tabulate

from cyberattacksim.experiment_helpers.constants import \
    STANDARD_GRAPH_METRIC_HEADERS


# 这段代码定义了一些函数，用于计算图的各种网络指标，并生成和打印相关的统计信息。
def geometric_mean_overflow(input_list: List) -> float:
    """Calculate the geometric mean accounting for the potential of overflow
    through using logs.

    计算输入列表的几何平均数，并处理可能出现的溢出问题。
    当处理较大的数值时，直接计算几何平均可能导致溢出，通过对数的形式可以有效避免这个问题。

    Args:
        input_list: A list of values

    Returns:
        Geometric mean as a float

    Note: There is actually a function included in the 'statistics'
    python module that does this but is only available in python 3.8 onwards
    """
    a = np.log(input_list)
    return np.exp(a.mean())


def flatten_list(list_input: list) -> list:
    """Take a list of lists and flattens them into a single list.
    将一个嵌套的列表（即列表的列表）展平成一个单一的列表。

    工作原理:
        使用列表推导式遍历嵌套列表中的每个子列表，并将其元素直接添加到结果列表中。

    Args:
        list_input: The input list of lists to be processed

    Returns:
        A single list containing all elements
    """
    return [item for sublist in list_input for item in sublist]


def get_assortativity_metrics(graph: nx.Graph):
    """Get assortativity metrics for an input graph using networkx's in-built
    algorithms. 获取输入图的同配性度量，即节点连接的倾向性，常用于社交网络分析中。

    工作原理:
        使用 NetworkX 库提供的 nx.degree_assortativity_coefficient() 和 nx.degree_pearson_correlation_coefficient() 计算图的度同配性系数和皮尔逊系数。
        返回一个包含两个系数的元组。

    Args:
        graph: A networkx graph

    Returns:
        A two-tuple with the metrics
    """
    degree_assortativity_coef = nx.degree_assortativity_coefficient(graph)
    degree_pearson_coef = nx.degree_pearson_correlation_coefficient(graph)

    return (degree_assortativity_coef, degree_pearson_coef)


def get_func_summary_statistics(func: Callable) -> list:
    """Generate a list of summary statistics based on the output of a networkx
    in-build algorithm. 基于 NetworkX 内置算法的输出生成一组统计摘要。

    工作原理:
        检查 func 的输出是否为字典类型，如果是，则提取字典的值作为指标列表。
        对这些指标计算算术平均数、几何平均数、调和平均数、标准差、方差和中位数。
        返回这些统计值的列表。

    Args:
        func: A networkx algorithm function

    Returns:
        A list containing:
            - Arithmetic Mean
            - Geometric Mean
            - Harmonic Mean
            - Standard Deviation
            - Variance
            - Median

    Example:

        > generate_summary_statistics(nx.degree_centrality(graph))
        > (3.3095238095238098, 2.5333333333333337, 2.9015675801088014, 1.9824913893491538, 2.620181405895692, 3.0)
    """
    metric_dict = func

    if isinstance(metric_dict, dict):
        metrics = list(metric_dict.values())
    else:
        raise TypeError(
            f'Expected an input type of dict. Got {type(metric_dict)}')

    mean = stats.mean(metrics)
    geomean = geometric_mean_overflow(metrics)
    harmonic_mean = stats.harmonic_mean(metrics)
    stdev = stats.stdev(metrics)
    variance = stats.pvariance(metrics)
    median = stats.median(metrics)

    return [mean, harmonic_mean, geomean, stdev, variance, median]


def get_graph_metric_bundle(graph: nx.Graph) -> List[List]:
    """Generate a graph metric bundle. 生成图的度量包，包含多个 NetworkX 算法的摘要统计信息。

    工作原理:

        首先，深拷贝图的边和节点，然后清空图并用深拷贝的数据重新更新图的结构。
        使用一系列的 NetworkX 算法（如平均度连接性、接近中心性、度中心性、特征向量中心性和传递性中介中心性）计算图的相关指标。
        调用 get_func_summary_statistics 生成这些指标的统计摘要，将结果保存在 metric_outputs 列表中。

    A graph metric bundle includes the summary statistics for a
    collection of networkx in-built algorithms.

    Algorithms used:
        - Average Degree Connectivity
        - Closeness Centrality
        - Degree Centrality
        - Eigenvector Centrality
        - Communicability Between-ness Centrality

    Args:
        graph: A networkx graph

    Returns:
        A list of lists containing the metrics
    """
    # Force an update to the adjacency lookup:

    edges = copy.deepcopy(graph.edges)
    nodes = copy.deepcopy(graph.nodes)
    graph.clear()
    graph.update(edges=edges, nodes=nodes)

    funcs_to_process = [
        nx.average_degree_connectivity(graph),
        nx.closeness_centrality(graph),
        nx.degree_centrality(graph),
        nx.eigenvector_centrality(graph),
        nx.communicability_betweenness_centrality(graph),
    ]

    func_names = [
        'Avg Degree Connectivity',
        'Closeness Centrality',
        'Degree Centrality',
        'Eigenvector Centrality',
        'Communicability Between-ness Centrality',
    ]

    metric_outputs = []
    for func, name in zip(funcs_to_process, func_names):
        output = get_func_summary_statistics(func)
        output.insert(0, name)
        metric_outputs.append(output)

    return metric_outputs


def pprint_metric_table(metric_output: List[List], headers=None):
    """Pretty prints graph metrics to the terminal using the tabulate module.
    使用 tabulate 模块将图的度量指标以表格形式打印到终端。

    Args:
        metric_output: A list of lists containing the values to be printed.
        headers: A list of heading names (optional)

    Returns:
        A formatted table to terminal
    """
    if headers:
        print(tabulate(metric_output, headers))
    else:
        print(tabulate(metric_output, headers=STANDARD_GRAPH_METRIC_HEADERS))
