import json
from collections import Counter

def read_jsonl(filename) -> list:
    data = []
    with open(filename, 'r', encoding='utf-8') as inf:
        for line in inf:
            data.append(json.loads(line))

    return data


if __name__ == '__main__':
    layer_data = read_jsonl('layer_0_data.jsonl')
    print('layer 0')

    #Self-attention
    self_attention_ctr = 0
    self_attention_count = Counter()
    self_attention_details = {}
    pos_counter_self_attention = Counter()
    pos_groups_self_attention = Counter()

    # Data with the most attention
    target_count = Counter()
    target_details = {}
    pos_counter_target = Counter()
    pos_groups_target = Counter()


    for item in layer_data:

        # Self-attention

        if item['source_token'] == item['target_token']:
            self_attention_ctr += 1
            source_token = item['source_token']
            self_attention_count[source_token] += 1
            pos_counter_self_attention[item['source_pos']] += 1
            if source_token not in self_attention_details:
                self_attention_details[source_token] = {
                    'token': source_token,
                    'pos': item.get('source_pos', None)
                }
            try:
                current_pos = item['source_pos'][0]
                pos_groups_self_attention[current_pos] += 1
            except:
                continue

        # Data with the most attention

        target_token = item['target_token']
        target_count[target_token] += 1
        pos_counter_target[item['target_pos']] += 1
        try:
            current_pos = item['target_pos'][0]
            pos_groups_target[current_pos] += 1
        except:
            continue


        if target_token not in target_details:
            target_details[target_token] = {
                'token': target_token,
                'pos': item.get('target_pos', None)
            }

    self_attention_filtered = {k: v for k, v in self_attention_count.items() if
                               v >= 10}
    target_filtered = {k: v for k, v in target_count.items() if v >= 20}

    print("Self-attention Counter:", self_attention_ctr)
    print("Self-attention Counts:", self_attention_filtered)
    print("Self attention pos counts: ", pos_counter_self_attention)
    print("POS groups Self attention: ", pos_groups_self_attention )


    print("Self-attention Details:", self_attention_details)
    print("Target Counts:", target_filtered)
    print("Target pos counts: ", pos_counter_target)
    print("Target Details:", target_details)
    print("POS groups target: ", pos_groups_target)