import json
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize


def read_jsonl(filepath):
    """
    Reads a JSONL file and returns a list of dictionaries.
    """
    with open(filepath, 'r', encoding='utf-8') as file:
        return [json.loads(line) for line in file]


def combine_jsonls(layer_path, full_data_path, output_path):
    """
    Combines two JSONL files based on sentence matching and removes duplicates.
    """
    layer = read_jsonl(layer_path)
    full_data = read_jsonl(full_data_path)

    collected_sentences = set()
    combined_data = []

    for entry in layer:
        sentence = entry.get('sentence')
        for entry_full in full_data:
            sentence_1 = entry_full.get(
                'sentence1')
            # Check for a match and uniqueness
            if sentence == sentence_1 and sentence not in collected_sentences:
                # Combine the two entries into one
                combined_entry = {**entry,
                                  **entry_full}  # Merges the dictionaries
                combined_data.append(combined_entry)
                collected_sentences.add(sentence)

    print(json.dumps(combined_data[0], indent=2))

    with open(output_path, 'w', encoding='utf-8') as file:
        for entry in combined_data:
            sentence = entry['sentence']
            for sent in sent_tokenize(sentence):
                wordtokens = word_tokenize(sent)
                wordtokens_list = nltk.pos_tag(wordtokens)
                sentence_token_dict = {}
                for item in wordtokens_list:
                    sentence_token_dict[item[0].lower()] = item[1].lower()
                all_combined = {**entry,
                                  'tokenized_sentence': sentence_token_dict}
            file.write(json.dumps(all_combined) + '\n')





layer_0_path = r'D:\prog\seminar_komplexe_netze\layers\layer_0.jsonl'
full_data_path = r'multinli_1.0_dev_matched.jsonl'
output_path = r'combined_data_layer0_with_pos.jsonl'


combine_jsonls(layer_0_path, full_data_path, output_path)

