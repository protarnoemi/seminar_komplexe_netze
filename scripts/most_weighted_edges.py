import json
import numpy as np

def read_jsonl(filename) -> list:
    data = []
    with open(filename, 'r', encoding='utf-8') as inf:
        for line in inf:
            data.append(json.loads(line))

    return data

def get_pos_tag(token, data, previous_entry):
    if token == '[CLS]':
        pos_tag = 'CLS'
    elif token == '[SEP]':
        pos_tag = 'SEP'
    elif token == '[PAD]':
        pos_tag = 'PAD'
    elif token in data['tokenized_sentence']:
        pos_tag = data['tokenized_sentence'][token]
    elif token == '##s':
        if previous_entry + 's' in data['tokenized_sentence']:
            pos_tag = data['tokenized_sentence'][previous_entry + 's']
        else:
            pos_tag = ''
    else:
        pos_tag = ''

    return pos_tag





if __name__ == '__main__':
    layer = read_jsonl('combined_data_layer_5_with_pos.jsonl')
    with open('layer_5_data.jsonl', 'a', encoding='utf-8') as outf:
        for item in layer:
            data = item
            # Extract edges and weights
            edges = data['graph']['edges']
            weights = np.array([edge['weight'] for edge in edges])

            # Determine the top 5% threshold
            threshold = np.percentile(weights, 95)

            # Filter edges with weight >= threshold
            top_edges = [edge for edge in edges if edge['weight'] >= threshold]


            # Collect results
            result = []
            for edge in top_edges:
                source_id = edge['source']
                target_id = edge['target']
                source_token = data['tokens'][source_id]
                target_token = data['tokens'][target_id]
                source_pos = get_pos_tag(source_token, data, previous_entry=data['tokens'][source_id-1])
                target_pos = get_pos_tag(target_token, data, previous_entry=data['tokens'][target_id-1])

                result.append({
                    "source_id": source_id,
                    "target_id": target_id,
                    "source_token": source_token,
                    "target_token": target_token,
                    "source_pos": source_pos,
                    "target_pos": target_pos,
                    "weight": edge['weight']
                })
            for line in result:
                outf.write(json.dumps(line))
                outf.write('\n')

