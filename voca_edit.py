import constants
import voca_edit
import voca_db
import voca_utils
print("LOADED FROM:", voca_utils.__file__)
import json
import os

FILE_PATH_CONST = constants.FILE_PATH_CONST
name=constants.NAME

def add_word(unit, word, meaning):
    
    try:
        word, meaning = voca_utils.to_lower(word, meaning)
        unit = voca_utils.unit_key(unit)

        voca_utils.is_valid_word_and_meaning(word, meaning)
        voca_db.file_exists(FILE_PATH_CONST)  # Using the global FILE_PATH_CONST

        data = voca_db.load_data(FILE_PATH_CONST)

        voca_utils.unit_exists(data, unit)
        voca_utils.word_not_exists(data, unit, word)

        voca_db.append_word(data, unit, word, meaning)
        voca_db.save_data(FILE_PATH_CONST, data)
        print(f"✅ Word '{word}' added to unit '{unit}'.")

    except voca_utils.VocaError as e:
        print(f"❌ {e}")


def update_word(unit, word, new_meaning):
    try:
        word, new_meaning = voca_utils.to_lower(word, new_meaning)
        unit = voca_utils.unit_key(unit)

        voca_utils.is_valid_word_and_meaning(word, new_meaning)
        voca_db.file_exists(FILE_PATH_CONST)

        data = voca_db.load_data(FILE_PATH_CONST)
        voca_utils.unit_exists(data, unit)
        voca_utils.word_exists(data, unit, word)

        updated = voca_db.update_word_in_unit(data, unit, word, new_meaning)
        if updated:
            voca_db.save_data(FILE_PATH_CONST, data)
            print(f"✅ Word '{word}' updated in unit '{unit}' with new meaning.")
        else:
            print(f"❌ Failed to update word '{word}'.")

    except voca_utils.VocaError as e:
        print(f"❌ {e}")


def delete_word(unit, word):
    try:
        word = voca_utils.to_lower(word)[0]
        unit = voca_utils.unit_key(unit)

        voca_utils.unit_exists(voca_db.load_data(FILE_PATH_CONST), unit)
        voca_utils.word_exists(voca_db.load_data(FILE_PATH_CONST), unit, word)

        confirm = input(f"❓ Are you sure you want to delete '{word}' from '{unit}'? (y/n): ").strip().lower()
        if confirm != 'y':
            print("❎ Deletion cancelled.")
            return

        data = voca_db.load_data(FILE_PATH_CONST)
        deleted = voca_db.delete_word(data, unit, word)

        if deleted:
            voca_db.save_data(FILE_PATH_CONST, data)
            print(f"✅ Word '{word}' deleted from unit '{unit}'.")
        else:
            print(f"❌ Word '{word}' not found. Nothing deleted.")

    except voca_utils.VocaError as e:
        print(f"❌ {e}")

def list_words(unit):
    try:
        data = voca_db.load_data(FILE_PATH_CONST)
        unit = voca_utils.unit_key(unit)
        voca_utils.unit_exists(data, unit)

        voca_db.print_list(unit,data)
    except voca_utils.VocaError as e:
        print(f"❌ {e}")

if __name__ == "__main__":
    # add_word(3, 'bird', 'ציפור')
    # update_word(3, 'bird', 'עוף')
    # delete_word(3, 'bird')
    list_words(4)