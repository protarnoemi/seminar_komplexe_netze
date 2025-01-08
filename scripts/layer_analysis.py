import json
import statistics
import numpy as np
import networkx as nx

# TODO: Comments

data = 'C:\Masterseminar\output_with_padding_random_1000.jsonl'

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
    with open(f"C:\\Masterseminar\\Layer{layernumber}.jsonl", 'w', encoding='utf-8') as outf:
        s='';
        for i in (d for n, d in g.degree()):
            s+=' '.join(str(i))
        outf.write(s+'\n')
        s = ' '.join(str(nx.clustering(g, n))for n in g.nodes);
        outf.write(s+'\n');
        s='';
        for source, path_dict in nx.all_pairs_shortest_path(g):
            for target, path in path_dict.items():
                s += f"{source}-{target}: {path}, ";
        outf.write(s+'\n\n\n');


    return 0

    # TODO: cut the data according to what we will agree upon


if __name__ == '__main__':
    reduce_data_by_layers(data)

    layers = []
    for i in range(6):
        layers.append(read_jsonl(f'C:\\Masterseminar\\layer_{i}.jsonl'))

    # for i, layer in enumerate(layers):
    #    print(f'layer {i}: ')
    #    print(calculate_weight_data(layer), '\n')"""

    thresholds = [0.009639047086238861, 0.00795428518205881, 0.005280134435743093, 0.001932974550873041, 0.004131996408104896, 0.0038631723914295426]
    for i, layer in enumerate(layers):
        print(f'layer {i}: ')
        generate_graph(layer, thresholds[i], i)
