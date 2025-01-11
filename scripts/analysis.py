import networkx as nx
import json
import matplotlib.pyplot as plt
import numpy as np

data = 'C:\Masterseminar\output_with_padding_random_1000.jsonl'

def reduce_data_by_layers(infile):
    with open(infile, 'r', encoding='utf-8') as inf:
        layer_0 = []
        layer_1 = []
        layer_2 = []
        layer_3 = []
        layer_4 = []
        layer_5 = []
        for line in inf:
            data_line = json.loads(line)
            if data_line['layer'] == 0:
                layer_0.append(data_line)
            elif data_line['layer'] == 1:
                layer_1.append(data_line)
            elif data_line['layer'] == 2:
                layer_2.append(data_line)
            elif data_line['layer'] == 3:
                layer_3.append(data_line)
            elif data_line['layer'] == 4:
                layer_4.append(data_line)
            elif data_line['layer'] == 5:
                layer_5.append(data_line)
    dump_json(layer_0, 'layer_0')
    dump_json(layer_1, 'layer_1')
    dump_json(layer_2, 'layer_2')
    dump_json(layer_3, 'layer_3')
    dump_json(layer_4, 'layer_4')
    dump_json(layer_5, 'layer_5')

def dump_json(data, outfile):
    with open(f"C:\\Masterseminar\\{outfile}.jsonl", 'w', encoding='utf-8') as outf:
        for item in data:
            outf.write(json.dumps(item, ensure_ascii=False) + '\n')

def read_jsonl(filename) -> list:
    data = []
    with open(filename, 'r', encoding='utf-8') as inf:
        for line in inf:
            data.append(json.loads(line))

    return data

def generate_graph(layer, threshold, layernumber):
    g = nx.Graph()
    nodes=0;
    for line in layer:
        graph = line['graph']
        for i in graph['nodes']:
            if i['label'] == '[PAD]':
                nodes=i['id']-1;
                break;
            g.add_node(i['label']);
        for i in graph['edges']:
            if i['source'] > nodes:
                break;
            if i['weight']>threshold:
                g.add_edge(i['source'], i['target'])
    return g

def analyze_graph(graph):
    # 1.) degree and centrality
    #
    # nx.degree(graph,n) -> amount of direct neighboors
    # nx.degree_centrality(graph) -> meaning of node depending on it's degree
    # nx.betweenness_centrality(graph) -> meaning of node based on amount of shortest paths through it
    # nx.eigenvector_centrality(graph) -> meaning of node based on meaning of neighboors
    #
    # 2.) path and distances
    #
    # nx.shortest_path(graph, source, target) -> shortest path between source node and target node
    # nx.average_shortest_path_length(graph) -> average distance between nodes (efficiency of spreading)
    #
    # 3.) clustering and community
    #
    # nx.clustering(graph, node) -> indicator for connection between neighboors (high value = tight locale connectivity)
    # nx.average_clustering(graph) -> average indicator for cluster formation
    # greedy_modularity_communities(graph) -> structure of network as collection of strong connected groups
    #
    # 4.) networkvisualization
    #
    # nx.draw(graph, **kwargs) -> draws graph
    #
    # 5.) draft of networktheories
    #
    # nx.is_connected(graph) -> shows if every node is connected to each other
    # nx.strongly_connected_components(graph) -> subgroup in network, each node can be reached from each node
    # nx.weakly_connected_components(graph) -> subgroup in network, each node can be indirectly reached from each node
    #
    # 6.) additional analysis
    #
    # nx.core_numbers(graph) -> indicator for nodes of dense subnetworks
    # centrality -> relative meaning or influence of node in network

    with open(f"C:\\Masterseminar\\Layer{layernumber}.jsonl", 'w', encoding='utf-8') as outf:
        s='';
        for i in (d for n, d in graph.degree()):
            s+=' '.join(str(i))
        outf.write(s+'\n')
        s = ' '.join(str(nx.clustering(graph, n))for n in graph.nodes);
        outf.write(s+'\n');
        s='';
        for source, path_dict in nx.all_pairs_shortest_path(graph):
            for target, path in path_dict.items():
                s += f"{source}-{target}: {path}, ";
        outf.write(s+'\n\n\n');

def evaluate_smallworld(graph):
    #
    # 1.) calculate average shortest path length for our network and random small-world network
    #
    # nx.erdos_renyi_graph(n=graph.number_of_nodes(), p=graph.number_of_edges() / (graph.number_of_nodes() * (graph.number_of_nodes() - 1) / 2) )
    # nx.average_shortest_path_length(graph)
    #
    # 2.) calculate average clustering-coefficient for both networks
    #
    # nx.average_clustering(graph)
    #
    # 3.) compare values
    #
    # if average shortest path is close to the random network but cluster-coefficient is higher it shows small-world property
    #

    with open(f"C:\\Masterseminar\\Layer{layernumber}.jsonl", 'w', encoding='utf-8') as outf:
        s='';
        for i in (d for n, d in graph.degree()):
            s+=' '.join(str(i))
        outf.write(s+'\n')
        s = ' '.join(str(nx.clustering(graph, n))for n in graph.nodes);
        outf.write(s+'\n');
        s='';
        for source, path_dict in nx.all_pairs_shortest_path(graph):
            for target, path in path_dict.items():
                s += f"{source}-{target}: {path}, ";
        outf.write(s+'\n\n\n');

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
    reduce_data_by_layers(data)

    layers = []
    for i in range(6):
        layers.append(read_jsonl(f'C:\\Masterseminar\\layer_{i}.jsonl'))

    # for i, layer in enumerate(layers):
    #    print(f'layer {i}: ')
    #    print(calculate_weight_data(layer), '\n')"""

    thresholds = [0.009639047086238861, 0.00795428518205881, 0.005280134435743093, 0.001932974550873041,
                  0.004131996408104896, 0.0038631723914295426]
    for i, layer in enumerate(layers):
        print(f'layer {i}: ')
        g = generate_graph(layer, thresholds[i], i)
        evaluate_scalefree(g)
