import networkx as nx
import json
import matplotlib.pyplot as plt
import numpy as np
import sys



def read_jsonl(filename) -> list:
    data = []
    with open(filename, 'r', encoding='utf-8') as inf:
        for line in inf:
            data.append(json.loads(line))

    return data


def generate_graph(input_data):
    g = nx.DiGraph()
    for line in input_data:
        source, target, weight = line['source_pos'], line['target_pos'], line[
            'weight']

        # If the edge already exists, sum the weights --> so that there are no duplicate edges
        if g.has_edge(source, target):
            g[source][target]['weight'] += weight
        else:
            g.add_edge(source, target, weight=weight)

    return g
def analyze_graph(graph):
    # 1.) degree and centrality
    #
    print("degrees in: ", dict(sorted(graph.in_degree(), key=lambda x: x[1], reverse=True)))
    print("degrees out: ", dict(sorted(graph.out_degree(), key=lambda x: x[1], reverse=True)))
    print("degree centrality: ", dict(
        sorted(nx.degree_centrality(graph).items(), key=lambda x: x[1],
               reverse=True))) # -> meaning of node depending on its degree
    print("betweenness centrality: ", dict(
        sorted(nx.betweenness_centrality(graph, weight='weight').items(),
               key=lambda x: x[1], reverse=True)))# -> meaning of node based on amount of shortest paths through it
    print("eigenvector centrality: ", dict(
        sorted(nx.eigenvector_centrality(graph, weight='weight').items(),
               key=lambda x: x[1], reverse=True))) # -> meaning of node based on meaning of neighbors
    #
    # 2.) path and distances
    #
    if nx.is_strongly_connected(graph):
        print('Graph is strongly connected.')
        print("Largest strongly connected component:",
              max(nx.strongly_connected_components(graph), key=len))
        print("Shortest path between nodes:",
              dict(nx.shortest_path(graph, weight='weight'))) # -> shortest path between source node and target node
        print("Average shortest path length:",
              nx.average_shortest_path_length(graph, weight='weight')) # -> average distance between nodes (efficiency of spreading)
    else:
        print('Graph is not strongly connected.')
        largest_component = max(nx.strongly_connected_components(graph),
                                key=len)
        subgraph = graph.subgraph(largest_component).copy()
        print("Average shortest path length (largest component):",
              nx.average_shortest_path_length(subgraph, weight='weight'))
    #
    # 3.) clustering and community --> this would only make sense with undirected graphs
    #
    # print("indicator for connection between neighboors (high value = tight locale connectivity): ", nx.clustering(graph)) # -> indicator for connection between neighboors (high value = tight locale connectivity)
    # print("average indicator for cluster formation: ", nx.average_clustering(graph)) # -> average indicator for cluster formation
    # print("structure of network as collection of strong connected groups: ", nx.community.greedy_modularity_communities(graph)) # -> structure of network as collection of strong connected groups
    #
    # 4.) network visualization
    #
    nx.draw(graph) # -> draws graph
    #
    # 5.) draft of networktheories
    #
    # print("is every node connected to each other: ", nx.is_connected(graph)) # -> shows if every node is connected to each other
    # largest = max(nx.connected_components(graph), key=len) # -> subgroup in network, each node can be reached from each node
    # print("subgroup in network, each node can be reached from each node: ", largest)
    #
    # 6.) additional analysis
    #
    graph.remove_edges_from(nx.selfloop_edges(graph))
    print("Core number: ", nx.core_number(graph)) # -> indicator for nodes of dense subnetworks
    #nx.centrality # -> relative meaning or influence of node in network


def evaluate_smallworld(graph):
    #
    # 1.) calculate average shortest path length for our network and random small-world network
    #
    #nx.draw(graph, with_labels=True, font_weight='bold')
    #plt.show()
    if not nx.is_strongly_connected(graph):
        print(
            "Graph is not strongly connected. Small-world analysis may not be meaningful.")
        return
    smallworld = nx.erdos_renyi_graph(n=graph.number_of_nodes(), p=graph.number_of_edges() / (graph.number_of_nodes() * (graph.number_of_nodes() - 1) / 2) )
    graphShortestPath = nx.average_shortest_path_length(graph)
    smallworldShortestPath = nx.average_shortest_path_length(smallworld)
    #
    # 2.) calculate average clustering-coefficient for both networks
    #
    graphCC = nx.average_clustering(graph)
    smallworldCC = nx.average_clustering(smallworld)
    #
    # 3.) compare values
    #
    print('Layer shortest Path: ' + str(graphShortestPath) + ' clustering-coefficient: ' + str(graphCC))
    print('Small-world shortest Path: ' + str(smallworldShortestPath) + ' clustering-coefficient: ' + str(smallworldCC))
    #if average shortest path is close to the random network but cluster-coefficient is higher it shows small-world property
    #

def evaluate_scalefree(graph):

    # calculate degree distribution
    degree_sequence = sorted([d for n, d in graph.degree()], reverse=True)
    degree_count = np.bincount(degree_sequence)
    degrees = np.arange(len(degree_count))

    plt.figure(figsize=(10, 6))
    plt.bar(degrees, degree_count, width=0.80, color='b')

    plt.title("Degree Distribution")
    plt.ylabel("Amount Nodes")
    plt.xlabel("Degree")
    plt.show()

    # check potency law
    degree_counts = np.array(degree_count[1:])  # remove Null, no nodes with degree 0
    degrees = np.array(degrees[1:])

    plt.figure(figsize=(10, 6))
    plt.scatter(degrees, degree_counts, color='b')
    plt.xscale('log')
    plt.yscale('log')
    plt.title("Log-Log-Diagramm der Gradverteilung")
    plt.ylabel("Anzahl der Knoten")
    plt.xlabel("Grad")
    plt.show()

if __name__ == '__main__':


    input = []
    with open("D:\prog\seminar_komplexe_netze\scripts\layer_5_data_with_id.jsonl",
              "r") as inf:
        for line in inf:
            input.append(json.loads(line))

    orig_stdout = sys.stdout
    f = open(f'layer_5.txt', 'w')
    sys.stdout = f

    graph = generate_graph(input)
    # nx.draw(graph)
    # plt.show()
    analyze_graph(graph)
    evaluate_scalefree(graph)
    evaluate_smallworld(graph)
