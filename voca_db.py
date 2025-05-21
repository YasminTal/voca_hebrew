import json
import os
import constants

# ------------------------
# File-related functions
# ------------------------

def file_exists(file_path):
     if not os.path.exists(file_path):
        raise FileNotFoundError(f"File '{file_path}' does not exist.")

def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def save_data(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def append_word(data, unit, word, meaning):
    data[unit].append({"word": word, "meaning": meaning})

def update_word_in_unit(data, unit, word, new_meaning):
   
    for entry in data[unit]:
        if entry["word"] == word:
            entry["meaning"] = new_meaning
            return True
    return False

def delete_word(data, unit, word):
   
    original_len = len(data[unit])
    data[unit] = [entry for entry in data[unit] if entry["word"] != word]
    return len(data[unit]) < original_len

def print_list(unit,data):
    

    print(f"\n📘 Words in {unit}:")
    for entry in data[unit]:
        print(f"  - {entry['word']} : {entry['meaning']}")
    print()