import json
import os
import constants
from botocore.exceptions import ClientError


# ------------------------
# File-related functions
# ------------------------
def s3_file_exists(s3_client, bucket_name, key):
    try:
        s3_client.head_object(Bucket=bucket_name, Key=key)
        return True
    except ClientError as e:
        if e.response["Error"]["Code"]== "404":
            return False
        raise
   
     
def load_data_from_s3(s3_client, bucket_name, key):
    try:
        response=s3_client.get_object(Bucket=bucket_name, Key=key)
        content=response['Body'].read().decode('utf-8')
        return json.loads(content)
    except ClientError as e:
        print (f"failed to laod data: {e}")
        return {}

def save_data_to_s3(s3_client, bucket_name, key, data):
    try:
        s3_client.put_object(
            Bucket=bucket_name,
            Key=key,
            Body=json.dumps(data, ensure_ascii=False, indent=4),
            ContentType='application/json'
        )
        print(f"Data successfully saved to S3 at {key}")
    except ClientError as e:
        print(f"Failed to save data: {e}")


# local "db" - before the boto .. 
# def file_exists(file_path):
#      if not os.path.exists(file_path):
#         raise FileNotFoundError(f"File '{file_path}' does not exist.")

# def load_data(file_path):
#     with open(file_path, 'r', encoding='utf-8') as file:
#         return json.load(file)

# def save_data(file_path, data):
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