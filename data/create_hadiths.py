import json

def convert_json_to_jsonl(input_file_path, output_file_path):
    with open(input_file_path, 'r', encoding='utf-8') as input_file:
        data = json.load(input_file)

    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        for idx, entry in enumerate(data, start=1):
            new_entry = {
                "id": idx,
                "text": entry["translation"],
                "source": entry["title"],
                "metadata": {"chain": entry["chain"]}
            }
            # Write the new entry as a JSON object on a new line with ensure_ascii set to False
            json.dump(new_entry, output_file, ensure_ascii=False)
            output_file.write('\n')

# Example usage
convert_json_to_jsonl('translations_with_titles.json', 'hadiths.jsonl')
