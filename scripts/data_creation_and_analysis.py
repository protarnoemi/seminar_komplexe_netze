import json
import statistics
import numpy as np

# TODO: Comments

data = 'D:\prog\SeminarArbeit\data\output_with_padding_random_1000.jsonl'


def dump_json(data, outfile):
    with open(f"{outfile}.jsonl", 'w', encoding='utf-8') as outf:
        for item in data:
            outf.write(json.dumps(item, ensure_ascii=False) + '\n')

def read_jsonl(filename) -> list:
    data = []
    with open(filename, 'r', encoding='utf-8') as inf:
        for line in inf:
            data.append(json.loads(line))

    return data


def create_data_by_layers(infile):
    with open(infile, 'r', encoding='utf-8') as inf:
        layer_0 = []
        layer_1 = []
        layer_2 = []
        layer_3 = []
        layer_4 = []
        layer_5 = []
        ctr = 0
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

def calculate_weight_data(layer):
    all_weights = []
    for line in layer:
        graph = line['graph']
        all_weights.extend(edge['weight'] for edge in graph['edges'])

    weight_data = {
        'max': max(all_weights),
        'min': min(all_weights),
        'mean': sum(all_weights) / len(all_weights),
        'median': statistics.median(all_weights),
        'stdev': statistics.stdev(all_weights)

    }

    return weight_data

def calculate_percentiles(layer):
    all_weights = []
    for line in layer:
        graph = line['graph']
        all_weights.extend(edge['weight'] for edge in graph['edges'])

    sorted_weights = sorted(all_weights)
    percentiles = np.linspace(0.05, 1, 20, endpoint=False)
    thresholds = [np.percentile(sorted_weights, p * 100) for p in percentiles]

    for i, t in enumerate(thresholds, start=1):
        print(f"{i * 5}%: {t}")
    return thresholds



if __name__ == '__main__':

    layers = []
    for i in range(6):
        layers.append(read_jsonl(f'D:\\prog\\SeminarArbeit\\data\\layer_{i}.jsonl'))

    # for i, layer in enumerate(layers):
    #    print(f'layer {i}: ')
    #    print(calculate_weight_data(layer), '\n')"""

    for i, layer in enumerate(layers):
        print(f'layer {i}: ')
        calculate_percentiles(layer)

