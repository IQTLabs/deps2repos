import plotly.graph_objects as go

import collections
import itertools
import networkx as nx


def random_plot():
    G = nx.random_geometric_graph(200, 0.125)

    # Create edges
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = G.node[edge[0]]["pos"]
        x1, y1 = G.node[edge[1]]["pos"]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        line=dict(width=0.5, color="#888"),
        hoverinfo="none",
        mode="lines",
    )

    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = G.node[node]["pos"]
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers",
        hoverinfo="text",
        marker=dict(
            showscale=True,
            # colorscale options
            #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
            #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
            #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
            colorscale="YlGnBu",
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title="Node Connections",
                xanchor="left",
                titleside="right",
            ),
            line_width=2,
        ),
    )

    # Color based on connection strength
    node_adjacencies = []
    node_text = []
    i = G.adj
    for node, adjacencies in G.adj.items():
        node_adjacencies.append(len(adjacencies))
        node_text.append("# of connections: " + str(len(adjacencies)))

    node_trace.marker.color = node_adjacencies
    node_trace.text = node_text

    # Create graph
    fig = go.Figure(
        data=[edge_trace, node_trace],
        layout=go.Layout(
            title="<br>Network graph made with Python",
            titlefont_size=16,
            showlegend=False,
            hovermode="closest",
            margin=dict(b=20, l=5, r=5, t=40),
            annotations=[
                dict(
                    text="Python code: <a href='https://plotly.com/ipython-notebooks/network-graphs/'> https://plotly.com/ipython-notebooks/network-graphs/</a>",
                    showarrow=False,
                    xref="paper",
                    yref="paper",
                    x=0.005,
                    y=-0.002,
                )
            ],
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        ),
    )
    fig.show()


def form_graph(input_file, node_index, edge_index):

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

    results = {}

    results["node_num"] = len(graph.node)
    results["edge_num"] = len(graph.edges())
    degree = graph.degree(weight="weight")
    results["avg_degree"] = sum(degree.values()) / len(degree)
    results["density"] = nx.density(graph)
    results["assortativity"] = nx.degree_assortativity_coefficient(
        graph, weight="weight"
    )
    results["average_clustering"] = nx.algorithms.cluster.average_clustering(
        graph, weight="weight"
    )

    return results


def save_graph_results(results, file_path="graph.txt"):
    with open(file_path, "w") as f:
        for result in results:
            f.write(f"{result}: {results[result]}\n")
            print(f"{result}: {results[result]}")


if __name__ == "__main__":
    project_index = 0
    contributor_index = 1
    location_index = 2
    country_index = 3
    # form_graph("results/contributors-trimmed.csv", contributor_index, project_index)
    # form_graph("results/contributors-trimmed.csv", project_index, contributor_index)
    graph = form_graph("results/contributors.csv", contributor_index, project_index)
    results = analyze(graph)
    save_graph_results(results)
