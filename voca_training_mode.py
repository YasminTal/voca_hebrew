

import voca_db
import voca_utils
import constants

FILE_PATH_CONST = constants.FILE_PATH_CONST

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
    list_words(2)