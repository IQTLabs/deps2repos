"""Create and analyze graph from csv file. Intended for use with Github contributors and projects but will work with
any arbitrary nodes and edges"""

import collections
import itertools
import os
import time
import argparse
import json
import networkx as nx
from pathlib import Path


def form_graph(input_file, node_index, edge_index):
    """Create a networkx graph from an input csv file.

    Reads csv file with one connection per line (such as github contributor and the project they worked on) and returns
    graph linking those elements
    Example input format:

    project,contributor,other_info,more_info
    project,contributor2,other_info,more_info
    project2,contributor,other_info,more_info
    project2,contributor3,other_info,more_info

    Args:
        input_file - a csv file that contains information for graph, such as github contributors and projects
        node_index - csv index to be used for nodes
        edge_index - csv index to be used for edges

    Returns:
        G - a networkx graph
    """

    edges = collections.defaultdict(list)

    G = nx.Graph()

    # Read import file from GitGeo:
    with open(input_file, "r") as f:

        # Skip first line
        next(f)

        for line in f:
            info = line.strip().split(",")
            edges[info[edge_index]].append(info[node_index])

    for i in edges:
        edge_combinations = list(itertools.combinations(edges[i], 2))
        for edge in edge_combinations:
            if G.has_edge(edge[0], edge[1]):
                G[edge[0]][edge[1]]["weight"] += 1
            else:
                G.add_edge(edge[0], edge[1], weight=1)

    return G


def analyze(graph):
    """Analyzes an input networkx graph.

    Calculations done:
    node_num - total number of nodes in graph
    edge_num - total number of edges in graph
    avg_degree - average of number of edges that are incident to all nodes
    density - ratio of the number of edges with respect to the maximum possible edges
    assortativity - the tendency for nodes of high degree in a graph to be connected to high degree nodes
    average_clustering - a measure of the degree to which nodes in a graph tend to cluster together
    page_rank - results of Google PageRank algorithm

    Args:
        graph - networkx graph with weight="weight"

    Returns:
        results - a dictionary with all finished calculations
    """

    results = {}

    results["assortativity"] = nx.degree_assortativity_coefficient(
        graph, weight="weight"
    )
    results["average_clustering"] = nx.algorithms.cluster.average_clustering(
        graph, weight="weight"
    )
    degree = graph.degree(weight="weight")
    results["avg_degree"] = sum(degree.values()) / len(degree)
    results["density"] = nx.density(graph)
    results["edge_num"] = len(graph.edges())
    results["node_num"] = len(graph.node)
    ranks = nx.algorithms.link_analysis.pagerank_alg.pagerank(graph)

    # Sort dict based on rank
    results["page_rank"] = {
        key: value
        for key, value in sorted(ranks.items(), reverse=True, key=lambda item: item[1])
    }

    return results


def write_graph_results(filename, results):
    """Write dictionary results to json file.

    Args:
        filename - filename base for output file. Can be basename or full path (path will be trimmed)
        results - dictionary of analysis results

    Returns:
        null
    """

    timestamp = time.strftime("%Y%m%d-%H%M%S")
    basename = os.path.basename(filename)
    basename = os.path.splitext(basename)[0]

    filename = Path.cwd() / "results"
    filename.mkdir(exist_ok=True)
    filename /= basename + "_" + timestamp + ".json"

    with open(filename, "w") as f:
        json.dump(results, f, indent=4)


def parse_command_line_arguments():
    """Parse command line arguments with argparse."""
    parser = argparse.ArgumentParser(
        description="Convert csv file into nodes and edges, such as github contributors and projects",
        epilog="For help with this program, contact John Speed at jmeyers@iqt.org.",
    )
    parser.add_argument(
        "--node-index",
        default=1,
        type=int,
        help="Index of nodes in csv file",
    )
    parser.add_argument(
        "--edge-index",
        default=0,
        type=int,
        help="Index of edges in csv file",
    )
    parser.add_argument(
        "--filepath",
        help="Filepath to csv file for analysis",
    )
    parser.add_argument(
        "--filename",
        default=None,
        help="Base file name for analysis results (timestamp will be added)",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_command_line_arguments()

    graph = form_graph(args.filepath, args.node_index, args.edge_index)
    results = analyze(graph)
    filename = args.filename or args.filepath
    write_graph_results(filename, results)
